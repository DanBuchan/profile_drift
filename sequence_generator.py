'''
In which we generate random equidistant protein strings
'''
import argparse
import random
import numpy as np
import csv


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
    '''Output a fasta file of the strings we generated'''
    string_count = 0
    with open(file, "w", encoding="utf-8") as fh_out:
        for protein in proteins:
            working_string = np.array(protein[0], dtype='U13')
            for y in range(alphabet_size):
                working_string = np.where(working_string == str(y), alph[y],
                                          working_string)
            fh_out.write(f'>{string_count}; approx_dist: {protein[1]}\n')
            fh_out.write(f'{"".join(working_string)}\n')
            string_count += 1


def check_positive(value):
    '''Function checks a value is positive'''
    ivalue = int(value)
    if ivalue <= 0:
        raise argparse.ArgumentTypeError(f'{value} must be positive')
    return ivalue


def read_distance_matrix():
    '''Read in the blosum csv from the data dir'''
    blosum_matrix = []
    with open('./data/blosum62.csv', "r", encoding="utf-8") as fh_bl:
        blosumreader = csv.reader(fh_bl, delimiter=",")
        for line in blosumreader:
            blosum_matrix.append(line[1:])
    return blosum_matrix


parser = argparse.ArgumentParser(description='Generate a sets of (approx)'
                                 'equi-spaced proteins',
                                 prog='sequence_generator.py',
                                 usage='\n%(prog)s --num_strings INT '
                                 '--distance INT '
                                 '--matrix_distance'
                                 '--output_file STRING '
                                 '--starting_string_file STRING')
parser.add_argument('--num_strings', help="Number of protein string to "
                    "generate", required=True, type=check_positive)
parser.add_argument('--distance', help="distance apart for each generated "
                    "string", required=True, type=check_positive)
parser.add_argument('--matrix_distance', help="Toggle whether distances are"
                    "calculated from a dist matrix of as the raw number of"
                    "substitutions", action="store_true")
parser.add_argument('--output_file', help="Name of output file", required=True)
parser.add_argument('--starting_string_file', help="Name of input file",
                    required=True)
args = parser.parse_args()

strings = []
hashed = []
if args.matrix_distance:
    DIST_MATRIX = read_distance_matrix()
alph = ['A', 'R', 'N', 'D', 'C', 'Q', 'E', 'G', 'H', 'I', 'L', 'K', 'M', 'F',
        'P', 'S', 'T', 'W', 'Y', 'V']

alphabet_size = len(alph)
curr_string = read_seq(args.starting_string_file)
length_of_strings = len(curr_string)
count = 0

for char in alph:
    curr_string[curr_string == char] = int(count)
    count = count + 1
curr_string = curr_string.astype('int32')
accumulated_dist = 0
# here we keep track of how many steps/moves we're making at each iteration
# so we can report that in the fasta header on output
while True:
    for x in range(args.num_strings):
        accumulated_dist += args.distance
        pos_to_change = random.sample(range(0, length_of_strings),
                                      args.distance)
        if args.matrix_distance:
            exit("DISTANCE MATRIX NOT YET IMPLMENTED")
        else:
            replacements = random.sample(range(0, alphabet_size),
                                         args.distance)
        while sum(curr_string[pos_to_change] == replacements) > 0:
            replacements = random.sample(range(0, alphabet_size),
                                         args.distance)

        curr_string[pos_to_change] = replacements
        strings.append([list(curr_string), accumulated_dist])
        hashed.append(curr_string.tobytes())

    unique = set(hashed)
    if len(unique) == len(strings):
        break

output_strings(args.output_file, strings)
