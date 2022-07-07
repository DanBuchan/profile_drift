import glob
import sys
import re
import subprocess
import os
from collections import defaultdict

'''
Usage: python ../../../run_blasts.py ../random_pathing_test.fa ../../../data/test_file_150.fa 5 random_membership.csv ../RAxML_distances.full_db.dist average_distances.csv
'''

def build_blast_db(fasta_file):
    makeblastdbargs = ['/home/dbuchan/Applications/ncbi-blast-2.12.0+/bin/makeblastdb',
                       '-in',
                       fasta_file,
                       '-dbtype',
                       'prot']
    subprocess.call(makeblastdbargs)


def do_blast_iterations(fasta_file, seed_seq, n):
    first_iteration_args = ['/home/dbuchan/Applications/ncbi-blast-2.12.0+/bin/psiblast',
                            '-query',
                            seed_seq,
                            '-num_iterations',
                            '1',
                            '-db',
                            fasta_file,
                            '-out_pssm',
                            'iteration1.pssm',
                            '-out',
                            'iteration1.bls',
                            '-save_pssm_after_last_round']
    subprocess.call(first_iteration_args)
    for i in range(2, int(n)+1):
        iteration_args = ['/home/dbuchan/Applications/ncbi-blast-2.12.0+/bin/psiblast',
                                '-in_pssm',
                                f'iteration{i-1}.pssm',
                                '-num_iterations',
                                '1',
                                '-db',
                                fasta_file,
                                '-out_pssm',
                                f'iteration{i}.pssm',
                                '-out',
                                f'iteration{i}.bls',
                                '-save_pssm_after_last_round']
        subprocess.call(iteration_args)

def parse_blast_hits(output):
    results = defaultdict(list)
    seen = []
    result_list_pattern = re.compile(r"^(.+?)\s+(.+?)\s+(.+?)\n")
    count = 0
    for file in glob.glob(f'*.bls'):
        print(file)
        count += 1
        read = False
        with open(file, "r") as fh:
            for line in fh:
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
                            if result.groups()[0] not in seen:
                                results[count].append(result.groups()[0])
                                seen.append(int(result.groups()[0]))
                            #print(result.groups()[0])

    with open(output, "w") as fhout:
        for iteration in results.keys():
            for hit in results[iteration]:
                fhout.write(f'{iteration},{hit}\n')
    return results


def get_distances(hits, distances):
    dist_results = defaultdict(dict)
    fhdist = open(distances, "r")
    for iteration in hits.keys():
        for matchID in hits[iteration]:
            fhdist.seek(0)
            for line in fhdist:
                line = line.rstrip()
                entries = line.split()
                if int(entries[0]) != 1:
                    break
                if matchID == entries[1]:
                    dist_results[iteration][matchID] = float(entries[2])
                    continue
    return dist_results


def calculate_distances(distances, output):
    results = defaultdict(int)
    for iteration in distances:
        for match in distances[iteration]:
            results[iteration] += distances[iteration][match]
        results[iteration] = results[iteration]/len(distances[iteration].keys())

    with open(output, "w") as fhout:
        fhout.write('iteration,ave_distance\n')
        for iteration in results:
            fhout.write(f'{iteration},{results[iteration]}\n')

# argv[1]: file to turn in to blast debug
# argv[2]: seed seq to search with
# argv[3]: number of iterations of seasrch
# argv[4]: output file for iteration membership
# argv[5]: file of all the RAxML distances
# argv[6]: output csv

build_blast_db(sys.argv[1])
do_blast_iterations(sys.argv[1], sys.argv[2], sys.argv[3])
blast_hits = parse_blast_hits(sys.argv[4])
distances = get_distances(blast_hits, sys.argv[5])
calculate_distances(distances, sys.argv[6])
