from collections import defaultdict
import subprocess
from multiprocessing.pool import ThreadPool
import sys
# 1. open domseqs fasta. read in and select 1 rep per
# 2. run blast vs the dom-seqs for each rep

def read_reps(dom_seqs):
    """
    read the domain seqs and pull out a random rep for each. Not really caring
    about the cath assigned rep as that's somewhat arbitrary anyway
    """
    reps = defaultdict(dict)
    rep_id = ''
    family = ''
    with open(dom_seqs, "r") as fhIn:
        for line in fhIn:
            if line.startswith(">"):
                line = line.rstrip()
                entries = line.split("|")
                family = entries[1]
                rep_id = entries[0].split("/")[0][1:]
            else:
                seq = line.rstrip()
                reps[family] = {rep_id: seq}
    return reps

def do_blast_iterations(id, blast_db, n):
    in_file = f'{id}.fa'
    first_iteration_args = ['/home/ucbcdwb/Applications/ncbi-blast-2.12.0+/bin/psiblast',
                            '-query',
                            in_file,
                            '-num_iterations',
                            '1',
                            '-db',
                            blast_db,
                            '-out_pssm',
                            f'{id}_iteration1.pssm',
                            '-out',
                            f'{id}_iteration1.bls',
                            '-save_pssm_after_last_round',
                            '-max_target_seqs',
                            '10000']
    subprocess.call(first_iteration_args)
    for i in range(2, int(n)+1):
        iteration_args = ['/home/ucbcdwb/Applications/ncbi-blast-2.12.0+/bin/psiblast',
                                '-in_pssm',
                                f'{id}_iteration{i-1}.pssm',
                                '-num_iterations',
                                '1',
                                '-db',
                                blast_db,
                                '-out_pssm',
                                f'{id}_iteration{i}.pssm',
                                '-out',
                                f'{id}_iteration{i}.bls',
                                '-save_pssm_after_last_round',
                                '-max_target_seqs',
                                '10000']
        subprocess.call(iteration_args)


def run_blasts(family, id, seq, blast_db):
    """
    run psiblast over each rep against the cath dom seqs db
    """
    fhRep = open(f'{id}.fa', "w")
    fhRep.write(f">{id}|{family}\n")
    fhRep.write(f"{seq}\n")
    fhRep.close()
    do_blast_iterations(id, blast_db, 20)

#dom_seqs = '/home/dbuchan/Projects/profile_drift/RAxML_distances/cath_blast_growth_experiment/blast_data/cath-domain-seqs-S100.fa.annotated'
rep_seqs = sys.argv[1]
blast_db = sys.argv[2]
seq_index = None
try:
    seq_index = sys.argv[3]-1
except:
    pass

reps = read_reps(rep_seqs)
tp = ThreadPool(1)
if seq_index:
    family = list(reps)[seq_index]
    id = list(reps[family].keys())[0]
    apply_async(run_blasts, (family, id, reps[family][id], blast_db, ))
    tp.close()
    tp.join()
    exit()
else:
    for family in reps:
        id = list(reps[family].keys())[0]
        apply_async(run_blasts, (family, id, reps[family][id], blast_db, ))
        tp.close()
        tp.join()
        exit()
tp.close()
tp.join()
