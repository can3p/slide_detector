# How to fix stupidity with kickass tools

We had an awesome meetup this time. Excellent talks, cool people,
bad recording. We had only to microphones - in the laptop and go pro,
and screen recording was made with poor resolution, visible mouse
cursor and some other artifacts.

Although I couldn't do much with sound quality except what iMovie provides
me, I decided that I really can improve video quality by generating
a slideshow with timing that precisely the same is in the video (the
good part there was that Raphael only changed slides with forward/backward
keys, so picture was static otherwise.

First things first, I decided to generate s folder with all the slides
in high resolution.

I was able to do it with image magick:

~~~bash
    convert -geometry 3600x3600 -extent 4800x2700 -density 300x300 -quality 90 -gravity center -background "#32302f" liszp.pdf out/liszp-%04d.png
~~~

The real script is [there](extract_slides.sh). In reality a had to split
processing in batches because laptop ran out of space otherwise.

What the script does is it first extract the pages with the size that fits in 3600x3600
box and then changes resulting image to have dimensions 4800x2700 (16:9 aspect
ratio) and fills all new blank areas with background color that matches the color of
slides. output filename template specifies that I want all numbers to be padded with
leading zeroes to 4 digits.

After that I decided that I can just make a text file with timings for slide changes
and feed it along with slides pictures. At first I decided to just get the timings
manually, however it became boring on the third slide and I started looking for automation.

The cool tool that I found is [pyscenedetect](http://pyscenedetect.readthedocs.io/). It's
setup for mac os x is not trivial, however I found a [gist](https://gist.github.com/patrickgill/9660af2757b4e43ebe1c43c38e7ec711),
which I followed ([this](http://www.pyimagesearch.com/2016/11/28/macos-install-opencv-3-and-python-2-7/)
guide to install opencv).

scenedetect -i ~/Desktop/raphael\ liszt\ talk.mov -st 00:01:13 -et 00:10:00 -l -d content -t 0.5 -si

....
Getting timings
....

After I got some timings I decided to check which tools can I use to generate the video.
The obvious choice is ffmpeg and description was found on [ffmpeg support forum](http://ffmpeg.gusari.org/viewtopic.php?f=25&t=39)
Duration can be specified [precisely](https://ffmpeg.org/ffmpeg-utils.html#time-duration-syntax)




