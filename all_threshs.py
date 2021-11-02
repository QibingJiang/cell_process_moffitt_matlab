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
import re

from phagocytosis_detect import PhagocytosisDetector

import multiprocessing

import time
import imageio
from itertools import chain
from statistics import mean
import random as ra

path = "/home/qibing/disk_t/Pt210/RawData/Beacon-73/"
frame = cv2.imread(path + "scan_Plate_D_p0_0_D01f00d0.TIF")
# path = "/home/qibing/disk_t/Pt204/RawData/Beacon-21/"
# frame = cv2.imread(path + "scan_Plate_D_p0_0_A21f00d1.PNG")

frame_org = frame.copy()
frame = cv2.medianBlur(frame_org,
                       81)  # There is an unexpected effect when ksize is 81, applied to 8 times scaled image.
frame = frame.astype(float) / 100.0
frame = frame_org.astype(float) / frame.astype(float)

frame += 0.5  # rounding
np.clip(frame, 0, 255, out=frame)
frame = frame.astype(np.uint8)

# cv2.imshow("org", frame)
frame = cv2.GaussianBlur(frame, (3, 3), 0.1)
# cv2.imshow("GaussianBlur", frame)
# cv2.waitKey()

if (len(frame.shape) > 2):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    frame_draw = frame.copy()
else:
    gray = frame.copy()
    frame_draw = cv2.cvtColor(gray, cv2.COLOR_GRAY2BGR)

gray_org = gray.copy()
f_threshs = open(path + "f_threshs.txt", "w")

# cv2.namedWindow('stroma 0', cv2.WINDOW_NORMAL)
# cv2.resizeWindow('stroma 0', 900, 900)
# cv2.imshow('stroma 0', frame)
# cv2.waitKey()
# exit()

image_path = path + "threshs/"
if (not os.path.exists(image_path)):
    os.makedirs(image_path)

data = []
for i in range(256):
    print(i)
    ret, black = cv2.threshold(gray, i, 255, cv2.THRESH_BINARY)
    contours, hierarchy = cv2.findContours(black, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    th4 = np.zeros_like(frame_org)
    cv2.drawContours(th4, contours, -1, (0, 255, 0), 1)

    count = 0
    black_contour = []
    cell_r_s = []
    having_child = 0
    having_parent = 0
    orphan = 0
    for k in range(len(contours)):
        area = cv2.contourArea(contours[k])
        if(area > frame.shape[0] * frame.shape[1] * 0.8):
            break

    for j in range(len(contours)):
        try:
            if (hierarchy[0][j][2] != -1):  # having child
                black_contour.append(contours[j])
                having_child += 1
            if (hierarchy[0][j][3] != -1 and hierarchy[0][j][3] != k): # having parent
                having_parent += 1
            if (hierarchy[0][j][2] == -1 and hierarchy[0][j][3] == -1):
                orphan += 1
        except ZeroDivisionError:
            pass

    data.append([len(contours), having_child, having_parent, orphan])

    cv2.drawContours(th4, black_contour, -1, (255, 0, 0), 1)
    cv2.imwrite(path + "threshs/" + str(i) + ".jpg", th4)
    print(i, len(contours), count, file = f_threshs)

    # cv2.namedWindow('stroma 0', cv2.WINDOW_NORMAL)
    # cv2.resizeWindow('stroma 0', 900, 900)
    # cv2.imshow('stroma 0', th4)
    # cv2.waitKey()

data = np.array(data)
np.savetxt(path + "threshs/data.txt", data, fmt="%d")
x = np.arange(0, len(data), 1)
plt.plot(x, data[:, 0], label= "contour amount")
plt.plot(x, data[:, 1], label= "having_child")
plt.plot(x, data[:, 2], label= "having_parent")
plt.plot(x, data[:, 3], label= "orphan")
plt.legend(loc="best")
plt.show()