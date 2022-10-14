import glob
import sys

dir = sys.argv[1]

dist_list = glob.glob(f'{dir}*.dist')
for file in dist_list:
    with open(file, "r") as fh:
        comparision_count = 0
        total = 0
        for line in fh:
            line = line.rstrip()
            entries = line.split()
            comparision_count += 1
            total += float(entries[2])
        print(f'{file[17:]},{total/comparision_count}')
