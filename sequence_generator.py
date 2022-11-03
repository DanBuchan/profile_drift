'''
In which we generate random equidistant protein strings
'''
import argparse
import random
import csv
import copy
import numpy as np


def read_seq(file):
    '''Read in a protein sequence and handle it if it is a fasta file'''
    seq = ''
    with open(file, "r", encoding="utf-8") as fh_in:
        for line in fh_in:
            if line.startswith(">"):
                continue
            seq += line.rstrip()
    return(np.array(list(seq), dtype=object))


def output_strings(file, proteins):
    '''Output a fasta file of the strings we generated'''
    step = 1
    with open(file, "w", encoding="utf-8") as fh_out:
        for protein in proteins:
            working_string = np.array(protein, dtype='U13')
            for y in range(alphabet_size):
                working_string = np.where(working_string == str(y), alph[y],
                                          working_string)
            fh_out.write(f'>{step}\n')
            fh_out.write(f'{"".join(working_string)}\n')
            step += 1


def check_positive(value):
    '''Function checks a value is positive'''
    ivalue = int(value)
    if ivalue <= 0:
        raise argparse.ArgumentTypeError(f'{value} must be positive')
    return ivalue


def read_distance_matrix():
    '''Read in the blosum csv from the data dir'''
    blosum_matrix = []
    with open('../../matrices/blosum62.csv', "r", encoding="utf-8") as fh_bl:
        blosumreader = csv.reader(fh_bl, delimiter=",")
        next(blosumreader)
        for line in blosumreader:
            blosum_matrix.append(list(map(float, line[1:])))
    return blosum_matrix


def generate_mat_dist_string(length, distance):
    '''Creates a randomised list of possible changes and a list of replacements
    counts them up until the distance score has been reached and returns that
    subset'''
    change_list = random.sample(range(0, length), length) # The residue
                                                          # position to change
    replace_list = random.choices(range(0, alphabet_size), k=length)
    # the change to make

    changes = []
    replacing = []
    score = 0
    print(change_list, replace_list)
    for i, entity in enumerate(change_list):
        source = curr_string[entity]
        replacement = replace_list[i]
        if DIST_MATRIX[source][replacement] < 0:
            score += abs(DIST_MATRIX[source][replacement])
            changes.append(entity)
            replacing.append(replace_list[i])
        if score >= distance:
            break
    return changes, replacing


def generate_prob_dist_string(length, distance, string_copy):
    '''Creates a randomised list of possible changes and selects the changes
    based on the distance matrix as though it were a probability '''
    changes = []
    replacing = []
    replace_list = []
    change_list = random.sample(range(0, length), length)
    for aa in string_copy:
        selection = random.choices(range(0, alphabet_size),
                                   weights=PROB_MATRIX[aa][:20],
                                   k=1)
        replace_list.append(selection[0])
    score = 0
    # print(change_list, replace_list)
    for i, entity in enumerate(change_list):
        source = curr_string[entity]
        replacement = replace_list[i]

        score += -DIST_MATRIX[source][replacement]
        changes.append(entity)
        replacing.append(replace_list[i])

        if score >= distance:
            break
    # print(changes, replacing)
    return changes, replacing


def prob_transform_matrix():
    '''
    Take a distance matrix and convert the propensities to probabilities
    '''
    new_mat = []
    for row in DIST_MATRIX:
        row_replacement = [x+abs(min(row))+1 for x in row]
        row_replacement = [x/sum(row_replacement) for x in row_replacement]
        new_mat.append(row_replacement)
    return(new_mat)


parser = argparse.ArgumentParser(description='Generate a sets of (approx)'
                                 'equi-spaced proteins',
                                 prog='sequence_generator.py',
                                 usage='\n%(prog)s --num_strings INT '
                                 '--distance INT '
                                 '--matrix_distance '
                                 '--output_file STRING '
                                 '--starting_string_file STRING')
parser.add_argument('--num_strings', help="Number of protein string to "
                    "generate", required=True, type=check_positive)
parser.add_argument('--distance', help="distance apart for each generated "
                    "string", required=True, type=check_positive)
parser.add_argument('--matrix_distance', help="Toggle whether distances are"
                    "calculated from a dist matrix of as the raw number of"
                    "substitutions", action="store_true")
parser.add_argument('--probability_selection', help="when selecting a "
                    "substitution draw it from the distance matrix as though"
                    " it were a probability distribution", action="store_true")
parser.add_argument('--breadth_traversal', help="Toggle whether the sequences"
                    "are generated as a single random walk or a set of "
                    "n fanning out walks. Value is the number of sequences to "
                    "fork off at each iteration", default=1,
                    type=check_positive)
parser.add_argument('--random_pathing', help="new sequences are generated by"
                    "picking at random [with replacement] one of the sequences"
                    "from the previous iterations. A picked sequence is removed"
                    "from the set of possible progenitors, so the generation is"
                    "forced to move away from the seed. Incompatible with"
                    "--breadth_traversal > 1. And incompatible with"
                    "--walk_number > 1.", default=None, type=check_positive)
parser.add_argument('--walk_number', help="Number of times to initiate a walk "
                    "from the initial seed sequence. Output will be "
                    "num_strings x walk_number", default=1,
                    type=check_positive)
parser.add_argument('--output_file', help="Name of output file", required=True)
parser.add_argument('--starting_string_file', help="Name of input file",
                    required=True)
args = parser.parse_args()

if args.random_pathing and args.breadth_traversal > 1:
    print("Can't set random pathing and breadth_traversal > 1 at the same "
          "time")
    exit(1)
if args.random_pathing and args.walk_number > 1:
    print("Can't set random_pather and walk_number > 1 at the same "
          "time")
    exit(1)

if args.matrix_distance:
    DIST_MATRIX = read_distance_matrix()
if args.probability_selection:
    DIST_MATRIX = read_distance_matrix()
    PROB_MATRIX = prob_transform_matrix()

alph = ['A', 'R', 'N', 'D', 'C', 'Q', 'E', 'G', 'H', 'I', 'L', 'K', 'M', 'F',
        'P', 'S', 'T', 'W', 'Y', 'V']
alphabet_size = len(alph)
seed_sequence = read_seq(args.starting_string_file)
length_of_strings = len(seed_sequence)


# here we keep track of how many steps/moves we're making at each iteration
# so we can report that in the fasta header on output
total_strings = []
for w in range(0, args.walk_number):

    # for every walk number reset the current strong to the seed_seuence
    strings = []
    curr_string = copy.deepcopy(seed_sequence)
    for i, char in enumerate(curr_string):
        curr_string[i] = alph.index(char)
    curr_string = curr_string.astype('int32')
    seed_strings = [curr_string]
    new_strings = []
    selected_strings = []
    while True:
        # print(len(strings))
        iter_strings = copy.deepcopy(seed_strings)
        if args.random_pathing:
            iter_strings = random.choices(seed_strings, k=args.random_pathing)
        for curr_string in iter_strings:
            for i in range(0, args.breadth_traversal):
                if args.matrix_distance:
                    pos_to_change, replacements = generate_mat_dist_string(
                                                  length_of_strings,
                                                  args.distance)
                elif args.probability_selection:
                    pos_to_change, replacements = generate_prob_dist_string(
                                                  length_of_strings,
                                                  args.distance,
                                                  copy.deepcopy(curr_string))
                else:
                    pos_to_change = random.sample(range(0, length_of_strings),
                                                  args.distance)
                    replacements = random.choices(range(0, alphabet_size),
                                                 k=args.distance)
                    # while sum(curr_string[pos_to_change] == replacements) > 0:
                    #     replacements = random.choices(range(0, alphabet_size),
                    #                                  k=args.distance)
                curr_string[pos_to_change] = replacements
                new_strings.append(curr_string)
                if list(curr_string) not in strings:
                    strings.append(list(curr_string))
                if len(strings) >= args.num_strings:
                    break
        for string in new_strings:
            seed_strings.append(string)
        for string in iter_strings:
            if string in seed_strings:
                seed_strings.remove(string)
        new_strings = []

        if len(strings) >= args.num_strings:
            break
    for string in strings:
        total_strings.append(string)

output_strings(args.output_file, total_strings)
