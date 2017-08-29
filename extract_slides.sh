#!/usr/bin/env bash

# usage:
# ./extract_slides path_to_presentation.pdf out_folder image_prefix start_idx end_idx
mkdir -p $2
convert -geometry 3600x3600 -extent 4800x2700 -density 300x300 -quality 90 -gravity center -background "#32302f" $1[$4-$5] $2/$3-%04d.png
