# MegaMind

MegaMind is a platform that enables users to deploy useful extensions on the Alexa virtual assistant. In the following document, we show how to build MegaMind from its source and deploy it on an x86 desktop. 

This tutorial has been tested on Ubuntu16.04 on a VMWare virtual machine with the following properties:
20GB of storage, 2GB of RAM, and 4 CPUs.



## Download MegaMind source

Let assume you want to set up MegaMind in a directory called ``$WD``.
First you need to make a few directories in ``$WD``
```bash
 cd $WD
 mkdir MegaMind
 cd MegaMind
 mkdir MegaMind_Alexa_SDK MegaMind_engine
```
We clone a modified version of Amazon Alexa SDK into the ``MegaMind_Alexa_SDK`` and all other source codes for MegaMind in MegaMind_engine.
First, lets download and set up ``MegaMind_Alexa_SDK``.

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
Then we need to download a few third-party binaries.    
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

Next, we install PortAudio

```bash
cd $WD/MegaMind/MegaMind_Alexa_SDK/third-party
wget -c http://www.portaudio.com/archives/pa_stable_v190600_20161030.tgz
tar xf pa_stable_v190600_20161030.tgz
cd portaudio
./configure --without-jack && make
```

Next, we install the Kitt-AI wake-word detector

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
 sudo apt install gawk
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
>>> nltk.download( 'wordnet')
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
### Download DeepSpeech's pre-trained english models
```bash
cd $WD/MegaMind/MegaMind_engine/deep_speech_models
curl -LO https://github.com/mozilla/DeepSpeech/releases/download/v0.9.3/deepspeech-0.9.3-models.pbmm
curl -LO https://github.com/mozilla/DeepSpeech/releases/download/v0.9.3/deepspeech-0.9.3-models.scorer

```
## Run MegaMind 

First, we need to provide the Client ID for each SDK for authentication purposes.
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

Then, we generate a run  script to run the Device SDK using the above file.

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

After authorization, you need to close all windows and run MegaMind again.
To do that, you can press 'ctrl+b' followed by ':' and type kill-session. Or you can press 'ctrl+c' and 'ctrl+d' multiple times.
To run MegaMind again
 
```bash
cd $WD/MegaMind/MegaMind_engine
tmuxp load mega.json
```

## Use MegaMind 
After running MegaMind, a tmux session opens with three panes. The upper-left pane, is the modified Alexa SDK. The upper-right pane is MegaMind engine logs, and the lower pane is the MegaMind API ( which can be a text based API -if you use mega.json- or voice based API -if you use megaVoice.json' to run MegaMind).

After running MegaMind, please wait until you see 

```bash
##################################
#      Alexa is currently idle    #
##################################
```
in upper left pane. 
After seeing this you can use the lower pane to insert your commands. 
You first need to press 's' followed by Enter key. Then you can type your command followed by Enter key.
For example you can type "what time is it" to check if the Alexa device is up and running.
Please note that for multi-turn conversations, you should not press 's' before each of your commands, when the Alexa (upper left pane) goes to "listening" state) the MegaMind text API, automatically asks you to insert your next command. 


### Test MegaMind's extensios
To show how MegaMind's extensions work in action, we enabled 3 simple extensions by default. A discarder that discards purchase-related utterances. A sanitizer that redacts first name of family members ( in this example, alex, steve and julia), and a companion extension which enables secure conversation with its companion skill. 
We also enabled two beta Alexa skills in our Alexa account to facilitate testing these extensions. The first one is 'repeat conversation' which simply repeats whatever you say after the keyword 'repeat'. The second one is 'confidential conversation' which echos whatever you say, but uses MegaMind enabled secure channel (It sends and recieves encrypted messages hidden from AVS). 

You can try the following commands to test some features of MegaMind. ( -your cmds,  +skill's responses)

```bash
- open repeat conversation
+ Welcome to mega mirror, what do you want me to repeat
- repeat it is a very nice day
+ you said it is a very nice day
- repeat please call steve 
+ you said please call ---- (a random name)
- repeat buy me a car
+ your message is discarded by parental control extension
```


```bash
- open confidential conversation
+ Welcome to the confidential conversation skill,  do you want to start a secret conversation?
- yes
+ A secure connection has established, tell me something
- how much money do i have in my bank account
+ you said how much money do i have in my bank account
- my name is julia
+ you said my name is ----- ( a random name)
- stop
+ Goodbye
```
You can see at the upper-left pane that Alexa is not aware of any of the above conversations and it only sees ciphertext.

If at any stage you see an error or any undefined behavior, please kill the tmux session, and run MegaMind again. 



### Test MegaMind's voice API

You can test MegaMind's voice API by running MegaMind using following commands:

```bash
cd $WD/MegaMind/MegaMind_engine
tmuxp load megaVoice.json
```
This time you do not need to press 's' to start a session. You can simply say 'Alexa' to start a session, and then you can say your commands. 
To get a good result from DeepSpeech speech to text please use headphones in a quiet environment. 













