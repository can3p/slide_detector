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

The tool has two modes of detection - content and treshold, both modes have treshold setting (funny, right?)
I found content much more useful in my case. Since slides don't have much content I had to
set a really low treshold value. Something like this:

~~~bash
    scenedetect -i ../talk.mov -st 00:01:13 -d content -t 0.5 -si -o ../scenedetect.csv
~~~

The real script is [there](extract_timings.sh). Due to small treshold scendetect gives a lot
of false positives, and that is a real pain if you need to get all the matches manually.
I decided that I got too far at this point to switch to the manual mode and I'd better
spend a week tweaking the code and generate everything in a hour than spend an evening
matching the slides by hand, right?

So, I decided to check for possible solutions and it appears that opencv provides a bunch
of algorythms for feature matching, and they can be used for my purposes. I chose
[this][1] tutorial and used number of good matches as a metric for my purposes. It turned
our to be a really good ones - out of more than 3000 photos it failed to detect maybe
a hundred. The full detection script lives [there](compare_images.py).

I've been running this script back and forth lot's of times, and given that generation of
descriptors didn't itself depend on any parameters, I decided to [precalulate](dump_image_descriptiors.py)
them at least for reference images and then use those for comparison.

So, what's the state of things now? I have a list of 3k matches, most of them are correct,
but there are still errors. Additionally there is a plenty of consequetive timings that in
reality belong to the same slide. I decided to fix former and to join the latter.

Errors. During analysis I've made several assumptions. First - video shows slides and only
slides, second - presenter uses only buttons `left` and `right` on keyboard and hence there
are now jumps during slide changes. E.g. after the slide 18 we can expect only 17, 18 or 19.
Third assumptions is that my detection script works fine for the most part, which means that
errors are really a minority, that can be fixed.

I've found three kinds of errors:

* Slide fail to be detected at all. In this case you can have four options: n-1, x, n+1;
  n+1, n, n-1; n, x, n + 1; n, x, n - 1; First two cases are really trivial to fix (x = n),
  the other two have two solutions (e.g. n and n+1 in the first case) and a way to fix them
  could be to go and compile the list of such slides and correct information somewhere and
  patch program results when it's finished.

* Script detects wrong slide. I assume that it's not a frequent case, so there can be a limited
  set of broken slides and then sequence recoers. Basic example of this is: 16, 17, 16, 17, 20, 21.
  An obvious solution there is to find a jump in the sequence and that go in both directions from it
  till two correct numbers are found (meaning in correct position, e.g. 17 and 20 in the example).
  If found we can replace all the numbers between them with generated numbers. And yeah, I assume,
  that we have noise in detection but we detected *all* the slides.

* Combination of first two - we have jumps together with unknown slides. This case still needs to
  be checked.

....
Getting timings
....

After I got some timings I decided to check which tools can I use to generate the video.
The obvious choice is ffmpeg and description was found on [ffmpeg support forum](http://ffmpeg.gusari.org/viewtopic.php?f=25&t=39)
Duration can be specified [precisely](https://ffmpeg.org/ffmpeg-utils.html#time-duration-syntax)

[1]: http://opencv-python-tutroals.readthedocs.io/en/latest/py_tutorials/py_feature2d/py_feature_homography/py_feature_homography.html


