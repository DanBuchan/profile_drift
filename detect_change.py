import ruptures as rpt
import matplotlib.pyplot as plt
import numpy as np
import changefinder

dir = "/home/dbuchan/Projects/profile_drift/RAxML_distances/drift_experiment/"
file = "average_distances10_23cluster_103cluster.csv"
path = dir+file

series = np.genfromtxt(path, delimiter=',', skip_header=True)
signal = series[:, 2]
signal = np.insert(signal, 0, 0)
signal = np.reshape(signal,(-1,1))
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

https://stackoverflow.com/questions/47519626/using-numpy-scipy-to-identify-slope-changes-in-digital-signals
