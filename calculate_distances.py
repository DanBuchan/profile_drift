'''
We calculate the NW alignment with EMBOSS stretcher and then the pairwise2
distance with biopython. Stretcher is 10x quicker than biopython align.globaldx
and biopython DistanceCalculator is about 10x quicker than EMBOSS distmat

python calculate_distance.py FASTAFILE OUTPUTFILE
'''
import subprocess
import sys
import os
from time import time
from Bio.Phylo.TreeConstruction import DistanceCalculator
from Bio import AlignIO

fasta_data = {}
with open(sys.argv[1], encoding="utf-8", mode="r") as fafile:
    name = ''
    for line in fafile:
        if line.startswith(">"):
            entries = line.split(";")
            name = entries[0][1:]
        else:
            fasta_data[name] = line.rstrip()

stretcher_args = ['/home/dbuchan/Applications/EMBOSS-6.6.0/emboss/stretcher',
                  '-asequence',
                  'tmpA.fa',
                  '-bsequence',
                  'tmpB.fa',
                  '-aformat',
                  'fasta',
                  '-outfile',
                  'stretch_tmp.fa']

fhOut = open(sys.argv[2], "w", encoding="utf-8")
fhOut.write("prot1,prot2,distance\n")
for name in fasta_data:
    for name2 in fasta_data:
        if name == name2:
            continue
        # start = time()
        with open('tmpA.fa', "w", encoding="utf-8") as outfh:
            outfh.write(f'>{name}\n')
            outfh.write(f'{fasta_data[name]}\n')
        with open('tmpB.fa', "w", encoding="utf-8") as outfh:
            outfh.write(f'>{name2}\n')
            outfh.write(f'{fasta_data[name2]}\n')
        try:
            code = subprocess.call(' '.join(stretcher_args), shell=True)
        except Exception as e:
            print(str(e))
            sys.exit(1)
        if code != 0:
            print("Non Zero Exit status: "+str(code))
            raise OSError("Non Zero Exit status: "+str(code))
        #align_time = time()

        aln = AlignIO.read('stretch_tmp.fa', 'fasta')
        calculator = DistanceCalculator('blosum62')
        dm = calculator.get_distance(aln)
        # print(dm)
        distance = dm[0][1]
        # distance_time = time()
        # print("Timings: ", align_time-start, distance_time-align_time)
        fhOut.write(f'{name},{name2},{distance}\n')

fhOut.close()
os.remove("tmpA.fa")
os.remove("tmpB.fa")
os.remove("stretch_tmp.fa")
