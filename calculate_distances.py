'''
We calculate the NW alignment with EMBOSS stretcher and then the pairwise2
distance with biopython. Stretcher is 10x quicker than biopython align.globaldx
and biopython DistanceCalculator is about 10x quicker than EMBOSS distmat

python calculate_distance.py FASTAFILE OUTPUTFILE THREADS
'''
import subprocess
import sys
import os
import numpy as np
from time import time
from Bio.Phylo.TreeConstruction import DistanceCalculator
from Bio import AlignIO
from multiprocessing import Pool, Array
from itertools import cycle

def file_len(fname):
    '''b
    '''
    offsets = []
    offset = 0
    with open(fname, encoding="utf-8", mode="r") as f:
        for i, l in enumerate(f):
            offsets.append(offset)
            offset += len(l)
    offsets = [offsets[i:i + 2] for i in range(0, len(offsets), 2)]
    return offsets


def process_distances(data, count, file):
    print(count, file)
    tmpa = f'tmpA{count}.fa'
    tmpb = f'tmpB{count}.fa'
    tmpstretch = f'stretch_tmp{count}.fa'

    fasta_data = {}
    current_fasta_ID = None
    distance_results = []
    for pair in data:
        with open(file, encoding="utf-8", mode="r") as fafile:
            fafile.seek(pair[0])
            header = next(fafile)
            seq = next(fafile)
            parts = header.split(";")
            current_fasta_ID = parts[0][1:]
            with open(tmpa, "w", encoding="utf-8") as outfh:
                outfh.write(f'>{current_fasta_ID}\n')
                outfh.write(seq)
            fafile.seek(0)

            for line in fafile:
                if line.startswith(">"):
                    entries = line.split(";")
                    name = entries[0][1:]
                else:
                    fasta_data[name] = line.rstrip()

            stretcher_args = ['/home/dbuchan/Applications/EMBOSS-6.6.0/emboss/stretcher',
                         '-asequence',
                         tmpa,
                         '-bsequence',
                         tmpb,
                         '-aformat',
                         'fasta',
                         '-outfile',
                         tmpstretch]
            for name in fasta_data:
                if current_fasta_ID == name:
                    continue
                # start = time()
                with open(tmpb, "w", encoding="utf-8") as outfh:
                    outfh.write(f'>{name}\n')
                    outfh.write(f'{fasta_data[name]}\n')
                try:
                    code = subprocess.call(' '.join(stretcher_args), shell=True)
                except Exception as e:
                    print(str(e))
                    sys.exit(1)
                if code != 0:
                    print("Non Zero Exit status: "+str(code))
                    print(' '.join(stretcher_args))
                    raise OSError("Non Zero Exit status: "+str(code))
                #align_time = time()

                aln = AlignIO.read(tmpstretch, 'fasta')
                calculator = DistanceCalculator('blosum62')
                dm = calculator.get_distance(aln)
                # print(dm)
                distance = dm[0][1]
                # distance_time = time()
                # print("Timings: ", align_time-start, distance_time-align_time)
                distance_results.append([current_fasta_ID, name, distance])
            os.remove(tmpa)
            os.remove(tmpb)
            os.remove(tmpstretch)
    return(distance_results)

num_of_threads = int(sys.argv[3])
input_file = sys.argv[1]
line_offset = file_len(input_file)
batches = np.array_split(line_offset, num_of_threads)

results = None
with Pool(num_of_threads) as p:
    sets = list(range(0, num_of_threads))
    results = p.starmap(process_distances, zip(batches, sets,
                        cycle([input_file])))

with open(sys.argv[2], "w", encoding="utf-8") as fhOut:
    fhOut.write("prot1,prot2,distance\n")
    for set in results:
        for r in set:
            fhOut.write(f'{r[0]},{r[1]},{r[2]}\n')
