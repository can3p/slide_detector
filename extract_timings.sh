#!/usr/bin/env bash

rm -rf scenedetect_out
mkdir scenedetect_out
pushd scenedetect_out
#scenedetect -i ../talk.mov -st 00:01:13 -et 00:02:00 -d content -t 0.5 -si -o ../scenedetect.csv
scenedetect -i ../talk.mov -st 00:01:13 -d content -t 0.5 -si -o ../scenedetect.csv
popd
