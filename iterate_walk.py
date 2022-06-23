import subprocess
import os

# python3 sequence_generator.py --num_string 200 --distance 2 --output_file initial_dist_2_200_strings.fa --starting_string_file data/test_file_150.fa

def run_over_targets(fa_list, number, file_stub):
    new_targets = []
    dist = 2
    string_num = 200
    for j, fasta in enumerate(fa_list):
        header = ''
        seq = ''
        fhtmp = open('tmp.fasta', "w")
        with open(fasta, "r") as fh:
            for line in fh:
                if line.startswith(">"):
                    header = line
                else:
                    seq = line
        fhtmp.write(header)
        fhtmp.write(seq)
        fhtmp.close()

        for i in range(0, number):
            seq_args = ['python3',
                        'sequence_generator.py',
                        '--num_string',
                        str(string_num),
                        '--distance',
                        str(dist),
                        '--output_file',
                        f'{file_stub}_idx_{j}_{i}_dist_{dist}_num_{string_num}.fa',
                        '--starting_string_file',
                        'tmp.fasta']
            new_targets.append(f'{file_stub}_idx_{j}_{i}_dist_{dist}_num_{string_num}.fa')
            subprocess.call(seq_args)

        os.remove('tmp.fasta')
    return(new_targets)


target_list = ['data/test_file_150.fa']
target_list = run_over_targets(target_list, 4, 'initial')
target_list = run_over_targets(target_list, 4, 'second')
target_list = run_over_targets(target_list, 4, 'third')
