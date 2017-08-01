#!/usr/bin/env bash

# I decided to go with ranges there because my laptop simply ran out of space otherwise
convert -geometry 3600x3600 -extent 4800x2700 -density 300x300 -quality 90 -gravity center -background "#32302f" liszp.pdf[$1-$2] out/liszp-%04d.png

# here is a sequence of commands that I ran:
# mkdir out
# ./extract_slides.sh 0 20
# ./extract_slides.sh 21 30
# ./extract_slides.sh 31 60
# ./extract_slides.sh 61 100
# ./extract_slides.sh 101 130
# ./extract_slides.sh 131 156
:q!
