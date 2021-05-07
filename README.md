# MegaMind

MegaMind is a platform that enables users to deploy useful extensions on the Alexa virtual assistant. In the following document, we show how to build MegaMind from its source and deploy it on an x86 desktop. 

This tutorial has been tested on Ubuntu16.04 on a VMWare virtual machine with the following properties:
20GB of storage, 2GB of RAM and 4 CPUs.



## Download MegaMind source

Let assume you want to setup MegaMind in a directory called ``$WD``.
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
git clone https://github.com/trusslab/megamind_alexa_sdk.git source
```

In order to build the SDK:

```bash

cd $WD/MegaMind/MegaMind_Alexa_SDK/build/
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
-DACSDK_EMIT_SENSITIVE_LOGS=ON && make

```

to make MegaMind Alexa SDK

```bash
cd $WD/MegaMind/MegaMind_Alexa_SDK/build/
source build.sh
```

### Download and  install MegaMind's components

MegaMind uses several third-party components such as speech-to-text and text-to-speech engines. In this step we install these components on the system.

#### Install FireJail
```bash
 cd $WD/MegaMind
 git clone https://github.com/netblue30/firejail.git  
 cd firejail  
 ./configure && make && sudo make install
 sudo cp /lib/x86_64-linux-gnu/libssl.so.1.0.0 /usr/lib/
 ```
#### Install pico2wav text-to-speech engine
```bash
 cd $WD/MegaMind
 sudo apt install libttspico-utils
 sudo apt install sox
 ```
#
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

```bash
sudo python3.7 -m pip install --ignore-installed --target=/usr/lib/python3.7/ cryptography
python3.7 -m pip install halo
python3.7 -m pip install numpy
python3.7 -m pip install scipy
sudo apt install portaudio19-dev
python3.7 -m pip install pyaudio
python3.7 -m pip install deepspeech
python3.7 -m pip install webrtcvad

python3.7 -m pip install nltk
python3.7 -m pip install spacy==2.2.4
python3.7 -m pip install spacy_wordnet
python3.7 -m spacy download en
```
open python3.7 by typing
```shell
python3.7
```
in python3.7 shell please type the following commands:
```python
>>> import nltk
>>> nltk.download( ‘wordnet’)
```

#### Install tmuxp
```bash
sudo apt install tmux
python3.7 -m pip install tmuxp
```

### Download and  setup MegaMind engine
```bash
cd $WD/MegaMind
git clone https://github.com/trusslab/megamind.git MegaMind_engine/
 ```

## Run MegaMind 

First we need to provide the Client ID for each SDK for authentication purposes.
```bash
    cd $WD/MegaMind/MegaMind_Alexa_SDK/build/Integration
    vim AlexaClientSDKConfig_backup.json
```
and copy the following text into the file:
```json
{
   "deviceInfo":{
     "deviceSerialNumber":"123456",
     "clientId":"XXXX CLIENT_ID XXXX",
     "productId":"MegaMind_device1"
   },  
   "cblAuthDelegate":{
       "databaseFilePath":"XXWDXX/MegaMind/MegaMind_Alexa_SDK/application-necessities/cblAuthDelegate.db"
   },  
   "miscDatabase":{
       "databaseFilePath":"XXWDXX/MegaMind/MegaMind_Alexa_SDK/application-necessities/miscDatabase.db"
   },  
   "alertsCapabilityAgent":{
       "databaseFilePath":"XXWDXX/MegaMind/MegaMind_Alexa_SDK/application-necessities/alerts.db"
   },  
   "settings":{
       "databaseFilePath":"XXWDXX/MegaMind/MegaMind_Alexa_SDK/application-necessities/settings.db",
       "defaultAVSClientSettings":{
           "locale":"en-US"
       }
   },  
   "certifiedSender":{
      "databaseFilePath":"XXWDXX/MegaMind/MegaMind_Alexa_SDK/application-necessities/certifiedSender.db"
   },  
   "notifications":{
       "databaseFilePath":"XXWDXX/MegaMind/MegaMind_Alexa_SDK/application-necessities/notifications.db"
   }   
}

```

!!! note: please (1) replace XXWDXX with absolute path of $WD.  (2) please replace XXXX CLIENT_ID XXXX with your Amazon Alexa Device client ID.

Then we generate a run  script to run the Device SDK using the above file.

```bash
cd $WD/MegaMind/MegaMind_Alexa_SDK/build
vim run.sh
```
we insert the following code into the run.sh
```bash
rm Integration/AlexaClientSDKConfig.json
cp Integration/AlexaClientSDKConfig_backup.json Integration/AlexaClientSDKConfig.json
    ./SampleApp/src/SampleApp Integration/AlexaClientSDKConfig.json ../third-party/snowboy/resources/  NONE
```

now to run MegaMind:
```bash
cd $WD/MegaMind/MegaMind_engine
tmuxp load mega.json
```

The first time you run the Alexa device SDK on a new machine, it asks you to authorize your device with an Amazon account, showing the following messages.

```bash
##############################
#      NOT YET AUTHORIZED    #
##############################

###############################
To Authorize, browse to https://amazon.com/us/code and enter the code:xxxx
##############################
```
You need to follow the instructions and authorize the device. 

