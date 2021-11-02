#!/usr/bin/env python3
import cv2
import copy
from cell_detect import CellDetector
from cell_classify import CellClassifier
import os
from matplotlib import pyplot as plt
import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
from libtiff import TIFF
import tifffile as tiff

from phagocytosis_detect import PhagocytosisDetector

import multiprocessing

import time
import imageio
from itertools import chain


vid = cv2.VideoCapture("/home/qibing/disk_t/Pt210/TimeLapseVideos/Beacon-73processed.avi")

path = "/home/qibing/disk_t/Pt210/"

scale = 8

fourcc = cv2.VideoWriter_fourcc(*'mp4v')

frame_count = 0

while (True):

    # Capture the video frame
    # by frame
    ret, frame = vid.read()

    if not ret:
        break

    frame = frame[0:256, 0:256, :]
    frame = cv2.resize(frame, (frame.shape[1] * scale, frame.shape[0] * scale), interpolation=cv2.INTER_CUBIC)
    # Display the resulting frame
    frame_0 = frame[:,:,0]
    frame_1 = frame[:,:,1]
    frame_2 = frame[:,:,2]

    red = frame_2.astype(np.float) - frame_1.astype(np.float)
    red_uint8 = np.clip(red, 0, 255).astype(np.uint8)

    ret, th4 = cv2.threshold(red_uint8, 10, 255, cv2.THRESH_BINARY)

    contours, hierarchy = cv2.findContours(th4, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    contours2 = []
    for cnt in contours:
        x, y, w, h = cv2.boundingRect(cnt)
        if(w > 5 * scale and h > 5 * scale):
            contours2.append(cnt)

    contour_img = frame.copy()

    cv2.drawContours(contour_img, contours2, -1, (0, 0, 255), int(0.3 * scale))

    if(frame_count == 0):
        video_out = cv2.VideoWriter(path + "red_masked_video" + time.strftime("%d_%H_%M", time.localtime()) + ".mp4",
                              fourcc, 3.0, (frame.shape[1], frame.shape[0]), isColor=True)

    video_out.write(contour_img)
    # cv2.namedWindow('frame',cv2.WINDOW_NORMAL)
    # cv2.resizeWindow('frame', 900,900)
    # cv2.imshow('frame', contour_img)
    #
    # if cv2.waitKey() & 0xFF == ord('q'):
    #     break
    frame_count += 1

# After the loop release the cap object
vid.release()
video_out.release()
# Destroy all the windows
cv2.destroyAllWindows()