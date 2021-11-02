#!/usr/bin/env python3
import cv2
import copy
from matplotlib import pyplot as plt
import numpy as np
import sys

# g_truth = np.loadtxt("/home/qibing/Work/2020_summer_research/Pt204/g_truth.txt")
# die_time = np.loadtxt("/home/qibing/Work/2020_summer_research/Pt204/die_time.txt") sys.argv[1]

# g_truth = np.loadtxt("/home/qibing/disk_t/Pt204/RawData/Beacon-73/g_truth.txt")
# die_time = np.loadtxt("/home/qibing/disk_t/Pt204/RawData/Beacon-73/die_time.txt")

g_truth = np.loadtxt(sys.argv[1])
die_time = np.loadtxt(sys.argv[2])


if 1:
	diff_0 = np.zeros((len(g_truth), 4))
	diff_0[:,0:3] = g_truth[:,:]
	diff_0[:, 3] = die_time[:, 1]

	g_truth_all_dead = np.count_nonzero(diff_0[2] == -1)
	die_time_all_dead = np.count_nonzero(diff_0[3] == -1)
	print("die at start: ", g_truth_all_dead, die_time_all_dead)

	g_truth_1000 = diff_0[diff_0[:, 2] == 1000, :]
	die_time_1000 = diff_0[diff_0[:, 3] == 1000, :]
	# and_1000 = g_truth_1000[g_truth_1000[:, 3] == 1000, :]
	g_truth_1000 = -g_truth_1000[g_truth_1000[:, 3] != 1000, :]
	and_1000 = die_time_1000[die_time_1000[:, 2] == 1000, :]
	die_time_1000 = die_time_1000[die_time_1000[:, 2] != 1000, :]
	comb_att = np.concatenate((g_truth_1000[:, 3], np.zeros((len(and_1000))), die_time_1000[:, 2]))

	plt.figure(0)
	plt.hist(comb_att, bins='auto')
	# plt.hist(g_truth_1000[:, 1], bins='auto')
	# plt.hist(die_time_1000[:, 1], bins=np.arange(-300, 300))
	# plt.xlim(-300, 300)
	# plt.ylim(0, 600)
	# plt.show()
	# exit()

	normal = diff_0[diff_0[:, 2] > -1, :]
	normal = normal[normal[:, 2] < 1000, :]
	normal = normal[normal[:, 3] > -1, :]
	normal = normal[normal[:, 3] < 1000, :]

	normal = normal[:,2] - normal[:,3]
	plt.figure(1)
	plt.hist(normal, bins='auto')
	# plt.hist(comb_att, bins=np.arange(-300, 300))
	plt.xlim(-300, 300)
	plt.ylim(0, 600)
	plt.show()
	diff = np.abs(normal)
	print("len(diff): ", len(diff))
else:
	diff_0 = g_truth[:,1] - die_time[:,1]
	# plt.hist(diff, bins='auto')
	plt.hist(diff_0, bins=np.arange(-50, 50))
	plt.xlim(-50, 50)
	plt.ylim(0, )
	plt.show()

	diff = np.abs(diff_0)

cond_3 = np.count_nonzero(diff < 3)
cond_5 = np.count_nonzero(diff < 5)
cond_10 = np.count_nonzero(diff < 10)

print(cond_3, cond_5, cond_10, np.count_nonzero(diff >= 10))
