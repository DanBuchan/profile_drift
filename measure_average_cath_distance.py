'''
python measure_average_cath_distance.py ~/Data/cath/cath-domain-seqs-S100.fa cath-domain-list-S100.txt 50
'''
import sys
import os
from collections import defaultdict
import random
import subprocess
from Bio.Phylo.TreeConstruction import DistanceCalculator
from Bio import AlignIO

def read_cath_assignments(file):
    assignments = {}
    with open(file, "r", encoding="utf-8") as fhIn:
        for line in fhIn:
            entries = line.split()
            assignments[entries[0]] = f'{entries[1]}.{entries[2]}.{entries[3]}.{entries[4]}'
    return assignments


def read_cath_data(file, membership):
    families = defaultdict(list)
    sequences = defaultdict(str)
    with open(file, "r", encoding="utf-8") as fhFasta:
        domainid = ''
        for line in fhFasta:
            if line.startswith(">"):
                entries = line.split("|")
                domainid = entries[2][:7]
            else:
                sequences[domainid]+=line.rstrip()
    for domainid in sequences:
        if domainid in membership:
            families[membership[domainid]].append(sequences[domainid])
    return families


def calculate_average_distances(fasta_data, size):
    sample_set = random.sample(fasta_data.keys(), size)
    tmpa = "tmpA.fa"
    tmpb = "tmpB.fa"
    tmpstretch = 'stretch_tmp.fa'
    fhOut = open('average_cath_family_distances.csv', "w", encoding="utf-8")
    fhOut.write("hfamily,comparision_number,total_distance,average_distance\n")
    for h_family in sample_set:
        comparison_count = 0
        total_distance = 0
        for n, seqA in enumerate(fasta_data[h_family]):
            with open(tmpa, "w", encoding="utf-8") as outfh:
                outfh.write(f'>{n}A\n')
                outfh.write(seqA)
            for m, seqB in enumerate(fasta_data[h_family]):
                if m == n:
                    continue
                comparison_count += 1
                with open(tmpb, "w", encoding="utf-8") as outfh:
                    outfh.write(f'>{m}B\n')
                    outfh.write(seqB)
                stretcher_args = ['/home/dbuchan/Applications/EMBOSS-6.6.0/emboss/stretcher',
                             '-asequence',
                             tmpa,
                             '-bsequence',
                             tmpb,
                             '-aformat',
                             'fasta',
                             '-outfile',
                             tmpstretch]
                try:
                    code = subprocess.call(' '.join(stretcher_args), shell=True)
                except Exception as e:
                    print(str(e))
                    sys.exit(1)
                if code != 0:
                    print("Non Zero Exit status: "+str(code))
                    print(' '.join(stretcher_args))
                    raise OSError("Non Zero Exit status: "+str(code))
                aln = AlignIO.read(tmpstretch, 'fasta')
                calculator = DistanceCalculator('blosum62')
                dm = calculator.get_distance(aln)
                distance = dm[0][1]
                # print(seqA)
                # print(seqB)
                # print(distance)
                total_distance += distance
        if comparison_count > 0:
            ave = total_distance/comparison_count
            fhOut.write(f'{h_family},{comparison_count},{total_distance},{ave}\n')
    os.remove(tmpa)
    if os.path.exists(tmpb):
        os.remove(tmpb)
    if os.path.exists(tmpstretch):
        os.remove(tmpstretch)
    fhOut.close()

input_fasta = sys.argv[1]
cath_list = sys.argv[2]
sample_size = int(sys.argv[3])

cath_assignments = read_cath_assignments(cath_list)
# print(cath_assignments)
fasta_data = read_cath_data(input_fasta, cath_assignments)
calculate_average_distances(fasta_data, sample_size)
