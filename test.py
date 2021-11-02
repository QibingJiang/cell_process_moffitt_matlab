#!/usr/bin/env python3
import cv2
import copy
import os
from matplotlib import pyplot as plt
import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
import multiprocessing
import re
import time

import multiprocessing as mp
import random

def my_sleep(i):
    time.sleep(i)

def main():

    path = "/home/qibing/disk_t/"
    configure_path = "./configure.txt"

    log_f = open(path + "mylog.txt", "w")

    processes = []
    for pt in ["Pt170", "Pt180", "Pt204", "Pt210", "Pt211", "Pt238"]:
        for drug in ["CARFILZOMIB", "DEXAMETHASONE", "DMSO", "IXAZOMIB", "LENALIDOMIDE", "PANOBINOSTAT", "POMALIDOMIDE", "SR3029"]:
            print(pt, drug, file=log_f)
            if(pt == "Pt170" and drug == "BORTEZOMIB"):
                continue

            with open("/home/qibing/disk_t/" + pt + "/GraphPadFiles/PtSample/ExperimentalDesign.txt", "r") as f:
                lines = f.readlines()

            g2 = []
            for l in lines:
                m = re.search(';(.+?);', l)
                m_1 = m.group(1)

                if (drug + "_" == m_1 or drug + "_2" == m_1 or drug == m_1):# the drug == m_1 is for control
                    bea_str = l[0:m.start()]
                    bea_str = re.sub("Beacon-", "", bea_str)
                    bea_1 = bea_str.split(",")
                    g2.append(bea_1)

            bea_s = g2[0] + g2[1]
            bea_arr = np.array(bea_s)
            bea_arr = bea_arr.astype(np.int64)

            print(bea_arr)
            loop_cnt = 0

            for beacon in bea_arr:
                input_path = path + pt + "/RawData/Beacon-" + str(beacon) + "/"
                # cell_process.main(configure_path, input_path)
                # exit()

                try:
                    t = random.randrange(3)
                    p = multiprocessing.Process(target=my_sleep, args=(t, ))
                    p.start()
                    processes.append(p)
                    print(time.strftime("%d_%H_%M ", time.localtime()), p, input_path, file = log_f)
                    log_f.flush()

                except Exception as e:  # work on python 3.x
                    print('Exception: ' + str(e))

                loop_cnt = loop_cnt + 1

                while len(processes) == 10:
                    print(time.strftime("%d_%H_%M ", time.localtime()), len(processes), " processes are running.", file=log_f)
                    for p in processes:
                        if(p.is_alive() == False):
                            print(time.strftime("%d_%H_%M ", time.localtime()), p, file=log_f)
                            log_f.flush()
                            p.close()
                            processes.remove(p)
                            break
                        else:
                            print(time.strftime("%d_%H_%M ", time.localtime()), p, file=log_f)
                            pass
                    # if(len(processes) == 10):
                    time.sleep(1)

    log_f.close()
    print("All processes ended.")


# def main():
#
#     path = "/home/qibing/disk_t/"
#     configure_path = "./configure.txt"
#
#     log_f = open(path + "mylong.txt", "w")
#
#     processes = []
#
#     for pt in ["Pt170", "Pt180", "Pt204", "Pt210", "Pt211", "Pt238"]:
#         for drug in ["BORTEZOMIB", "CARFILZOMIB", "DEXAMETHASONE", "DMSO", "IXAZOMIB", "LENALIDOMIDE", "PANOBINOSTAT", "POMALIDOMIDE", "SR3029"]:
#
#             with open("/home/qibing/disk_t/" + pt + "/GraphPadFiles/PtSample/ExperimentalDesign.txt", "r") as f:
#                 lines = f.readlines()
#
#             g2 = []
#             for l in lines:
#                 m = re.search(';(.+?);', l)
#                 m_1 = m.group(1)
#
#                 if (drug + "_" == m_1 or drug + "_2" == m_1):
#                     bea_str = l[0:m.start()]
#                     bea_str = re.sub("Beacon-", "", bea_str)
#                     bea_1 = bea_str.split(",")
#                     g2.append(bea_1)
#
#             bea_s = g2[0] + g2[1]
#             bea_arr = np.array(bea_s)
#             bea_arr = bea_arr.astype(np.uint64)
#
#             loop_cnt = 0
#
#             for beacon in bea_arr:
#                 input_path = path + pt + "/RawData/Beacon-" + str(beacon) + "/"
#                 # cell_process.main(configure_path, input_path)
#                 # exit()
#
#                 try:
#                     t = random.randrange(5)
#                     p = multiprocessing.Process(target=my_sleep, args=(t, ))
#                     p.start()
#                     print(time.strftime("%d_%H_%M ", time.localtime()), p, input_path, file = log_f)
#                     log_f.flush()
#                     processes.append(p)
#
#                 except Exception as e:  # work on python 3.x
#                     print('Exception: ' + str(e))
#
#                 loop_cnt = loop_cnt + 1
#
#                 while len(processes) == 10:
#                     print(len(processes), " processes are running.")
#                     for p in processes:
#                         if(p.is_alive() == False):
#                             print(time.strftime("%d_%H_%M ", time.localtime()), p, file=log_f)
#                             log_f.flush()
#                             p.close()
#                             processes.remove(p)
#                             print(len(processes))
#                             break
#                         else:
#                             pass
#                     time.sleep(5)
#
#     log_f.close()
#     print("All processes ended.")

if __name__ == "__main__":
    # execute main
    main()

#
#
# with open("/home/qibing/disk_t/Pt180/GraphPadFiles/PtSample/ExperimentalDesign.txt") as f:
#     lines = f.readlines()
#
# g2 = []
# for l in lines:
#     m = re.search(';(.+?);', l)
#     m_1 = m.group(1)
#
#
#     if("BORTEZOMIB" + "_" == m_1 or "BORTEZOMIB" + "_2" == m_1):
#         bea_str = l[0:m.start()]
#         bea_str = re.sub("Beacon-", "", bea_str)
#         bea_1 = bea_str.split(",")
#         g2.append(bea_1)
#
# bea_s = g2[0] + g2[1]
# bea_arr = np.array(bea_s)
# bea_arr = bea_arr.astype(np.int)
# print(bea_arr)
#
# exit()
#
# l = []
# l.append(1)
# l.append(3)
# l.append(5)
# print(len(l))
# for p in l:
#     l.remove(p)
#     break
# print(l, len(l))
# exit()
#
# def foo(q):
#     print("I am here")
#     q.put('hello')
#
# print("I am here 3")
#
# if __name__ == '__main__':
#     print("I am here 2")
#     mp.set_start_method('spawn')
#     q = mp.Queue()
#     p = mp.Process(target=foo, args=(q,))
#     p.start()
#     print(q.get())
#     p.join()
#     exit()
#
# exit()
# # path = '/home/qibing/disk_t/Pt210/TimeLapseVideos/tmp/Beacon-191_tmp/mark_img_117.png'
# # path = '/home/qibing/disk_t/Pt210/TimeLapseVideos/tmp/Beacon-191_tmp/imj_j117.png'
#
# # path = "/home/qibing/disk_t/Pt210/TimeLapseVideos/tmp/Beacon_73_tmp/mark_img_13.png"
# path = "/home/qibing/disk_t/Pt210/TimeLapseVideos/tmp/Beacon_73_tmp/imj_j13.png"
# img = cv2.imread(path)
# img = cv2.resize(img, (img.shape[1] * 8, img.shape[0] * 8), interpolation=cv2.INTER_CUBIC)
#
# # crop_fm = img[841:1351, 6743:7268]
# # crop_fm = img[841:1351, 6743:(6743+510)]
# # cv2.imwrite(path + '_crop.png', crop_fm)
#
# crop_fm = img[(7416 - 510):7416, (985 - 510):985]
# cv2.imwrite(path + '_crop.png', crop_fm)
#
# # cv2.namedWindow('frame', cv2.WINDOW_NORMAL)
# # cv2.resizeWindow('frame', 900, 900)
# # cv2.imshow("frame", img)
# # cv2.waitKey()
# exit()
#
# for pt in ["Pt211", "Pt210"]:#"Pt211", "Pt210"
#     print(pt)
# exit()
#
# with open("tmp.txt","w") as f:
#     f.write("abd,")
#
# exit()
#
# path = "/home/qibing/disk_t/Pt204/RawData/Beacon-2/"
#
# files=os.listdir(path)
# files = [x for x in files if ("PNG" in x) or ("TIF" in x) or ("TIFF" in x) or ("JPG" in x) or ("JPEG" in x) or ("png" in x) or ("tif" in x) or ("tiff" in x) or ("jpg" in x) or ("jpeg" in x)]
#
# if(len(files) == 0):
#     print("No images can be found!")
#
# len_s = [len(x) for x in files]
# len_s = list(dict.fromkeys(len_s))
# len_s = np.array(len_s)
# len_s = np.sort(len_s)
# files_l =[]
# for i in range(len(len_s)):
#     a = [x for x in files if len(x) == len_s[i]]
#     a.sort()
#     files_l.append(a)
# files = [x for y in files_l for x in y]
# print(files)
#
# exit()
#
#
#
# # a = np.array([[1, 2, 3, 4, 5], [11, 12, 13, 14, 15]])
# #
# # b = a -1
# # b[:, 1] = b[:, 1] - 1
# # print(b[:, 1])
# # exit()
#
#
# # frame = cv2.imread("/home/qibing/disk_t/Pt204/RawData/Beacon-73/scan_Plate_D_p1_0_D01f00d1.PNG")
# # frame = imageio.imread(image_path)
# # adjust luminance
# if (len(frame.shape) > 2):
#     frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
# frame_org = frame.copy()
# frame = cv2.medianBlur(frame_org, 81)
#
# # frame = frame.astype(float) / 100.0
# # frame = frame_org.astype(float) / frame.astype(float)
# #
# # np.clip(frame, 0, 255, out=frame)
# # frame = frame.astype(np.uint8)
#
# plt.figure(0, figsize=(16, 7))
# plt.rcParams.update({'font.size': 16})
#
# plt.subplot(121)
# plt.imshow(frame, cmap="gray")
# plt.xticks([]), plt.yticks([])
# plt.subplot(122)
# hi = plt.hist(frame.flatten(), 256, [0, 256], alpha=0.5)
# background_pixel = np.argmax(hi[0])
# background_pixel_mean = frame.mean()
# background_pixel_std = frame.std()
# plt.plot(hi[1][background_pixel] + 0.05, hi[0][background_pixel], 'o',
#          label="{0:.2f}".format(background_pixel_mean) + " {0:.2f}".format(background_pixel_std))
# plt.legend(loc="best")
# plt.xlim(0, )
# plt.ylim(0, 200000)
#
# plt.show()
#
# # image_path = "/home/qibing/disk_t/Pt204/RawData/Beacon-73/scan_Plate_D_p0_0_D01f00d1.PNG"
# # #"/home/qibing/disk_t/Pt204/RawData/Beacon-73/scan_Plate_D_p1_0_D01f00d1.PNG"
# # frame = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
# #
# # frame_org = frame.copy()
# # background = cv2.medianBlur(frame_org, 81)  # There is an unexpected effect when ksize as 81, applied to 8 times scaled image.
# # frame = frame - background
# # background = background / 100
# # frame = frame_org / background
# # np.clip(frame, 0, 255, out=frame)
# # frame = frame.astype(np.uint8)
# #
#
# # ret, th4 = cv2.threshold(frame, 100, 255, cv2.THRESH_BINARY)
#
# #*** Fourier Transform
# # f = np.fft.fft2(frame)
# # fshift = np.fft.fftshift(f)
# # magnitude_spectrum = 20*np.log(np.abs(fshift))
# # plt.subplot(121)
# # plt.imshow(frame, cmap = 'gray')
# # # plt.title('Input Image'), plt.xticks([]), plt.yticks([])
# # plt.subplot(122)
# # plt.imshow(magnitude_spectrum, cmap = 'gray')
# # # plt.title('Magnitude Spectrum'), plt.xticks([]), plt.yticks([])
# # plt.show()
#
# # frames_arr = None
# # for i in range(100):
# #     image_path = "/home/qibing/disk_t/Pt204/RawData/Beacon-73/scan_Plate_D_p" + "{0:0=1d}".format(i) + "_0_D01f00d1.PNG"
# #                     #"/home/qibing/disk_t/Pt204/RawData/Beacon-73/scan_Plate_D_p1_0_D01f00d1.PNG"
# #     frame = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
# #
# #     if(i == 0):
# #         frames_arr = frame.flatten()
# #     else:
# #         frames_arr = np.concatenate((frames_arr, frame.flatten()))
# #
#
# #
# #
# # # frame = imageio.imread(image_path)
# #
# # # frame_org = frame.copy()
# # # frame = cv2.medianBlur(frame_org, 81)  # There is an unexpected effect when ksize as 81, applied to 8 times scaled image.
# # # frame = frame / 100
# # # frame = frame_org / frame
# # # np.clip(frame, 0, 255, out=frame)
# # # frame = frame.astype(np.uint8)
# #
#
# # histSize = 256
# # histRange = (0, histSize)  # the upper boundary is exclusive
# # frame_0_b_hist = cv2.calcHist([frame], [0], None, [histSize], histRange, accumulate=False)
# # window_hist_max_index = np.argmax(frame_0_b_hist)
# # print(window_hist_max_index)
#
# # a = np.arange(histSize)
# # plt.plot(a, frame_0_b_hist)
# #
# # plt.figure(0, figsize=(16, 7))
# # plt.hist(frame.flatten(), 256, [0, 256], alpha=0.5, label='Image a')
# # plt.show()
#
# # # out_image_path = out_path + "t" + "{0:0=3d}".format(frame_count) + ".tif"
# # # cv2.imwrite(out_image_path, frame)
