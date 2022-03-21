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

## TODO

1. Double check distance matrix generation is working
2. Add check so that `--distance` is not greater than the length of the sequence (hamming) or bigger than can be achieved given a distance matrix (length*max_residue_distance)
3. Add flag to build data set by random walk (current) or depth direct traversal
