import csv
import sys
from collections import defaultdict

"""
python hmmer_seq_generator.py ../iteration_summary.csv
"""

def read_drifts(file):
    drift_families = defaultdict(set)
    with open(file, "r") as fhIn:
        next(fhIn)
        iteration_reader = csv.reader(fhIn, delimiter=",")
        for row in iteration_reader:
            drift_families[row[1]].add(row[3])
    return drift_families


def make_drift_set_non_redundant(drift_families):
    families = set()
    for key, hit_set in drift_families.items():
        families.add(key)
        families.update(hit_set)
    return(families)


drift_families = read_drifts(sys.argv[1])
nr_drift_set = make_drift_set_non_redundant(drift_families)

# skim through Pfam-A.hmm and retrieve everything in nr_drift_set
# cat to one file then run
# ./hmmemit -N 200 ~/Data/pfam/test.hmm