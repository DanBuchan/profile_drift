import random
import sys
import numpy as np

print('Usage, python3 random_k_distcode.py num_of_strings length_of_strings alphabet_size distance output_file starting_string_file')
print('')
print('Number of arguments:', len(sys.argv), 'arguments.')
print('Argument List:', str(sys.argv))

if len(sys.argv)!=7:
    print('Incorrect number of arguments')
    print('Usage, random_k_distcode.py number_of_strings length_of_strings alphabet_size distance output_file starting_string_file')


strings = list()
hash    = list()

k=int(sys.argv[4])

n=int(sys.argv[1])#number of strings
m=int(sys.argv[2])#length of strings
alp_size=int(sys.argv[3])#alphabet size
output=sys.argv[5]

alph = ['A', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'K', 'L', 'M', 'N', 'P', 'Q', 'R', 'S', 'T', 'V', 'W', 'Y']

start = sys.argv[6]

file = open(sys.argv[6])
curr_string = np.array(list(file.read()))
count = 0

if len(curr_string)!=m:
    print("length_of_strings and starting string length do not match.")

for char in alph:
    curr_string[curr_string==char] = int(count)
    count = count + 1
curr_string=curr_string.astype('int32')

while(True):
    for x in range(n):
        pos_to_change = random.sample(range(0, m), k)
        replacements = random.sample(range(0, alp_size), k)

        while (sum(curr_string[pos_to_change] == replacements) > 0):
            replacements = random.sample(range(0, alp_size), k)

        curr_string[pos_to_change] = replacements
        strings.append(list(curr_string))
        hash.append(curr_string.tobytes())

    unique = set(hash)
    if (len(unique) == len(strings)):
        break

final_array = np.array(strings, dtype='U13')
for x in range(alp_size):
    final_array = np.where(final_array==str(x), alph[x], final_array)

np.savetxt(output, final_array, fmt='%s', delimiter='')