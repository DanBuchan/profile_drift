import csv
import sys
from collections import defaultdict
import statistics
'''
python calculate_drift_types.py iteration_summary.csv
'''

input_file = sys.argv[1]
drift_data = defaultdict(lambda: defaultdict(list))
with open(input_file, "r") as fh:
    driftreader = csv.reader(fh, delimiter=",")
    next(driftreader)
    for row in driftreader:
        # print(row)
        drift_data[row[1]][row[2]].append(row[3:])

family_count = 0 # TOTAL NUMBER OF FAMILIES WITH DRIFT
family_hits_sizes = [] # list of the number of drift families in each blast run
purified_lost_query = 0
purified_total_lost_hit = 0

for family in drift_data:
    family_count += 1
    families_set = set() #The total set of families we've seen in this blast run
    previous_iteration_set = defaultdict(int) # set of families from the prior iteration
    for iteration in sorted(drift_data[family]):
        iteration_set = defaultdict(int) # The set of families we've seen in this iteration
        iteration_set_peaks = defaultdict(int) # The set of families we've seen in this iteration
        iteration_set_nadirs = defaultdict(int) # The set of families we've seen in this iteration
        for matches in drift_data[family][iteration]:
            families_set.add(matches[0])
            iteration_set[matches[0]] += int(matches[1])
        # do some min and max tests

        if family not in iteration_set:
            purified_lost_query += 1
            break
        if (family in iteration_set) and (len(previous_iteration_set.keys()) < len(iteration_set.keys())):
            purified_total_lost_hit += 0
        previous_iteration_set = iteration_set


    family_hits_sizes.append(len(families_set))

print(f"Mean families found: {statistics.mean(family_hits_sizes)}")
print(f"SD families found: {statistics.stdev(family_hits_sizes)}")
print("---")
print(f"Purifying Selection: LOST QUERY: {purified_lost_query}")
print(f"Purifying Selection: TOTALLY MISSING HIT: {purified_total_lost_hit}")
