#!/usr/bin/env python3
import cv2
import copy
from cell_detect import CellDetector
from cell_classify import CellClassifier
import os
from matplotlib import pyplot as plt
import numpy as np


# line0 = np.loadtxt("/home/qibing/disk_t/Pt210/RawData/Beacon-73/845.txt")
# line0 = np.loadtxt("/home/qibing/disk_t/Pt210/RawData/Beacon-73/293.txt")
# line0 = np.loadtxt("/home/qibing/disk_t/Pt210/RawData/Beacon-73/281.txt")
#
#
# line1 = np.loadtxt("/home/qibing/disk_t/Pt210/RawData/Beacon-73/192.txt")
# line1 = np.loadtxt("/home/qibing/disk_t/Pt210/RawData/Beacon-73/223.txt")
# line1 = np.loadtxt("/home/qibing/disk_t/Pt210/RawData/Beacon-73/230.txt")
# i = 20

# arr = ["174_overlap_change"]
# arr = ["845", "293", "281", "192", "223", "230"]
# arr = [[230, 233, 64], [174, 175, 49], [594, 131, 61]]
arr = [[198, 124, 244], [53, 144, 222], [338, 84, 154]]#(cell no, death time, death, time)
strs = ["cell_diff", "area", "ratio"]
# line0 = line0[100:]
# line1 = line1[100:]
# print(line)

plt.figure(0, figsize=(7.4, 5.7))
# a = np.arange(0, len(line1), 1)
a = np.zeros(0, dtype=int)

for feature in strs:
    for i in range(len(arr)):

        line = np.loadtxt("/home/qibing/disk_t/Pt210/RawData/Beacon-73/cell_feature/" + str(arr[i][0]) + "_" + feature + ".txt")

        if(len(a) == 0):
            a = np.arange(0, len(line), 1)

        # if(i < 3):
        #     plt.plot(a, np.array(line), linestyle='dashed', label = str(i))
        # else:
        #     plt.plot(a, np.array(line), label = str(i))

        plt.plot(a, np.array(line), label = str(arr[i][0]))
        plt.plot(arr[i][1], line[arr[i][1]], 'o')
        plt.plot(arr[i][2], line[arr[i][2]], 's')

        # plt.plot(a, np.array(line1))
        # plt.xlim(100, 150)
    plt.title(feature)
    plt.legend(loc='best')
    plt.show()

