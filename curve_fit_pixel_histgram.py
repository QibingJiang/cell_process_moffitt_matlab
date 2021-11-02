#!/usr/bin/env python3
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import scipy as scipy
from scipy import optimize
from matplotlib import gridspec
from matplotlib.ticker import AutoMinorLocator
import matplotlib.ticker as ticker
import cv2
from lmfit import Model
from numpy import exp, loadtxt, pi, sqrt, linspace, random

# linearly spaced x-axis of 10 values between 1 and 10

def gaussian(x, amp, cen, wid):
    """1-d gaussian: gaussian(x, amp, cen, wid)"""
    return (amp / (sqrt(2*pi) * wid)) * exp(-(x-cen)**2 / (2*wid**2))

# def _1gaussian(x, amp1,cen1,sigma1):
#     return amp1*(1/(sigma1*(np.sqrt(2*np.pi))))*(np.exp((-1.0/2.0)*(((x-cen1)/sigma1)**2)))

def _1gaussian(x, amp1,cen1,sigma1):

    arr = np.array([amp1,cen1,sigma1])
    for data in arr:
        if data < 0:
            return float("inf")

    return amp1*(np.exp((-1.0/2.0)*(((x-cen1)**2)/(sigma1**2))))
    # return amp1*(1/(sigma1*(np.sqrt(2*np.pi))))*(np.exp((-1.0/2.0)*(((x-cen1)**2)/(sigma1**2))))


def _2gaussian(x, amp1,cen1,sigma1, amp2,cen2,sigma2):
    return _1gaussian(x, amp1,cen1,sigma1) + _1gaussian(x, amp2,cen2,sigma2)

def _3gaussian(x, amp1,cen1,sigma1, amp2,cen2,sigma2, amp3,cen3,sigma3):
    return _1gaussian(x, amp1,cen1,sigma1) + _1gaussian(x, amp2,cen2,sigma2) + _1gaussian(x, amp3,cen3,sigma3)


# frame = cv2.imread("/home/qibing/disk_t/Pt210/RawData/Beacon-73/scan_Plate_D_p0_0_D01f00d0.TIF")
frame = cv2.imread("/home/qibing/disk_t/Pt204/RawData/Beacon-21/scan_Plate_D_p0_0_A21f00d1.PNG")
# frame = imageio.imread(image_path)
# adjust luminance

if (len(frame.shape) > 2):
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
frame_org = frame.copy()
frame = cv2.medianBlur(frame_org, 81)
frame = frame.astype(float) / 100.0
frame = frame_org.astype(float) / frame.astype(float)

frame += 0.5  # rounding
# fra_max = frame.max()
# fra_min = frame.min()
# fra_range = fra_max - fra_min
# frame = (frame - fra_min) / fra_range * 255.0
# print("qibing: ", frame.max(), frame.min())


np.clip(frame, 0, 255, out=frame)

frame = frame.astype(np.uint8)

plt.figure(0, figsize=(16, 7))

plt.subplot(221)
print(frame)
plt.imshow(frame, cmap="gray")
plt.xticks([]), plt.yticks([])
plt.subplot(222)
hi = plt.hist(frame.flatten(), 256, [0, 256], alpha=0.5)
background_pixel = np.argmax(hi[0])

# target_peak = 100
# print(background_pixel, hi[0][background_pixel], hi[1][background_pixel])
# frame = np.where(frame > background_pixel, ((255 - target_peak) * frame - 255 * background_pixel + target_peak * 255) / (255 - background_pixel) + 0.5, frame)
# frame = np.where(frame < background_pixel, target_peak * frame / background_pixel + 0.5, frame)

plt.subplot(223)
print(frame)
plt.imshow(frame, cmap="gray")
plt.xticks([]), plt.yticks([])

plt.subplot(224)
hi = plt.hist(frame.flatten(), 256, [0, 256], alpha=0.5)


background_pixel = np.argmax(hi[0])
background_pixel_mean = frame.mean()
background_pixel_std = frame.std()

plt.plot(hi[1][background_pixel] + 0.05, hi[0][background_pixel], 'o',
         label="{0:.2f}".format(background_pixel_mean) + " {0:.2f}".format(background_pixel_std))
plt.legend(loc="best")
plt.xlim(0, )
plt.ylim(0, max(200000, hi[0][background_pixel]))

coordi_strr_2 = "[" + "{0}".format(int(hi[1][background_pixel])) + ", " + "{0}".format(int(
    hi[0][background_pixel])) + "]"
plt.text(hi[1][background_pixel] + 0.05, hi[0][background_pixel], coordi_strr_2)

print("background_pixel: ", hi[1][background_pixel] + 0.05, hi[0][background_pixel], background_pixel_mean, background_pixel_std)


# plt.show()
# exit()

# plt.savefig(path + str(pt) + "_" + str(Beacon) + "_pixel_hist.png")

# data = np.loadtxt("/home/qibing/disk_t/Pt204/RawData/Beacon-93/Pt204_93_radius_hist.txt")
# x_array = data[:, 0]
# y_array_2gauss = data[:, 1]

x_array = hi[1][0:-1]
y_array_2gauss = hi[0]
x_array = x_array.astype(int)
y_array_2gauss = y_array_2gauss.astype(int)

print(x_array)
# np.set_printoptions(precision=2, suppress=True)
print(y_array_2gauss)


# gmodel = Model(gaussian)
# result = gmodel.fit(y_array_2gauss, x=x_array, amp=5, cen=5, wid=1)

# # gmodel = Model(_1gaussian)
# # result = gmodel.fit(y_array_2gauss, x=x_array, amp1=5,cen1=5,sigma1=1)
# print(result.fit_report())
# exit()

p0_guess = [150000, 100, 4]
# p0_guess = [5, 5, 1]
# popt_2gauss, pcov_2gauss = scipy.optimize.curve_fit(gaussian, x_array, y_array_2gauss)
popt_2gauss, pcov_2gauss = scipy.optimize.curve_fit(_1gaussian, x_array, y_array_2gauss, p0 = p0_guess)#, maxfev = 5000)
# popt_2gauss, pcov_2gauss = scipy.optimize.curve_fit(_2gaussian, x_array, y_array_2gauss)
# popt_2gauss, pcov_2gauss = scipy.optimize.curve_fit(_3gaussian, x_array, y_array_2gauss)

perr_2gauss = np.sqrt(np.diag(pcov_2gauss))

pars_1 = popt_2gauss[0:3]
pars_2 = popt_2gauss[3:6]
pars_3 = popt_2gauss[6:9]

gauss_peak_1 = _1gaussian(x_array, *pars_1)
# gauss_peak_2 = _1gaussian(x_array, *pars_2)            
# gauss_peak_3 = _1gaussian(x_array, *pars_3)            

fig = plt.figure(figsize=(16,6))
gs = gridspec.GridSpec(1,2)
ax1 = fig.add_subplot(gs[0])

ax1.plot(x_array, y_array_2gauss)
ax1.plot(x_array, _1gaussian(x_array, *popt_2gauss), 'k--')
# ax1.plot(x_array, _2gaussian(x_array, *popt_2gauss), 'k--')
# ax1.plot(x_array, _3gaussian(x_array, *popt_2gauss), 'k--')

ax1.fill_between(x_array, gauss_peak_1.min(), gauss_peak_1, alpha=0.5, label = "{0:.2f}".format(popt_2gauss[0]) + " {0:.2f}".format(popt_2gauss[1]) + " {0:.2f}".format(popt_2gauss[2]))
# ax1.fill_between(x_array, gauss_peak_2.min(), gauss_peak_2, alpha=0.5, label = "{0:.2f}".format(popt_2gauss[3]) + " {0:.2f}".format(popt_2gauss[4]) + " {0:.2f}".format(popt_2gauss[5]))
# ax1.fill_between(x_array, gauss_peak_3.min(), gauss_peak_3, alpha=0.5, label = "{0:.2f}".format(popt_2gauss[6]) + " {0:.2f}".format(popt_2gauss[7]) + " {0:.2f}".format(popt_2gauss[8]))
    

# ax1.set_xlim(0,8)
# ax1.set_ylim(0,)

# ax1.set_xlabel("radius",family="serif",  fontsize=12)
# ax1.set_ylabel("Num of white points",family="serif",  fontsize=12)

print(popt_2gauss)
print(pcov_2gauss)

ax1.legend(loc="best")
fig.tight_layout()
plt.show()
fig.savefig("fit2Gaussian_peaks.png", format="png",dpi=1000)
