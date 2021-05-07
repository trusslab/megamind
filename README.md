# MegaMind

MegaMind is a ...

Following this document we build MegaMind from source.
This tutorial has been tested on Ubuntu16.04 on a VMWare virtual machine with the following properties:
20GB of storage, 2GB of RAM and 4 CPUs.



## Download MegaMind source

Let assume you want to setup MegaMind in a directory called ``$WD``.
Since some of the following steps require absolute path please export the absolute path of your working directory to ``$WD``.
First you need to make a few directories in ``$WD``
```bash
	cd $WD
    mkdir MegaMind
	cd MegaMind
	mkdir MegaMind_Alexa_SDK MegaMind_engine
```
We clone a modified version of Amazon Alexa SDK into the ``MegaMind_Alexa_SDK`` and all other source codes for MegaMind in MegaMind_engine.
First lets download and setup ``MegaMind_Alexa_SDK``.

### Download and  setup MegaMind_Alexa_SDK
```bash
	cd $WD/MegaMind/MegaMind_Alexa_SDK
	mkdir application-necessities   build   third-party
```	
We need to install a few dependencies first.
```bash
	sudo apt-get install -y \
	git gcc cmake openssl clang-format libgstreamer1.0-0 gstreamer1.0-plugins-base \
	gstreamer1.0-plugins-good gstreamer1.0-plugins-bad \
	gstreamer1.0-plugins-ugly gstreamer1.0-libav gstreamer1.0-doc gstreamer1.0-tools \
	pulseaudio doxygen libsqlite3-dev repo libasound2-dev
```
We need to install more gstreamer packages as dependencies
```bash
	sudo  apt-get install -y \
	libgstreamer1.0-dev libgstreamer-plugins-base1.0-dev \
	gstreamer1.0-plugins-base gstreamer1.0-plugins-good \
	gstreamer1.0-plugins-bad gstreamer1.0-plugins-ugly \
	gstreamer1.0-libav libgstrtspserver-1.0-dev
```

```bash	
	
	sudo apt-get -y install build-essential nghttp2 libnghttp2-dev libssl-dev
```
Then we need to download a few third party binaries.	
```bash
	cd $WD/MegaMind/MegaMind_Alexa_SDK/third-party
	
	wget https://curl.haxx.se/download/curl-7.63.0.tar.gz
	tar xzf curl-7.63.0.tar.gz
	cd curl-7.63.0
	./configure --with-nghttp2 --prefix=/usr/local --with-ssl
	make && sudo make install
	sudo ldconfig
```
To verify curl installation please run:

```bash
	curl -I https://nghttp2.org/
```
the successful response should look like this:

  ```
HTTP/2 200
date: Fri, 15 Dec 2017 18:13:26 GMT
content-type: text/html
last-modified: Sat, 25 Nov 2017 14:02:51 GMT
etag: "5a19780b-19e1"
accept-ranges: bytes
content-length: 6625
x-backend-header-rtt: 0.001021
strict-transport-security: max-age=31536000
server: nghttpx
via: 2 nghttpx
x-frame-options: SAMEORIGIN
x-xss-protection: 1; mode=block
x-content-type-options: nosniff
```

Next we install PortAudio

```bash
	cd $WD/MegaMind/MegaMind_Alexa_SDK/third-party
	wget -c http://www.portaudio.com/archives/pa_stable_v190600_20161030.tgz
	tar xf pa_stable_v190600_20161030.tgz

	cd portaudio
	./configure --without-jack && make
```

Next we install the Kitt-AI wake-word detector

```bash
	cd $WD/MegaMind/MegaMind_Alexa_SDK/third-party
	git clone https://github.com/Kitt-AI/snowboy.git 

```
Kitt-AI requires some packages
```bash
	sudo apt-get install -y libblas-dev liblapack-dev 
```
We need to copy one file:
```bash
	cd $WD/MegaMind/MegaMind_Alexa_SDK/third-party/snowboy/resources
	cp alexa/alexa-avs-sample-app/alexa.umdl .
```

Now that we have all the packages let's clone the source code for  ``MegaMind_device_SDK``:
```bash
	cd $WD/MegaMind/MegaMind_Alexa_SDK/
	git clone https://github.com/trusslab/megamind_alexa_sdk.git source source
```
In order to build the SDK:
```bash
	cd $WD/MegaMind/MegaMind_Alexa_SDK//build/
	sudo apt install vim
	vim build.sh
```

And insert the following lines to build.sh:
 ```bash
	SDK_FOLDER=$WD/MegaMind/MegaMind_Alexa_SDK
	cmake $SDK_FOLDER/source \
	-DCMAKE_BUILD_TYPE=DEBUG \
	-DSENSORY_KEY_WORD_DETECTION=OFF \
	-DKITTAI_KEY_WORD_DETECTOR=ON \
	-DKITTAI_KEY_WORD_DETECTOR_LIB_PATH=$SDK_FOLDER/third-party/snowboy/lib/ubuntu64/libsnowboy-detect.a \
	-DKITTAI_KEY_WORD_DETECTOR_INCLUDE_DIR=$SDK_FOLDER/third-party/snowboy/include \
	-DGSTREAMER_MEDIA_PLAYER=ON \
	-DPORTAUDIO=ON \
	-DPORTAUDIO_LIB_PATH=$SDK_FOLDER/third-party/portaudio/lib/.libs/libportaudio.a \
	-DPORTAUDIO_INCLUDE_DIR=$SDK_FOLDER/third-party/portaudio/include \
	-DACSDK_EMIT_SENSITIVE_LOGS=ON   && make
```
  

### Download and  install MegaMind's components

MegaMind uses several third-party components such as speech-to-text and text-to-speech engines. In this step we install these components on the system.

#### Install FireJail
```bash
 cd $WD/MegaMind
 git clone https://github.com/netblue30/firejail.git  
 cd firejail  
sudo apt install gawk
 ./configure && make && sudo make install
 ```
#### Install pico2wav text-to-speech engine
```bash
 cd $WD/MegaMind
 sudo apt install libttspico-utils
 ```
#### Install python3.7 and its pip
```bash
sudo add-apt-repository ppa:deadsnakes/ppa
sudo apt update
sudo apt install python3.7
cd $WD/MegaMind
curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
python3.7 get-pip.py
sudo apt install python3.7-dev
 ```
#### Install required python packages
python3.7 -m pip install cryptography
python3.7 -m pip install halo
python3.7 -m pip install numpy
python3.7 -m pip install scipy
sudo apt install portaudio19-dev python3-pyaudio
python3.7 -m pip install pyaudio
python3.7 -m pip install deepspeech
python3.7 -m pip install webrtcvad




