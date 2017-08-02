import os
import numpy as np
import cv2
import sys
import glob
import re
import pickle
import operator

# Initiate SIFT detector
sift = cv2.xfeatures2d.SIFT_create()

def get_matches_count(des1, des2):
    FLANN_INDEX_KDTREE = 0
    index_params = dict(algorithm = FLANN_INDEX_KDTREE, trees = 5)
    search_params = dict(checks = 50)

    flann = cv2.FlannBasedMatcher(index_params, search_params)

    # return  len([ m.distance for m in flann.match(des1,des2) if m.distance < 160 ])
    # return  - reduce(operator.add, [ m.distance for m in flann.match(des1,des2)])
    matches = flann.knnMatch(des1,des2,k=2)

    # store all the good matches as per Lowe's ratio test.
    good = []
    for m,n in matches:
        if m.distance < 0.7*n.distance:
            good.append(m)

    return len(good)

def get_decriptors_from_folder(image_folder):
    descriptors = []
    all_files = next(os.walk(image_folder))[2]
    all_count = len(all_files)

    for file_name_temp in all_files:
        train_image = image_folder + '/' + file_name_temp

        with open(train_image, 'rb') as f:
            des = pickle.load(f)

        descriptors.append([file_name_temp, des])
        if len(descriptors) % 20 == 0:
            print "loaded {} out of {}".format(len(descriptors), all_count)

    print "done"
    return descriptors

def get_timings(fname):
    with open(fname, 'r') as f:
        line = f.readline().rstrip()
        lines = line.split(',')
        lines[0] = '00:00:00.000'
        return lines

def get_best_match(query_fname, target_descriptor, descriptors, idx):
    max_idx = -1
    max_matches = 0
    max_fname = ''

    if idx == 0:
        idxes_to_check = range(0, len(descriptors))
    else:
        idxes_to_check = [i for i in [idx -1, idx, idx + 1] if i >= 0 and i < len(descriptors) ]

    scores = []

    for current_idx in idxes_to_check:
        [fname, des] = descriptors[current_idx]
        matches =  get_matches_count(target_descriptor, des)
        scores.append(matches)
        if matches > max_matches:
            max_matches = matches
            max_idx = current_idx
            max_fname = fname

    if max_idx < idx:
        print "started moving backwards? Scores: ", scores, " filename: ", query_fname

    if max_idx == -1 and idx != 0:
        print "Failed to find slide amongst nearest neighbours, checking all slides"
        return get_best_match(query_fname, target_descriptor, descriptors, 0)

    return max_idx, max_fname

def get_test_images(folder):
    files = glob.glob('{}/*OUT.jpg'.format(folder))
    files.sort(key=lambda x: int(re.findall(r'\d+', x)[0]))

    return files[1:] # first frame looks duplicated let's throw her our to get better timings


print "getting timings"
timings =  get_timings('scenedetect.csv')

test_images = get_test_images('scenedetect_out')

if len(timings) < len(test_images):
    print "we don't have enough timings ({}) for all images({}), unable to proceed".format( len(timings), len(test_images))
    sys.exit(1)

image_folder = 'out.pickle'
# image_folder = 'out_thumb'
print "loading image db";
descriptors = get_decriptors_from_folder(image_folder)
current_idx = 0
timing_idx = 0;
out_file = 'slides_timings_generated.txt'

output = []

if len(sys.argv) == 3:
    print "Checking scores for {} around index {}".format(sys.argv[1], sys.argv[2])
    query_image = sys.argv[1]
    current_idx = int(sys.argv[2])
    img = cv2.imread(query_image, 0)
    _, target_descriptor = sift.detectAndCompute(img, None)

    matches =  [ (des[0], get_matches_count(target_descriptor, des[1])) for des in descriptors[current_idx - 1:current_idx + 2] ];
    print "Scores: ", matches

    sys.exit(0)



for query_image in test_images:
    img = cv2.imread(query_image, 0)
    _, des = sift.detectAndCompute(img, None)

    query_image_base = query_image.split("/")[1]
    current_idx, slide_fname = get_best_match(query_image_base, des, descriptors, current_idx)
    if current_idx < 0:
        print "Failed at timing ", timings[timing_idx]
        output.append("{}    {}     {}".format(query_image_base, "unknown", timings[timing_idx]))
        current_idx = 0
    else:
        output.append("{}    {}     {}".format(query_image_base, slide_fname, timings[timing_idx]))

    timing_idx = timing_idx + 1
    if len(output) % 50 == 0:
        print "Processed {} out of {}".format(len(output), len(test_images))


print "Writing the output"
with open(out_file, 'w') as f:
    f.write('\n'.join(output))

