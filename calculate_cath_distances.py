'''
We calculate the NW alignment with MUSCLE then the distance
calculation with RAxML. Stretcher is 10x quicker than biopython align.globaldx

python calculate_distance.py FASTAFILE OUTPUTFILE
'''

import subprocess
import sys
import os
import numpy as np
from collections import defaultdict
from time import time
from multiprocessing import Pool, Array
import itertools


def select_string(seqlist):
    length = 1000000
    ave = sum(map(len, seqlist)) / len(seqlist)
    selected = ''
    for seq in seqlist:
        if abs(len(seq)-ave) < length:
            length = abs(len(seq)-ave)
            selected = seq
    return(seq)

def execute_process(executable_args):
    try:
        print(' '.join(executable_args))
        code = subprocess.call(' '.join(executable_args), shell=True)
    except Exception as e:
        print(str(e))
        sys.exit(1)
    if code != 0:
        print("Non Zero Exit status: "+str(code))
        print(' '.join(executable_args))
        raise OSError("Non Zero Exit status: "+str(code))
def process_distances(data):

    rep_seqs = []
    for h_family in sequences:
        h_file = f'{h_family}.fa'
        align_file = f'{h_family}.afa'
        dist_file = f'{h_family}.dist'
        fhOut = open(h_file, "w")
        rep_seqs.append(select_string(sequences[h_family]))
        if len(sequences[h_family]) == 0:
            continue
        for i, seq in enumerate(sequences[h_family]):
            fhOut.write(f'>{i}\n')
            fhOut.write(f'{seq}\n')
        fhOut.close()
        if i > 0:
            pass
            #RUN MUSCLE
            muscle_args = ['/home/dbuchan/Applications/MUSCLE/muscle5.1.linux_intel64',
                              '-super5', # or -align
                              h_file,
                              '-output',
                              align_file]
            execute_process(muscle_args)
            # run raxml
            raxml_args = ['/home/dbuchan/Applications/standard-RAxML/raxmlHPC-MPI-SSE3',
                          '-s',
                          align_file,
                          '-n',
                          dist_file,
                          '-m',
                          'PROTGAMMABLOSUM62',
                          '-N'
                          '2',
                          '-p',
                          '123',
                          '-f',
                          'x']
            execute_process(raxml_args)
            #tidy up
            os.remove(h_file)
            os.remove(align_file)
            os.remove(align_file+".reduced")
            os.remove(f'RAxML_info.{h_family}.dist')
            os.remove(f'RAxML_parsimonyTree.{h_family}.dist.RUN.0')
        # exit()

    rep_file = 'reps.fa'
    align_file = 'reps.afa'
    dist_file = 'reps.dist'
    fhOut = open(rep_file, "w")
    for i, seq in enumerate(rep_seqs):
        fhOut.write(f'>{i}\n')
        fhOut.write(f'{seq}\n')
    fhOut.close()
    muscle_args = ['/home/dbuchan/Applications/MUSCLE/muscle5.1.linux_intel64',
                   '-super5', # or -align
                   rep_file,
                   '-output',
                   align_file]
    execute_process(muscle_args)
    # run raxml
    raxml_args = ['/home/dbuchan/Applications/standard-RAxML/raxmlHPC-MPI-SSE3',
                  '-s',
                  align_file,
                  '-n',
                  dist_file,
                  '-m',
                  'PROTGAMMABLOSUM62',
                  '-N'
                  '2',
                  '-p',
                  '123',
                  '-f',
                  'x']
    execute_process(raxml_args)
    #tidy up
    os.remove(rep_file)
    os.remove(align_file)
    os.remove(align_file+".reduced")
    os.remove(f'RAxML_info.rep.dist')
    os.remove(f'RAxML_parsimonyTree.rep.dist.RUN.0')



input_file = sys.argv[1]

results = None
sequences = defaultdict(list)
hfamily = ''
with open(input_file) as fh:
    for line in fh:
        line = line.rstrip()
        if line.startswith(">"):
            entries = line.split("|")
            hfamily = entries[3]
        else:
            sequences[hfamily].append(line)

process_distances(sequences)

with open(sys.argv[2], "w", encoding="utf-8") as fhOut:
    fhOut.write("prot1,prot2,distance\n")
    for set in results:
        for r in set:
            fhOut.write(f'{r[0]},{r[1]},{r[2]}\n')
