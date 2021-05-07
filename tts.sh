#!/bin/bash
pico2wave -w=/tmp/test.wav "$1"
#play /tmp/test.wav
play -qV0 /tmp/test.wav treble 24 gain  -8
#play -qV0 /tmp/test.wav treble 24 gain  -24
rm /tmp/test.wav
