import sys
import subprocess
# 1. Read fa file
# 2. saved 1000th and x000th seqs up to 9000th
# 3. for each of those generate 500 sequences at set 1
# 4. cat fa and 1000th and nth families in to seperate database

def read_fasta(file):
    seeds = {}
    getseq = False
    name = ''
    seq = ''
    with open(file, "r") as fh:
        for line in fh:
            if line.startswith(">"):
                name = int(line.rstrip()[1:])
                if name % 500 == 0 and name < 10000:
                    getseq = True
                else:
                    getseq = False
            else:
                if getseq:
                    seeds[name] = line.rstrip()
    return seeds

def generate_families(seeds, file_stub):
    for seq in seeds:
        with open(f'{file_stub}_{seq}_seed.fa', "w") as fh:
            fh.write(f'>{seq}\n')
            fh.write(f'{seeds[seq]}\n')

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
                        f'{file_stub}_{seq}cluster.fa',
                        '--starting_string_file',
                        f'{file_stub}_{seq}_seed.fa']
        subprocess.call(seq_gen_args)

    for seq in seeds:
        for seq2 in seeds:
            if seq == seq2:
                continue
            with open(f'{file_stub}_{seq}cluster_{seq2}cluster.fa', 'w') as outfile:
                with open(f'{file_stub}.fa') as infile:
                    outfile.write(infile.read())
                for name in [seq, seq2]:
                    with open(f'{file_stub}_{name}cluster.fa') as infile:
                        for line in infile:
                            if line.startswith(">"):
                                line = line.rstrip()
                                outfile.write(f'{line}_{name}\n')
                            else:
                                outfile.write(line)
        break

# sys.argv[1] : input fa file
# sys.argv[2] : background distance, used for file naming
seed_seqs = read_fasta(sys.argv[1])
generate_families(seed_seqs, sys.argv[2])
