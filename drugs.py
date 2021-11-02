#!/usr/bin/env python3
import cv2
import copy
import os
from matplotlib import pyplot as plt
import numpy as np
import multiprocessing
import time
# import imageio
from itertools import chain
from operator import add
from statistics import mean
import sys
import re
import pandas as pd

pt_drugs_list = []
pt_drugs = pd.DataFrame()

path = "/home/qibing/disk_t/"
files = os.listdir(path)
files = [x for x in files if ("Pt" in x and len(x) == 5)]
# print(files)
# exit()

# for pt in ["Pt170", "Pt180", "Pt204", "Pt210", "Pt211", "Pt238", "Pt171", "Pt181", "Pt242"]:
for pt in files:
    with open("/home/qibing/disk_t/" + pt + "/GraphPadFiles/PtSample/ExperimentalDesign.txt") as f:
        lines = f.readlines()

    drugs = []
    for l in lines:
        m = re.search(';(.+?);', l)
        drugs.append(m.group(1))

    drugs.sort()
    drugs.remove("CONTROL")
    drugs.remove("CONTROL")

    # print(*drugs)
    df = pd.DataFrame(np.ones(len(drugs)), columns=[pt], index=drugs)
    # df.set_index('drug')
    # print(df)
    pt_drugs = pt_drugs.join(df, how="outer")

    pt_drugs_list.append(df)

# pt_drugs = pd.merge(pt_drugs_list[1], pt_drugs_list[2], how="outer")
# pt_drugs = pt_drugs_list[1].join(pt_drugs_list[2], how="outer", lsuffix='_left', rsuffix='_right')
# pt_drugs = pt_drugs_list[1].join(pt_drugs_list[2], how="outer")

# print(pt_drugs)
pt_drugs.to_excel('./10_patients_10_drugs.xlsx')