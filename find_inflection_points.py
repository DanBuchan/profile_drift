import glob
import csv
import re
import itertools
import numpy as np
from scipy.signal import argrelmax
from scipy.signal import find_peaks
from scipy.ndimage.filters import gaussian_filter1d
from itertools import product


dir = "/home/dbuchan/Projects/profile_drift/RAxML_distances/drift_experiment/members/*.membercount"
drift_dir = "/home/dbuchan/Projects/profile_drift/RAxML_distances/drift_experiment/"
files = glob.glob(dir)

for file in files:
    cluster_1_first_elbow_found = False
    cluster_2_first_elbow_found = False
    cluster_2_second_elbow_found = False
    parts = re.findall(r'\d+', file)
    print(int(parts[0]), int(parts[1]), int(parts[2]))
    elbows = []
    with open(file, "r", encoding="utf-8") as csvfile:

        member_reader = csv.reader(csvfile, delimiter=",")
        next(member_reader)
        clus_1_previous = 0
        clus_2_previous = 0
        for count, row in enumerate(member_reader):
            # print(count, row)
            if count == 0:
                clus_1_previous = int(row[2])
                clus_2_previous = int(row[3])
            else:
                diff_clus_1 = int(row[2])-clus_1_previous
                diff_clus_2 = int(row[3])-clus_2_previous
                if diff_clus_1 == 0 and cluster_1_first_elbow_found == False:
                    cluster_1_first_elbow_found = True
                    elbows.append(count)
                if diff_clus_2 > 0 and cluster_1_first_elbow_found == True and cluster_2_first_elbow_found == False:
                    cluster_2_first_elbow_found = True
                    elbows.append(count)
                if diff_clus_2 == 0 and cluster_2_first_elbow_found == True and cluster_2_second_elbow_found == False:
                    cluster_2_second_elbow_found = True
                    elbows.append(count)
                clus_1_previous = int(row[2])
                clus_2_previous = int(row[3])
        print(elbows)
    ave_file = f"average_distances{parts[0]}_{parts[1]}cluster_{parts[2]}cluster.csv"
    series = np.genfromtxt(drift_dir+ave_file, delimiter=',', skip_header=True)
    signal = series[:, 2]
    signal_1stdev = np.gradient(signal)
    signal_2nddev = np.gradient(signal_1stdev)
    signal_2nddev_clipped = np.clip(np.abs(np.gradient(signal_2nddev)), 0, 15)
    smoothed_signal = gaussian_filter1d(signal_2nddev_clipped, 1)
    max_idx, _ = find_peaks(smoothed_signal, height=10)
    max_idx = list(max_idx)
    TP = 0
    FP = 0
    FN = 0
    if len(max_idx) != 0 and len(elbows) != 0:
        if abs(elbows[0] - max_idx[0]) <= 2:
            TP+=1
            max_idx.pop(0)
            elbows.pop(0)
    c = list(itertools.product(max_idx, elbows))
    # print(c)
    print("REMAINING", len(max_idx), len(elbows))
    if len(max_idx) != 0 and len(elbows) != 0:
        for item in elbows[:]: # make a copy of x
            for item2 in max_idx[:]:
                if abs(item-item2) <= 2:
                    elbows.remove(item)
                    max_idx.remove(item2)
                    TP+=1
                if len(elbows) == 0:
                    break
                if len(max_idx) == 0:
                    break
            if len(elbows) == 0:
                break
            if len(max_idx) == 0:
                break

    FP = len(max_idx)
    FN = len(elbows)
    print("TP,FP,FN")
    print(f"{TP},{FP},{FN}")
    #break
