# Some code to study the nature of profile drift in sequence search

## Code

### sequence_generator.py

Script that takes a seed sequence and generates an artificial database
of protein sequences where each sequence is some fixed distance from its parent.

Current it just random walks from each generated sequence and ensures it doesn't
generate a sequence it has seen before. Distance is just the raw substitution
distance (like a hamming distance).

Options:

* --num_strings : The number of proteins to generate
* --distance : The distance between each string in the random walk
* --output_file : Name of a fasta file to put the protein strings in
* --starting_string_file : Seed string to start. All strings will be the same size as the seed string
* --matrix_distance : flag to toggle if the distance should be interpreted as a substitution distance or a value from a distance matrix

#### matrix_distance

If you set the matrix_distance flag then you must provide a distance value that is
meaningful for the distance matrix you provide. By default `data/` contains the blosum62 matrix but you can replace this with any distance matrix in the same format. The amino acids MUST be in the ordering as provided: `A, R, N, D, C, Q, E, G, H, I, L, K, M, F, P, S, T, W, Y, V`. Extra symbols can be included at the end but will be ignored. A header line must be included.

Worth noting that when matrix distance is FALSE then it is equivalent to using a distance matrix where all, off-diagonal, distances are equivalent to -1

#### Example

```
python3 sequence_generator.py --num_string 10 --distance 1 --output_file output.fa --starting_string_file test_file.fa
```

### Building datasets of 10,000


```
python3 sequence_generator.py --num_string 1000 --walk_number 10 --distance 5 --output_file output.fa --starting_string_file test_file.fa
```

### calculate_distances.py

OBSOLETE: Script takes a fasta file, calculates all NW pairwise global alignments (EMBOSS stretcher). Then calculates the Kimura corrected evolutionary distance (EMBOSS distmat). Outputs a pairwise distance list.

This simply takes WAY TOO LONG

### RAxML

/home/dbuchan/Applications/standard-RAxML/raxmlHPC-MPI-SSE3 -s ../output_100_substitution.fa -n 100_distances.txt -m PROTGAMMABLOSUM62 -N 2 -p 123 -f x > time.out 2> time.err &

single core execution:
100x100 took 2 seconds
1000x1000 took 1:40 mins
10000x10000 took 98mins
100000x1000000 took 6 and a half days

### measure_average_cath_distance.py

File that takes the cath h family fasta file. Takes a sample of H families and
works out the average Kimura corrected evolutionary distance between each family member

### average_martix_distance.py

handy script that returns the average, off diagonal, distance in a distance matrix

### visualise_distance.R

Small R script to take a distance csv and visualise it use MDS

https://stackoverflow.com/questions/3081066/what-techniques-exists-in-r-to-visualize-a-distance-matrix

## Testing distance from seq to cluster "centroid"

If we have the distances in the distance file then we can just take the average of all the distances to the query seq.

## TODO

1. Add check so that `--distance` is not greater than the length of the sequence (hamming) or bigger than can be achieved given a distance matrix (length*max_residue_distance)
