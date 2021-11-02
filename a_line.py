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


# data = np.loadtxt("/home/qibing/Work2/OneDrive_1_11-2-2020/area.txt")
# x = np.arange(0, len(data), 1)
# # plt.plot(x[:16], data[:16, 0], label= "Cell 38")
# # plt.plot(x[4:], data[4:, 1], label= "Cell 90")
# plt.plot(x, data[:, 0], label= "Nucleus 47")
# plt.plot(x[11:], data[11:, 1], label= "Nucleus 102")
# plt.xlim(0, 18)
# plt.xlabel("Image Index")
# plt.ylim(0, )
# plt.ylabel("area")
# plt.legend(loc="best")
# plt.show()

diff_path = "/home/qibing/Work/paper_1/Pt210_73/version_2/cell_159_diff_max.txt"
table = np.loadtxt(diff_path)

plt.rcParams.update({'font.size': 16})

plt.figure(0)
plt.plot(table)
plt.xlim(0, )
plt.ylim(0, )

plt.xlabel("Time Point(t)")
plt.ylabel("Max SSR")
plt.tight_layout()
plt.savefig(diff_path + ".png")

area_path = "/home/qibing/Work/paper_1/Pt210_73/version_2/cell_159_area_max.txt"
table = np.loadtxt(area_path)
# table = np.diff(table)

plt.figure(1)
plt.plot(table)
plt.xlim(0, )
plt.ylim(0, )

plt.xlabel("Time Point(t)")
plt.ylabel("Max ∆Area")
plt.tight_layout()
# plt.show()
plt.savefig(area_path + ".png")


## beacons = chain(range(1, 6, 1), range(11, 16, 1))
# beacons = chain(range(73, 78, 1))
# for bea in beacons:
# 	path = "/home/qibing/Work/2020_summer_research/Pt204/Results/Results_" + "{0:0=3d}".format(bea) + ".csv"
# 	line = np.genfromtxt(path, delimiter=',')[1:]
# 	plt.plot(np.arange(0, len(line), 1), np.array(line), label = str(bea))
# 	plt.ylim(0,10)

# legend = plt.legend(loc='best')
# plt.show()

