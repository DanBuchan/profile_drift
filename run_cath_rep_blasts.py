from collections import defaultdict
import subprocess
# 1. open domseqs fasta. read in and select 1 rep per
# 2. run blast vs the dom-seqs for each rep

def read_pseudo_reps(dom_seqs):
    """
    read the domain seqs and pull out a random rep for each. Not really caring
    about the cath assigned rep as that's somewhat arbitrary anyway
    """
    reps = defaultdict(dict)
    rep_id = ''
    h_family = ''
    with open(dom_seqs, "r") as fhIn:
        for line in fhIn:
            if line.startswith(">"):
                line = line.rstrip()
                h_family = line.rstrip().split("|")[3]
                rep_id = line[12:19]

            else:
                seq = line.rstrip()
                reps[h_family] = {rep_id: seq}
    return reps

def do_blast_iterations(fasta_file, seed_seq, n):
    in_file = f'{seed_seq}.fa'
    first_iteration_args = ['/home/dbuchan/Applications/ncbi-blast-2.12.0+/bin/psiblast',
                            '-query',
                            in_file,
                            '-num_iterations',
                            '1',
                            '-db',
                            fasta_file,
                            '-out_pssm',
                            f'{seed_seq}_iteration1.pssm',
                            '-out',
                            f'{seed_seq}_iteration1.bls',
                            '-save_pssm_after_last_round',
                            '-max_target_seqs',
                            '10000']
    subprocess.call(first_iteration_args)
    for i in range(2, int(n)+1):
        iteration_args = ['/home/dbuchan/Applications/ncbi-blast-2.12.0+/bin/psiblast',
                                '-in_pssm',
                                f'{seed_seq}_iteration{i-1}.pssm',
                                '-num_iterations',
                                '1',
                                '-db',
                                fasta_file,
                                '-out_pssm',
                                f'{seed_seq}_iteration{i}.pssm',
                                '-out',
                                f'{seed_seq}_iteration{i}.bls',
                                '-save_pssm_after_last_round',
                                '-max_target_seqs',
                                '10000']
        subprocess.call(iteration_args)

def run_blasts(reps, dom_seqs):
    """
    run psiblast over each rep against the cath dom seqs db
    """
    for h_family in reps:
        for rep_id in reps[h_family]:
            fhRep = open(f'{rep_id}.fa', "w")
            fhRep.write(f">{rep_id}|{h_family}\n")
            fhRep.write(f"{reps[h_family][rep_id]}\n")
            fhRep.close()
            do_blast_iterations(dom_seqs, rep_id, 20)

dom_seqs = '/home/dbuchan/Projects/profile_drift/RAxML_distances/cath_blast_growth_experiment/blast_data/cath-domain-seqs-S100.fa.annotated'

reps = read_pseudo_reps(dom_seqs)
run_blasts(reps, dom_seqs)
