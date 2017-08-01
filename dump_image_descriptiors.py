import os
import numpy as np
import cv2
import pickle

# Initiate SIFT detector
sift = cv2.xfeatures2d.SIFT_create()

def get_decriptors_from_folder(image_folder):
    descriptors = []
    all_files = next(os.walk(image_folder))[2]

    for file_name_temp in all_files:
        train_image = image_folder + '/' + file_name_temp
        print "load ", train_image

        img = cv2.imread(train_image, 0)          # queryImage
        _, des = sift.detectAndCompute(img,None)

        descriptors.append([file_name_temp, des])

    return descriptors


in_folder = 'out'
out_folder = 'out.pickle'

all_files = next(os.walk(in_folder))[2]

for file_name_temp in all_files:
    train_image = in_folder + '/' + file_name_temp
    out_image = out_folder + '/' + file_name_temp
    print "processing ", train_image

    img = cv2.imread(train_image, 0)          # queryImage
    _, des = sift.detectAndCompute(img,None)
    with open(out_image, 'wb') as f:
        pickle.dump(des, f)
