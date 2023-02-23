import csv
import sys
from collections import defaultdict
import statistics
import pickle
import os


'''
python calculate_drift_types.py iteration_summary.csv /home/dbuchan/Data/pfam/pfam_fasta.fa
'''


def count_alignments(file):
    size_lookup = defaultdict(int)
    with open(file, "r") as fh:
        for line in fh:
            if line.startswith(">"):
                line = line.rstrip()
                entries = line.split("|")
                size_lookup[entries[1]] += 1
    return size_lookup


input_file = sys.argv[1]
alignment_file = sys.argv[2]

if (os.path.exists("pfam_family_size.p")):
    size_lookup = pickle.load(open("pfam_family_size.p", "rb"))
else:
    size_lookup = count_alignments(alignment_file)
    pickle.dump(size_lookup, open("pfam_family_size.p", "wb"))

drift_data = defaultdict(lambda: defaultdict(list))
with open(input_file, "r") as fh:
    driftreader = csv.reader(fh, delimiter=",")
    next(driftreader)
    for row in driftreader:
        # print(row)
        drift_data[row[1]][int(row[2])].append(row[3:])

family_count = 0  # TOTAL NUMBER OF FAMILIES WITH DRIFT
family_hits_sizes = []  # list of the number of drift families in each blast
purified_lost_query = 0
purified_total_lost_hit = 0
multiple_families = 0
non_growing_contaminants = 0

for family in drift_data:
    family_count += 1
    families_set = set()  # The fullset of families seen in this blast run
    final_set = None # set of families in the final iteration
    last_seen_iteration = {} # last iteration we see a family in
    previous_iteration_set = defaultdict(int)  # set of families from the prior
    # iteration
    iteration_set_peaks = defaultdict(int)  # The set of families we've
    # seen in this iteration
    iteration_set_nadirs = defaultdict(int)  # The set of families we've
    # seen in this iteration
    iteration_set_starts = defaultdict(int)  # The set of families we've
    # seen in this iteration
    iteration_set_stops = defaultdict(int)  # The set of families we've
    # seen in this iteration
    final_iteration = 0
    for iteration in sorted(drift_data[family]):
        final_iteration = iteration
        iteration_set = defaultdict(int)  # The set of families we've seen in
        # this iteration

        for matches in drift_data[family][iteration]:
            families_set.add(matches[0])
            iteration_set[matches[0]] += int(matches[1])
        # do some min and max tests

        # we now have iteration set which are all the matches seen in a run.
        # loop through the matches again and see when they arrive and go

        contaminant_iteration = 0
        final_set = set()
        for matches in drift_data[family][iteration]:
            hit_family = matches[0]
            num_hits = int(matches[1])
            last_seen_iteration[hit_family] = iteration
            final_set.add(hit_family)
            if iteration == 1:
                iteration_set_peaks[hit_family] = 0
                iteration_set_nadirs[hit_family] = num_hits
            if hit_family not in iteration_set_starts.keys():
                iteration_set_starts[hit_family] = num_hits
                iteration_set_stops[hit_family] = num_hits

            iteration_set_stops[hit_family] = num_hits

            if num_hits > iteration_set_peaks[hit_family]:
                iteration_set_peaks[hit_family] = num_hits
            if num_hits < iteration_set_nadirs[hit_family]:
                iteration_set_nadirs[hit_family] = num_hits

    
        if family not in iteration_set:
            purified_lost_query += 1
            break
        if (family in iteration_set) and (len(previous_iteration_set.keys())
           < len(iteration_set.keys())):
            purified_total_lost_hit += 0
        previous_iteration_set = iteration_set

    for hit_family in families_set:
        if hit_family not in final_set:
            iteration_set_stops[hit_family] = 0

    print("family", family)
    print("Peak", iteration_set_peaks)
    print("Lowest", iteration_set_nadirs)
    print("First value", iteration_set_starts)
    print("Final value", iteration_set_stops)
    print("Last seen iter", last_seen_iteration)
    for hit_family in families_set:
        ten_percent_of_peak = iteration_set_peaks[hit_family]/10
        if hit_family == family:
            if iteration_set_peaks[hit_family] \
               > iteration_set_starts[hit_family]+ten_percent_of_peak:
                # accumulated querey
                pass
            if iteration_set_stops[hit_family] \
               < iteration_set_peaks[hit_family]*0.8:
                # spiked querey
                pass
            if iteration_set_stops[hit_family] \
               < iteration_set_peaks[hit_family]*0.2:
                # query purified out
                pass     
        else:
            if iteration_set_peaks[hit_family] \
               > iteration_set_starts[hit_family]+ten_percent_of_peak:
                # accumulated hit
                pass
            if iteration_set_peaks[hit_family] \
               > iteration_set_stops[hit_family]*0.8:
                # spiked hit
                pass
            if iteration_set_stops[hit_family]*2 \
               < iteration_set_peaks[hit_family]*0.2:
                # hit purified out
                pass

    number_families_at_end = 0
    small_non_growing_contaminant = 0
    for hit_family in iteration_set_stops:
        if iteration_set_stops[family] < 0:
            number_families_at_end += 1
        if hit_family != family:
            if iteration_set_starts[hit_family] <= iteration_set_peaks[family]*0.1 and iteration_set_stops[hit_family] <= iteration_set_peaks[family]*0.1:
                small_non_growing_contaminant += 0
    
    if small_non_growing_contaminant > 0:
        non_growing_contaminants += 1
    if number_families_at_end > 2:
        multiple_families += 1
        
    exit()
    family_hits_sizes.append(len(families_set))

print(f"Mean families found: {statistics.mean(family_hits_sizes)}")
print(f"SD families found: {statistics.stdev(family_hits_sizes)}")
print("---")
print(f"Purifying Selection: LOST QUERY: {purified_lost_query}")
print(f"Purifying Selection: TOTALLY MISSING HIT: {purified_total_lost_hit}")
print(f"Count with Non growing contaminants: {non_growing_contaminants}")
print(f"Count with multiple contaminants: {multiple_families}")