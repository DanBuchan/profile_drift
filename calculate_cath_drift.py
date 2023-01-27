import sys
import Bio
import glob
import re
import csv
from os.path import exists
from collections import defaultdict
# Usage
# python calculate_cath_drift.py ./cath_distances/REPS/reps.fa ./cath_distances/REPS/RAxML_distances.reps.dist /home/dbuchan/Data/cath/cath-domain-seqs-S100.fa.annotated /home/dbuchan/Projects/profile_drift/RAxML_distances/cath_blast_growth_experiment/rep_blasts


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


def read_blast_db(file):
    h_family_membership = {}
    with open(file, "r") as fh:
        for line in fh:
            if line.startswith(">"):
                entries = line.rstrip().split("|")
                domain = entries[2].split("/")
                h_family_membership[domain[0]] = entries[3]
    return(h_family_membership)


def parse_blast_results(distances, h_family_membership, blast_data_dir):
    fileOut = "parsed_blast_rep_iteration_data.csv"
    fhOut = open(fileOut, "w")
    fhOut.write("QueryRep,RepHFamily,Iteration,HitID,HitHFamily\n")
    for i, rep in enumerate(distances):
        # print(f'{blast_data_dir}/{rep}*.bls')
        print(f'{i} {h_family_membership[rep]}')
        file_list = []
        for file in glob.glob(f'{blast_data_dir}/{rep}*.bls'):
            parts = file.split("iteration")
            # print(parts[1][:-4])
            iteration = int(parts[1][:-4])
            file_list.insert(iteration-1, file)
        for i, file in enumerate(file_list):
            # print(file)
            hits = parse_blast_data(rep, file)
            for rep in hits:
                for hit in hits[rep]:
                    fhOut.write(f'{rep},{h_family_membership[rep]},{i+1},{hit},{h_family_membership[hit]}\n')
#        exit()
    fhOut.close()


def parse_blast_data(rep, file):
    results = defaultdict(list)
    seen = []
    result_list_pattern = re.compile(r"^(.+?)\s+(.+?)\s+(.+?)\n")
    count = 0

    count += 1
    read = False
    with open(file, "r") as fh:
        for line in fh:
            # print(line)
            if line.startswith('Sequences producing significant'):
                 read = True
                 continue
            if line.startswith('>'):
                read = False
                continue
            if read:
                result = re.match(result_list_pattern, line)
                if result:
                    if float(result.groups()[2]) < 1e-5:
                        name_entries = result.groups()[0].split("|")
                        domain_entries = name_entries[2].split("/")
                        if domain_entries[0] not in seen:
                            results[rep].append(domain_entries[0])
                            seen.append(domain_entries[0])
    return results

def read_parsed_data(data_file):
    with open("parsed_blast_rep_iteration_data.csv", "r") as fhIn:
        hitreader = csv.reader(fhIn, delimiter=',',)
        for row in hitreader:
            print(', '.join(row))

def process_blast_data(distances, blast_data):
    pass

reps_file = sys.argv[1]
dist_file = sys.argv[2]
blast_db_file = sys.argv[3]
blast_data_dir = sys.argv[4]
blast_data = None
if exists("parsed_blast_rep_iteration_data.csv"):
    print("hello")
    blast_data = read_parsed_data("parsed_blast_rep_iteration_data.csv")
    exit()
    distances = read_distances(lookup, dist_file)
else:
    lookup = read_reps(reps_file)
    distances = read_distances(lookup, dist_file)
    h_family_membership = read_blast_db(blast_db_file)
    parse_blast_results(distances, h_family_membership, blast_data_dir)
    blast_data = read_parsed_data()

# process_blast_data(distances, blast_data)
