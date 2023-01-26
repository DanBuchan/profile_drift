import sys
import Bio
import glob
from collections import defaultdict
# Usage
# python calculate_cath_drift.py ./cath_distances/REPS/reps.fa ./cath_distances/REPS/RAxML_distances.reps.dist /home/dbuchan/Projects/profile_drift/RAxML_distances/cath_blast_growth_experiment/rep_blasts

def read_reps(file):
    reps_lookup = {}
    with open(file, "r") as fh:
        for line in fh:
            if line.startswith(">"):
                # print(line[1:])
                entries = line[1:].split()
                reps_lookup[entries[0]] = entries[1]
    return reps_lookup

def read_distances(lookup, file):
    dists_lookup = defaultdict(dict)
    with open(file, "r") as fh:
        for line in fh:
            entries = line.split()
            dists_lookup[lookup[entries[0]]][lookup[entries[1]]] = entries[2]
            # do this in the other direction to make the lookup symmetric (not fully needed)
            dists_lookup[lookup[entries[1]]][lookup[entries[0]]] = entries[2]
    return dists_lookup

def parse_blast_results(distances, blast_data_dir):
    for rep in distances:
        print(f'{blast_data_dir}{rep}*.bls')
        for file in glob.glob(f'{blast_data_dir}{rep}*.bls'):
            print(file)
        exit()

reps_file = sys.argv[1]
dist_file = sys.argv[2]
blast_data_dir = sys.argv[3]
lookup = read_reps(reps_file)
distances = read_distances(lookup, dist_file)
parse_blast_results(distances, blast_data_dir)
