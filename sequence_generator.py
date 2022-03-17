'''
In which we generate random equidistant protein strings
'''
import argparse
import random
import numpy as np


def read_seq(file):
    '''Read in a protein sequence and handle it if it is a fasta file'''
    seq = ''
    with open(file, "r", encoding="utf-8") as fh_in:
        for line in fh_in:
            if line.startswith(">"):
                continue
            seq += line.rstrip()
    return(np.array(list(seq)))


def output_strings(file, proteins):
    '''Output a fasta file of the string we generated'''
    string_count = 0
    with open(file, "w", encoding="utf-8") as fh_out:
        for protein in proteins:
            fh_out.write(f'>{string_count}\n')
            fh_out.write(f'{"".join(protein)}\n')
            string_count += 1


def check_positive(value):
    '''Function checks a value is positive'''
    ivalue = int(value)
    if ivalue <= 0:
        raise argparse.ArgumentTypeError(f'{value} must be positive')
    return ivalue


parser = argparse.ArgumentParser(description='Generate a sets of (approx)'
                                 'equi-spaced proteins',
                                 prog='sequence_generator.py',
                                 usage='\n%(prog)s --num_strings INT '
                                 '--alphabet_size INT '
                                 '--distance INT '
                                 '--output_file STRING '
                                 '--starting_string_file STRING')
parser.add_argument('--num_strings', help="Number of protein string to "
                    "generate", required=True, type=check_positive)
parser.add_argument('--alphabet_size', help="Size of...", required=True,
                    type=check_positive)
parser.add_argument('--distance', help="distance apart for each generated "
                    "string", required=True, type=check_positive)
parser.add_argument('--output_file', help="Name of output file", required=True)
parser.add_argument('--starting_string_file', help="Name of input file",
                    required=True)
args = parser.parse_args()

strings = []
hashed = []

alph = ['A', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'K', 'L', 'M', 'N', 'P', 'Q',
        'R', 'S', 'T', 'V', 'W', 'Y']

curr_string = read_seq(args.starting_string_file)
length_of_strings = len(curr_string)
count = 0

for char in alph:
    curr_string[curr_string == char] = int(count)
    count = count + 1
curr_string = curr_string.astype('int32')

while True:
    for x in range(args.num_strings):
        pos_to_change = random.sample(range(0, length_of_strings),
                                      args.distance)
        replacements = random.sample(range(0, args.alphabet_size),
                                     args.distance)

        while sum(curr_string[pos_to_change] == replacements) > 0:
            replacements = random.sample(range(0, args.alphabet_size),
                                         args.distance)

        curr_string[pos_to_change] = replacements
        strings.append(list(curr_string))
        hashed.append(curr_string.tobytes())

    unique = set(hashed)
    if len(unique) == len(strings):
        break

final_array = np.array(strings, dtype='U13')
for x in range(args.alphabet_size):
    final_array = np.where(final_array == str(x), alph[x], final_array)

output_strings(args.output_file, final_array)
