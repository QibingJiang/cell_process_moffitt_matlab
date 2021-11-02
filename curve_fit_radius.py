#!/usr/bin/env python3
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import scipy as scipy
from scipy import optimize
from matplotlib import gridspec
from matplotlib.ticker import AutoMinorLocator
import matplotlib.ticker as ticker

# linearly spaced x-axis of 10 values between 1 and 10

# def _1gaussian(x, amp1,cen1,sigma1):
#     return amp1*(1/(sigma1*(np.sqrt(2*np.pi))))*(np.exp((-1.0/2.0)*(((x-cen1)/sigma1)**2)))

def _1gaussian(x, amp1,cen1,sigma1):

    arr = np.array([amp1,cen1,sigma1])
    for data in arr:
        if data < 0:
            return float("inf")

    return amp1*(1/(sigma1*(np.sqrt(2*np.pi))))*(np.exp((-1.0/2.0)*(((x-cen1)/sigma1)**2)))


def _2gaussian(x, amp1,cen1,sigma1, amp2,cen2,sigma2):
    return amp1*(1/(sigma1*(np.sqrt(2*np.pi))))*(np.exp((-1.0/2.0)*(((x-cen1)/sigma1)**2))) + \
            amp2*(1/(sigma2*(np.sqrt(2*np.pi))))*(np.exp((-1.0/2.0)*(((x-cen2)/sigma2)**2)))

def _3gaussian(x, amp1,cen1,sigma1, amp2,cen2,sigma2, amp3,cen3,sigma3):
    return _1gaussian(x, amp1,cen1,sigma1) + _1gaussian(x, amp2,cen2,sigma2) + _1gaussian(x, amp3,cen3,sigma3)

data = np.loadtxt("/home/qibing/disk_t/Pt204/RawData/Beacon-93/Pt204_93_radius_hist.txt")
x_array = data[:, 0]
y_array_2gauss = data[:, 1]

# print(x, y)

popt_2gauss, pcov_2gauss = scipy.optimize.curve_fit(_2gaussian, x_array, y_array_2gauss)

perr_2gauss = np.sqrt(np.diag(pcov_2gauss))

pars_1 = popt_2gauss[0:3]
pars_2 = popt_2gauss[3:6]
gauss_peak_1 = _1gaussian(x_array, *pars_1)
gauss_peak_2 = _1gaussian(x_array, *pars_2)            

fig = plt.figure(figsize=(16,6))
gs = gridspec.GridSpec(1,2)
ax1 = fig.add_subplot(gs[0])

ax1.plot(x_array, y_array_2gauss)
ax1.plot(x_array, _2gaussian(x_array, *popt_2gauss), 'k--')

# peak 1
# ax1.plot(x_array, gauss_peak_1, "g")
ax1.fill_between(x_array, gauss_peak_1.min(), gauss_peak_1, alpha=0.5, label = "{0:.2f}".format(popt_2gauss[0]) + " {0:.2f}".format(popt_2gauss[1]) + " {0:.2f}".format(popt_2gauss[2]))

# peak 2
# ax1.plot(x_array, gauss_peak_2, "y")
ax1.fill_between(x_array, gauss_peak_2.min(), gauss_peak_2, alpha=0.5, label = "{0:.2f}".format(popt_2gauss[3]) + " {0:.2f}".format(popt_2gauss[4]) + " {0:.2f}".format(popt_2gauss[5]))
    

ax1.set_xlim(0,8)
ax1.set_ylim(0,)

ax1.set_xlabel("radius",family="serif",  fontsize=12)
ax1.set_ylabel("Num of white points",family="serif",  fontsize=12)

ax1.legend(loc="best")

fig.tight_layout()
plt.show()
fig.savefig("fit2Gaussian_peaks.png", format="png",dpi=1000)
