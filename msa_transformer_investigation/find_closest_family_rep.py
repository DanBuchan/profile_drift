import sys
import csv
from collections import defaultdict

"""
python find_closest_family_rep.py ../iteration_summary.csv ~/Data/pfam/Pfam-A.full.uniprot
"""

def parse_pfam_alignments(pfam_aligns, drift_families):
    nr_list = set()
    for family in drift_families:
         nr_list.add(family)
         for item in drift_families[family]:
             nr_list.add(item)

    with open(pfam_aligns, "r") as fh:
        align_name = ''
        msa = defaultdict(list)
        for line in fh:
            if line.startswith("//"):
                continue
            if line.startswith("# STOCKHOLM"):
                if align_count != 0:
                    if align_name in nr_list:
                        print(f"Printing: {align_name}")
                        with open(f"{align_name}.fa") as fhOut:
                            for line in msa[align_name]:
                                fhOut.write(f">{line[0]}\n")
                                fhOut.write(f"{line[1]}\n")             
                else:
                    align_count+=1
                align_name = ''
                msa = defaultdict(list)
            if line.startswith("#=GF AC   "):
                align_name = line[10:].rstrip()
                align_name = align_name.split(".", 1)[0]
            if not line.startswith("#"):
                entries = line.split()
                seq_data = (entries[0], remove_insertions(entries[1]))
                msa[align_name].append(seq_data)
        print(f"Printing: {align_name}")
        with open(f"{align_name}.fa") as fhOut:
            for line in msa[align_name]:
                fhOut.write(f">{line[0]}\n")
                fhOut.write(f"{line[1]}\n")

    with open("famiies_list.txt") as fhOut:
        for entry in nr_list:
            fhOut.write(f'nr_list\n')
        


def read_drifts(file):
    drift_families = defaultdict(set)
    with open(file, "r") as fhIn:
        iteration_reader = csv.reader(fhIn, delimiter=",")
        for row in iteration_reader:
            drift_families[row[1]].add(row[3])
    return drift_families

drift_families = read_drifts(sys.argv[1])

# if thing doesn't exist
parse_pfam_alignments(sys.argv[2], drift_families)
