import sock as consts
import socket
import threading
import struct
from mypipe import MyPipe
import time, logging
from datetime import datetime
import threading, collections, queue, os, os.path
import deepspeech
import numpy as np
import pyaudio
import wave
import webrtcvad
from halo import Halo
from scipy import signal

logging.basicConfig(level=20)

listen_event_signal = False

jrecord = False

class Audio(object):
    """Streams raw audio from microphone. Data is received in a separate thread, and stored in a buffer, to be read from."""

    FORMAT = pyaudio.paInt16
    # Network/VAD rate-space
    RATE_PROCESS = 16000
    CHANNELS = 1
    BLOCKS_PER_SECOND = 50

    def __init__(self, callback=None, device=None, input_rate=RATE_PROCESS, file=None):
        def proxy_callback(in_data, frame_count, time_info, status):
            #pylint: disable=unused-argument
            if self.chunk is not None:
                in_data = self.wf.readframes(self.chunk)
            callback(in_data)
            return (None, pyaudio.paContinue)
        if callback is None: callback = lambda in_data: self.buffer_queue.put(in_data)
        self.buffer_queue = queue.Queue()
        self.device = device
        self.input_rate = input_rate
        self.sample_rate = self.RATE_PROCESS
        self.block_size = int(self.RATE_PROCESS / float(self.BLOCKS_PER_SECOND))
        self.block_size_input = int(self.input_rate / float(self.BLOCKS_PER_SECOND))
        self.pa = pyaudio.PyAudio()

        kwargs = {
            'format': self.FORMAT,
            'channels': self.CHANNELS,
            'rate': self.input_rate,
            'input': True,
            'frames_per_buffer': self.block_size_input,
            'stream_callback': proxy_callback,
        }

        self.chunk = None
        # if not default device
        if self.device:
            kwargs['input_device_index'] = self.device
        elif file is not None:
            self.chunk = 320
            self.wf = wave.open(file, 'rb')

        self.stream = self.pa.open(**kwargs)
        self.stream.start_stream()

    def resample(self, data, input_rate):
        """
        Microphone may not support our native processing sampling rate, so
        resample from input_rate to RATE_PROCESS here for webrtcvad and
        deepspeech

        Args:
            data (binary): Input audio stream
            input_rate (int): Input audio rate to resample from
        """
        data16 = np.fromstring(string=data, dtype=np.int16)
        resample_size = int(len(data16) / self.input_rate * self.RATE_PROCESS)
        resample = signal.resample(data16, resample_size)
        resample16 = np.array(resample, dtype=np.int16)
        return resample16.tostring()

    def read_resampled(self):
        """Return a block of audio data resampled to 16000hz, blocking if necessary."""
        return self.resample(data=self.buffer_queue.get(),
                             input_rate=self.input_rate)

    def read(self):
        """Return a block of audio data, blocking if necessary."""
        return self.buffer_queue.get()

    def destroy(self):
        self.stream.stop_stream()
        self.stream.close()
        self.pa.terminate()

    frame_duration_ms = property(lambda self: 1000 * self.block_size // self.sample_rate)

    def write_wav(self, filename, data):
        logging.info("write wav %s", filename)
        wf = wave.open(filename, 'wb')
        wf.setnchannels(self.CHANNELS)
        # wf.setsampwidth(self.pa.get_sample_size(FORMAT))
        assert self.FORMAT == pyaudio.paInt16
        wf.setsampwidth(2)
        wf.setframerate(self.sample_rate)
        wf.writeframes(data)
        wf.close()

#def start_session_notice_thread(name):
#	print("start_session_notice_thread")
#	global jrecord
#	while True:
#		a = input()
#		if( a =='s'):
#			jrecord = True
#			print('start recording')
#	return

class VADAudio(Audio):
    """Filter & segment audio with voice activity detection."""

    def __init__(self, aggressiveness=3, device=None, input_rate=None, file=None):
        super().__init__(device=device, input_rate=input_rate, file=file)
        self.vad = webrtcvad.Vad(aggressiveness)

    def frame_generator(self):
        """Generator that yields all audio frames from microphone."""
        if self.input_rate == self.RATE_PROCESS:
            while True:
                yield self.read()
        else:
            while True:
                yield self.read_resampled()

    def vad_collector(self, padding_ms=300, ratio=0.75, frames=None):
        """Generator that yields series of consecutive audio frames comprising each utterence, separated by yielding a single None.
            Determines voice activity by ratio of frames in padding_ms. Uses a buffer to include padding_ms prior to being triggered.
            Example: (frame, ..., frame, None, frame, ..., frame, None, ...)
                      |---utterence---|        |---utterence---|
        """
        global jrecord
        if frames is None: frames = self.frame_generator()
        num_padding_frames = padding_ms // self.frame_duration_ms
        ring_buffer = collections.deque(maxlen=num_padding_frames)
        triggered = False
        initial_frames = 0
        for frame in frames:
            if len(frame) < 640:
                return

            is_speech = self.vad.is_speech(frame, self.sample_rate)
            
            if(jrecord == True):
                if(initial_frames < 50):
                     is_speech = True
                ring_buffer.append((frame, is_speech))
                num_unvoiced = len([f for f, speech in ring_buffer if not speech])
                yield frame
                initial_frames = initial_frames + 1
                if num_unvoiced > ratio * ring_buffer.maxlen:
                    jrecord = False
                    initial_frames = 0
                    print('finish recording')
                    yield None
                    ring_buffer.clear() 





def send_cmd_to_sdk(cmd):
	speech_recog_end_pipe.write_to_pipe(cmd)
	return
def wait_for_keyword_detection():
	speech_recog_start_pipe.wait_on_pipe()
	return
		
def send_start_request():
#	print("Sendign start request from Megamind Text API")
#	with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:	
#		s.connect( (consts.Host,consts.PortNumber_text_start_req) )
#		s.sendall("start".encode())
#		s.close()
#		return
	global pipe_start
	pipe_start.write_to_pipe('s')
	
def wait_for_listenning_thread(name):
	print('wait_for_listenning_thread')
	global listen_event_signal
	global jrecord
	while True:
		wait_for_keyword_detection()
		listen_event_signal = True
		jrecord = True
		print("Say your cmd")
	#	while(listen_event_signal == True):
	#		pass
def main():
	print('Welcome to MegaMind Text API')
	global pipe_start 
	pipe_start =  MyPipe('text_start_request')
	pipe_start.make()
	global speech_recog_start_pipe
	speech_recog_start_pipe = MyPipe('speech_recog_start')
	global speech_recog_end_pipe
	speech_recog_end_pipe = MyPipe('speech_recog_end')

	DEFAULT_SAMPLE_RATE = 16000

	th1 = threading.Thread(target=wait_for_listenning_thread, args=(1,), daemon=True)
	th1.start()
	global listen_event_signal

	print('Initializing model...')
	model = deepspeech.Model('deep_speech_models/deepspeech-0.7.0-models.pbmm')
	model.enableExternalScorer('deep_speech_models/deepspeech-0.7.0-models.scorer')
	# Start audio with VAD
	vad_audio = VADAudio(aggressiveness=3,
		device=None,
		input_rate=DEFAULT_SAMPLE_RATE,
		file=None)

	print("Listening (ctrl-C to exit)...")
	frames = vad_audio.vad_collector()
	spinner = Halo(spinner='line')
	stream_context = model.createStream()
	for frame in frames:
		if frame is not None:
			spinner.start()
			stream_context.feedAudioContent(np.frombuffer(frame, np.int16))
		else:
			spinner.stop()
			text = stream_context.finishStream()
			print("Recognized: %s" % text)
			send_cmd_to_sdk(text)
			listen_event_signal = False
			stream_context = model.createStream()



if __name__ == '__main__':
	main()
