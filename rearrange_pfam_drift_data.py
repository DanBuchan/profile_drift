import sys
"""
python rearrange_pfam_drift_data.py /home/dbuchan/Data/pfam/reps_renumbered.fasta.fa parsed_pfam_iteration_data.csv
"""

def get_lookup(reps):
    lookup = {}
    with open(reps, "r") as fh:
        for line in fh:
            if line.startswith(">"):
                line = line.rstrip()
                entries = line.split("|")
                lookup[entries[1].split("/")[0]] = entries[2]
    return lookup

rep_file = sys.argv[1]
summary_file = sys.argv[2]

rep_lookup = get_lookup(rep_file)

print("rep,rep_family,iteration,hit_family,hit_count")
with open(summary_file, "r") as fh:
    for line in fh:
        line = line.rstrip()
        entries = line.split("|")
        header = entries.pop(0)
        rep = header.split(",")
        for entry in entries:
            entry = entry[:-1]
            iter_data = entry.split(",")
            iteration = iter_data.pop(0)
            for pair in  [iter_data[i:i + 2] for i in range(0, len(iter_data), 2)]:
                print(f"{rep[0]},{rep_lookup[rep[0]]},{iteration},{pair[0]},{pair[1]}")
