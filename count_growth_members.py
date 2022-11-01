import os
import glob
import re
from collections import defaultdict

experiment_dir = "/home/dbuchan/Projects/profile_drift/RAxML_distances/drift_experiment/"

def read_fa_file(file):
    numbers = re.findall(r'\d+', file)
    mapping = {numbers[1]: 'first',
               numbers[2]: 'second'}
    members = {}
    with open(file, "r") as fh:
        for line in fh:
            if line.startswith(">"):
                # print(line)
                id = line[1:-1]
                # print(id)
                if "_" in id:
                    bits = id.split("_")
                    members[id] = mapping[bits[1]]
                else:
                    members[id] = 'background'
    exit
    return members


for root, dir, stuff, in os.walk(experiment_dir):
    for d in dir:
        if d.startswith("distance50") or d.startswith("distance50") :
            print(d)
        else:
            continue

        fa = d+".fa"
        iteration_members = {}
        if os.path.isfile(fa):
            # print(fa)
            fa_members = read_fa_file(fa);
            # print(fa_members)
            for file in glob.glob(experiment_dir+d+"/*.bls"):
                paths = file.split("/")
                iteration = re.findall(r'\d+', paths[8])
                # print(file)
                # print(iteration[0])
                parse_toggle = False
                with open(file, "r") as fh:
                    membership = defaultdict(list)
                    for line in fh:
                        if line.startswith("Sequences producing significant"):
                            parse_toggle = True
                            continue
                        if line.startswith(">"):
                            parse_toggle = False
                            continue
                        if parse_toggle:
                            entries = line.split()
                            if len(entries) > 0:
                                membership[fa_members[entries[0]]].append(entries[0])
                    iteration_members[int(iteration[0])] = membership
        print(fa[:-2]+"membercount")
        with open(fa[:-2]+"membercount", "w") as fh:
            fh.write("iteration,background,first,second\n")
            for iteration in sorted(iteration_members):
                background = len(iteration_members[iteration]["background"])
                first = len(iteration_members[iteration]["first"])
                second = len(iteration_members[iteration]["second"])
                fh.write(f"{iteration},{background},{first},{second}\n")
