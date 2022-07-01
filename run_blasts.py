
# 4. scrub through dist file to find all the seed to member distances
# 5. calcualte average distance from seed to members for each iteration,
#    both for the whole set and for just the new ones
# 6. Output CSV of iteration members
# 7. Output the distance stats

import glob
import sys
import re
import subprocess
from collections import defaultdict


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
        count+=1
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
                                seen.append(result.groups()[0])
                            #print(result.groups()[0])

    with open(output, "w") as fhout:
        for iteration in results.keys():
            for hit in results[iteration]:
                fhout.write(f'{iteration},{hit}\n')

# argv[1]: file to turn in to blast debug
# argv[2]: seed seq to search with
# argv[3]: number of iterations of seasrch
# argv[4]: output file for iteration membership
build_blast_db(sys.argv[1])
do_blast_iterations(sys.argv[1], sys.argv[2], sys.argv[3])
parse_blast_hits(sys.argv[4])
