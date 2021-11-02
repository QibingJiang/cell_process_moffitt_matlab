#!/usr/bin/env python3
import cv2
import copy
from cell_detect import CellDetector
from cell_classify import CellClassifier
import os
from matplotlib import pyplot as plt
import numpy as np
import sys
from itertools import chain 


# line0 = np.loadtxt("/home/qibing/disk_t/Pt204/RawData/Beacon-73/selected_cells/3028_cell_diff.txt")
# line0 = np.loadtxt("/home/qibing/disk_t/Pt204/RawData/Beacon-73/selected_cells/3028_cell_area.txt")
a1 = np.loadtxt(sys.argv[1])
a2 = np.loadtxt(sys.argv[2])
a3 = np.loadtxt(sys.argv[3])
# line0 = np.concatenate((np.array(a1[:,1]), np.array(a2[:,1]), np.array(a3[:,1])))
# line1 = np.concatenate((np.array(a1[:,2]), np.array(a2[:,2]), np.array(a3[:,2])))

lines = []
for i in range(10):
	line = np.concatenate((np.array(a1[:,i]), np.array(a2[:,i]), np.array(a3[:,i])))
	lines.append(line)


# m0 = np.mean(line0)
# m1 = np.mean(line1)
# print(m0, m1)
# line = np.array(line0)
# line[:] = m
# print(line0)
# line0 = np.diff(line0)
# line0 = np.abs(line0)
# print(line0)

# plt.scatter(np.arange(0, len(lines[2]), 1), np.array(lines[2]), label = "Peak 1 mean")
# plt.scatter(np.arange(0, len(lines[3]), 1), np.array(lines[3]), label = "Peak 1 std")

# plt.scatter(np.arange(0, len(lines[5]), 1), np.array(lines[5]), label = "Peak 2 mean")
# plt.scatter(np.arange(0, len(lines[6]), 1), np.array(lines[6]), label = "Peak 2 std")

plt.scatter(np.arange(0, len(lines[7]), 1), np.array(lines[7]), label = "Peak")
plt.scatter(np.arange(0, len(lines[8]), 1), np.array(lines[8]), label = "Mean")
plt.scatter(np.arange(0, len(lines[9]), 1), np.array(lines[9]), label = "std")

# print(lines[5].mean(), lines[6].mean())

plt.xlim(0, 150)
# min_y = np.min([np.min(lines[2:4]), np.min(lines[5:7])])
# max_y = np.max([np.max(lines[2:4]), np.max(lines[5:7])])
# plt.ylim(min_y, max_y)
# plt.ylim(-5, 5)

plt.legend(loc = "best")
plt.ylabel("radius")
plt.show()

## beacons = chain(range(1, 6, 1), range(11, 16, 1))
# beacons = chain(range(73, 78, 1))
# for bea in beacons:
# 	path = "/home/qibing/Work/2020_summer_research/Pt204/Results/Results_" + "{0:0=3d}".format(bea) + ".csv"
# 	line = np.genfromtxt(path, delimiter=',')[1:]
# 	plt.plot(np.arange(0, len(line), 1), np.array(line), label = str(bea))
# 	plt.ylim(0,10)

# legend = plt.legend(loc='best')
# plt.show()

