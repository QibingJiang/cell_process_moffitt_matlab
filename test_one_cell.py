#!/usr/bin/env python3
import cv2
import copy
from cell_detect import CellDetector
from cell_classify import CellClassifier
import os
from matplotlib import pyplot as plt
import numpy as np
from phagocytosis_detect import PhagocytosisDetector
import multiprocessing
import time
# import imageio
from itertools import chain
from operator import add
from statistics import mean
import numpy.ma as ma

crop_width = 1328
crop_height = 1048
crop_width = 512
crop_height = 512
crop_width = 256
crop_height = 256
# crop_width = 128
# crop_height = 128


Beacon = 73
frame_count = 0
pt = "Pt210"
path = "/home/qibing/disk_t/" + pt + "/"
image_path = path + "RawData/Beacon-" + str(Beacon) + "/"
fourcc = cv2.VideoWriter_fourcc(*'mp4v')
old_frame = np.array(0)
old_area = 0
old_ratio = 0
ratio = 0
area = 0
vid = cv2.VideoCapture("/home/qibing/disk_t/Pt210/RawData/Beacon-73/cell_track_13_13_44.mp4")
scale = 8

# sum = []
#
# a = np.array([[0, 0, 0, 0],
#               [0, 1, 0, 0],
#               [0, 1, 1, 0],
#               [0, 0, 0, 0]])
# a = a.astype(np.uint8)
#
# contours, hierarchy = cv2.findContours(a, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
#
# print(contours, contours[0])
#
# print(cv2.contourArea(contours[0]))

# a = np.where(a > 4, 1, 0)
# b = np.count_nonzero(a)
# print(b)
# exit()

while True:
    # print(str(Beacon) + "_" + str(frame_count), end=" ", flush=True)
    ret, frame = vid.read()

    if not ret:
        break

    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    ret, th4 = cv2.threshold(frame, 120, 255, cv2.THRESH_BINARY)

    # detect the black edge is not satisfactory.
    # ret, black = cv2.threshold(frame, 95, 255, cv2.THRESH_BINARY)

    contours, hierarchy = cv2.findContours(th4, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    contours2 = []
    for cnt in contours:
        # x, y, w, h = cv2.boundingRect(cnt)
        (x, y), radius = cv2.minEnclosingCircle(cnt)
        if(frame.shape[1] - 3 * scale > x > 3 * scale and frame.shape[0] - 3 * scale > y > 3 * scale):
            # #### sum white
            my_mask = np.full((frame.shape[1], frame.shape[0]), 1, dtype=np.uint8)
            cv2.drawContours(my_mask, [cnt], -1, (0, 0, 0), -1)
            mask_arr = ma.masked_array(frame, mask=my_mask)
            out_arr = ma.sum(mask_arr)

            #### area
            # area = cv2.contourArea(cnt)

            ##### ratio
            # retval = cv2.minAreaRect(cnt)
            # ratio = min(retval[1][0], retval[1][1]) / max(retval[1][0], retval[1][1])

            # contours2.append(cnt)
            sum.append(out_arr)

    cv2.drawContours(frame, contours2, -1, (0, 0, 0), 1)
    cv2.namedWindow('frame',cv2.WINDOW_NORMAL)
    cv2.resizeWindow('frame', 900,900)
    cv2.imshow("frame", frame)
    cv2.waitKey()

    # if(frame_count > 0):
    #     diff = frame.astype(float) - old_frame.astype(float)
    #     diff = np.abs(diff)
    #     sum.append(np.sum(diff))

    # if(frame_count == 0):
    #     video_out = cv2.VideoWriter(path + "org_video_" + str(Beacon) + time.strftime("%d_%H_%M", time.localtime()) + ".mp4",
    #                           fourcc, 3.0, (frame.shape[1], frame.shape[0]), isColor=False)

    # video_out.write(frame)

    # cv2.namedWindow('frame',cv2.WINDOW_NORMAL)
    # cv2.resizeWindow('frame', 900,900)
    # cv2.imshow("frame", frame)
    # cv2.waitKey()

    # if frame_count > 0:
    #     diff = frame.astype(float) - old_frame.astype(float)
    #     diff = np.abs(diff).astype(np.uint8)
    #     cv2.namedWindow('frame', cv2.WINDOW_NORMAL)
    #     cv2.resizeWindow('frame', 900, 900)
    #     cv2.imshow("frame", diff)
    #     cv2.waitKey()

    old_frame = frame
    old_area = area
    old_ratio = ratio
    frame_count += 1

print(sum)

plt.figure(0, figsize=(7.4, 5.7))
a = np.arange(0, len(sum), 1)
plt.plot(a, np.array(sum))
plt.show()
