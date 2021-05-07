import sock as consts
import socket
import threading
import struct
from mypipe import MyPipe

listen_event_signal = False
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
	while True:
		wait_for_keyword_detection()
		listen_event_signal = True
		print("or type your cmd")
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

	th1 = threading.Thread(target=wait_for_listenning_thread, args=(1,), daemon=True)
	th1.start()
	global listen_event_signal
	while True:
		a = input("press 's' to start a new session...")
		if ( a == 's' and (len(a) == 1)):
			send_start_request()
		else:
			if( listen_event_signal == True):
			#	cmd = cmd.rstrip()
				cmd = a
				print('=======================================')
				print('Your command is:' + cmd + '\n')
				send_cmd_to_sdk(cmd)
				listen_event_signal = False

if __name__ == '__main__':
	main()
