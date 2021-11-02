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

y_array_2gauss = np.loadtxt("/home/qibing/disk_t/Pt210/RawData/Beacon-73/threshs/data.txt")[:, 3]
x_array = np.arange(0, len(y_array_2gauss), 1)
p0_guess = [y_array_2gauss.max(), 100, 4]
print(x_array, y_array_2gauss)
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
