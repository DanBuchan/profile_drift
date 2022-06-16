'''
We calculate the NW alignment with MUSCLE then the distance
calculation with RAxML. Stretcher is 10x quicker than biopython align.globaldx

python calculate_distance.py FASTAFILE
'''

import subprocess
from subprocess import Popen, PIPE
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

def execute_process(executable_args, stdout_location=None):
    try:
        print(' '.join(executable_args))
        p = Popen(executable_args, stdin=PIPE, stdout=PIPE, stderr=PIPE)
        output, err = p.communicate()
        code = p.returncode
    except Exception as e:
        print(str(e))
        sys.exit(1)
    if code != 0:
        print("Non Zero Exit status: "+str(code))
        print("Command:"+' '.join(executable_args))
        if code != 255:
            raise OSError("Non Zero Exit status: "+str(code)+output.decode('utf-8'))
    if stdout_location:
        fhalign = open(stdout_location, "w")
        fhalign.write(output.decode("utf-8") )
        fhalign.close()

def process_distances(data):

    rep_seqs = []
    for h_family in sequences:
        # if '1.10.168.10' not in h_family:
        #     continue
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
            mafft_args = ['/usr/local/bin/mafft',
                           h_file]
            execute_process(mafft_args, align_file)
            # run raxml
            raxml_args = ['/home/dbuchan/Applications/standard-RAxML/raxmlHPC-PTHREADS-AVX',
                          '-T',
                          '4',
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
            #exit()
            #tidy up
            try:
                os.remove(h_file)
            except:
                pass
            try:
                os.remove(align_file)
            except:
                pass
            try:
                os.remove(align_file+".reduced")
            except:
                pass
            try:
                os.remove(f'RAxML_info.{h_family}.dist')
            except:
                pass
            try:
                os.remove(f'RAxML_parsimonyTree.{h_family}.dist.RUN.0')
            except:
                pass
            # exit()

    rep_file = 'reps.fa'
    align_file = 'reps.afa'
    dist_file = 'reps.dist'
    fhOut = open(rep_file, "w")
    for i, seq in enumerate(rep_seqs):
        fhOut.write(f'>{i}\n')
        fhOut.write(f'{seq}\n')
    fhOut.close()
    mafft_args = ['/usr/local/bin/mafft',
                   rep_file]
    execute_process(mafft_args, align_file)
    # run raxml
    raxml_args = ['/home/dbuchan/Applications/standard-RAxML/raxmlHPC-PTHREADS-AVX',
                  '-T',
                  '4',
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
    try:
        os.remove(rep_file)
    except:
        pass
    try:
        os.remove(align_file)
    except:
        pass
    try:
        os.remove(align_file+".reduced")
    except:
        pass
    try:
        os.remove(f'RAxML_info.rep.dist')
    except:
        pass
    try:
        os.remove(f'RAxML_parsimonyTree.rep.dist.RUN.0')
    except:
        pass



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
