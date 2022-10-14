import sys
import subprocess
from collections import defaultdict
# 1. Read fa file
# 2. distanceX_membership.csv per iteration

def read_fasta(file):
    fasta = {}
    name = ''
    seq = ''
    with open(file, "r") as fh:
        for line in fh:
            if line.startswith(">"):
                name = int(line.rstrip()[1:])
            else:
                fasta[name] = line.rstrip()
    return fasta


def read_distances(fasta, distances):
    dists = defaultdict(list)
    seen = []
    with open(distances, "r") as fhdists:
        line = fhdists.readline()
        # print(line)
        for line in fhdists:
            line = line.rstrip()
            entries = line.split(",")
            if entries[1] not in seen:
                dists[int(entries[0])].append([int(entries[1]), float(entries[2])])
                seen.append(entries[1])

    seeds = []
    for iteration in range(2, 22, 2):
        # print(iteration)
        sorted_list = sorted(dists[iteration], key=lambda x: x[1])
        # print(sorted_list)
        for pair in sorted_list:
            if pair not in seeds:
                seeds.append(pair)
                break
            else:
                continue
    return(seeds)

def generate_families(seeds, fasta, file_stub):
    for seq in seeds:
        with open(f'{file_stub}_{seq[0]}_seed.fa', "w") as fh:
            fh.write(f'>{seq[0]}; distance {seq[1]}\n')
            fh.write(f'{fasta[seq[0]]}\n')

    for seq in seeds:
        seq_gen_args = ['python',
                        '/home/dbuchan/Projects/profile_drift/sequence_generator.py',
                        '--num_string',
                        '500',
                        '--distance',
                        '1',
                        '--random_pathing',
                        '20',
                        '--output_file',
                        f'{file_stub}_{seq[0]}cluster.fa',
                        '--starting_string_file',
                        f'{file_stub}_{seq[0]}_seed.fa']
        subprocess.call(seq_gen_args)

    for seq in seeds:
        for seq2 in seeds:
            if seq[0] == seq2[0]:
                continue
            with open(f'{file_stub}_{seq[0]}cluster_{seq2[0]}cluster.fa', 'w') as outfile:
                with open(f'{file_stub}.fa') as infile:
                    outfile.write(infile.read())
                for name in [seq[0], seq2[0]]:
                    with open(f'{file_stub}_{name}cluster.fa') as infile:
                        for line in infile:
                            if line.startswith(">"):
                                line = line.rstrip()
                                outfile.write(f'{line}_{name}\n')
                            else:
                                outfile.write(line)
        break

# sys.argv[1] : input fa file
# sys.argv[2] : distance info
# sys.argv[3] : background distance, used for file naming

fasta = read_fasta(sys.argv[1])
seed_seqs = read_distances(fasta, sys.argv[2])
generate_families(seed_seqs, fasta, sys.argv[3])
