import ruptures as rpt
import matplotlib.pyplot as plt
from matplotlib import gridspec
import numpy as np

from scipy.signal import argrelmax
from scipy.signal import find_peaks

from scipy.ndimage.filters import gaussian_filter1d


dir = "/home/dbuchan/Projects/profile_drift/RAxML_distances/drift_experiment/"
file = "average_distances10_23cluster_103cluster.csv"
path = dir+file

series = np.genfromtxt(path, delimiter=',', skip_header=True)
signal = series[:, 2]
# signal = np.reshape(signal,(-1,1))

# # detection
# use dynamic programming, downside you have to pre-soecify how many breaks
# you're looking for
# And break predictions see to lag the change
# algo = rpt.Dynp(model="rbf", min_size=0).fit(signal)
# result = algo.predict(n_bkps=3)
# print(result)
# # display
# rpt.display(signal, [], result)
# plt.show()

# Pruned Exact Linear Time
# when penalty value is low we get more boundaries
# l1 and l2 models find the right number of boundaries
# algo = rpt.Pelt(model="rbf", min_size=0).fit(signal)
# result = algo.predict(pen=1)
# print(result)
# # display
# rpt.display(signal, [], result)
# plt.show()

# [4, 7, 12]
# cf = changefinder.ChangeFinder(r=0.01, order=3, smooth=3)
# ts_score = [cf.update(p) for p in signal]
#
# plt.plot(signal)
# plt.plot(ts_score)
# plt.show()

# from scipy.signal import savgol_filter
# https://stackoverflow.com/questions/47519626/using-numpy-scipy-to-identify-slope-changes-in-digital-signals
# window = 11
# der2 = savgol_filter(signal, window_length=window, polyorder=3, deriv=3)
# max_der2 = np.max(np.abs(der2))
# large = np.where(np.abs(der2) > max_der2/2)[0]
# gaps = np.diff(large) > window
# begins = np.insert(large[1:][gaps], 0, large[0])
# ends = np.append(large[:-1][gaps], large[-1])
# changes = ((begins+ends)/2).astype(np.int)
# plt.plot(signal)
# plt.plot(changes, signal[changes], 'ro')
# plt.show()

fig = plt.figure(figsize=(8,12))
gs = gridspec.GridSpec(5, 1)

ax0 = plt.subplot(gs[0])
ax0.set_title('Iteration Counts')
ax0.plot(signal)

signal_1stdev = np.gradient(signal)
ax1 = plt.subplot(gs[1])
ax1.set_title('1st derivative')
ax1.plot(signal_1stdev)

signal_2nddev = np.gradient(signal_1stdev)
ax2 = plt.subplot(gs[2])
ax2.set_title('2nd derivative')
ax2.plot(signal_2nddev)

signal_2nddev_clipped = np.clip(np.abs(np.gradient(signal_2nddev)), 0, 15)
ax3 = plt.subplot(gs[3])
ax3.set_title('absolute value + clipping')
ax3.plot(signal_2nddev_clipped)

smoothed_signal = gaussian_filter1d(signal_2nddev_clipped, 1)
ax4 = plt.subplot(gs[4])
ax4.set_title('Smoothing applied')
ax4.plot(smoothed_signal)

plt.tight_layout()
# plt.show()

#max_idx = argrelmax(smoothed_signal, order=3)[0]
max_idx, _ = find_peaks(smoothed_signal, height=10)

print(max_idx)
fig, ax = plt.subplots()
ax.plot(signal)
ax.scatter(max_idx, signal[max_idx], marker='x', color='red')
plt.show()
