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

### Building datasets of num_strings

average in h family distance in CATH is 1.6
avaerage between family distance in cath is 11

a) sequence_generator.py --num_string 200 --walk_number 5 --distance 2 --output_file initial_dist_2_200_strings_5_walks_total_1000.fa --starting_string_file data/test_file_150.fa

b) iterate_walk.py

run seq generator multiple times over n walks and for each ouput file take the last seq and so it again

c) cat together all the sub files

d) relabel fa headers

relabel_headers.py full_db.afa > relabelled.afa

### calculate_distances.py

OBSOLETE: Script takes a fasta file, calculates all NW pairwise global alignments (EMBOSS stretcher). Then calculates the Kimura corrected evolutionary distance (EMBOSS distmat). Outputs a pairwise distance list.

This simply takes WAY TOO LONG

### RAxML

/home/dbuchan/Applications/standard-RAxML/raxmlHPC-PTHREADS-AVX -T 6 -s full_db.afa -n full_db.dist -m PROTGAMMABLOSUM62 -N2 -p 123 -f x > stdout 2> stderr

single core execution:
100x100 took 2 seconds

1000x1000 took 1:40 mins
10000x10000 took 98mins
100000x1000000 took 6 and a half days

## CATH DISTANCES

### calculate_cath_distances.py

Takes an annotated CATH seqs file uses mafft to build alignments of each and then runs RAxML to work out the distances. Produces .dist files in the cath_distances dir

### average_cath_distances.py

takes the distances from the above and spits out the average in-h-family distances
and the average distance between reps. Produces average_cath_distances.csv

### average_martix_distance.py

handy script that returns the average, off diagonal, distance in a distance matrix

### plot_average_cath_distances.R

take the average_cath_distances.csv and average the average distance and plot a nice histogram.

## GENERAL DISTANCES

### visualise_distance.R

Small R script to take a distance csv and visualise it use MDS

https://stackoverflow.com/questions/3081066/what-techniques-exists-in-r-to-visualize-a-distance-matrix

## Testing distance from seq to cluster "centroid"

If we have the distances in the distance file then we can just take the average of all the distances to the query seq.

## Blast

~/Applications/ncbi-blast-2.12.0+/bin/makeblastdb -in full_relabelled.affa -dbtype prot

### Iteration 1
~/Applications/ncbi-blast-2.12.0+/bin/psiblast -query ../../../data/test_file_150.fa -num_iterations 1 -db full_relabelled.affa -out_pssm iteration1.pssm -out iteration1.bls -save_pssm_after_last_round
### Iteration 2
~/Applications/ncbi-blast-2.12.0+/bin/psiblast -in_pssm iteration1.pssm -num_iterations 1 -db full_relabelled.affa -out_pssm iteration2.pssm -out iteration2.bls -save_pssm_after_last_round
### Iteration 3
~/Applications/ncbi-blast-2.12.0+/bin/psiblast -in_pssm iteration2.pssm -num_iterations 1 -db full_relabelled.affa -out_pssm iteration3.pssm -out iteration3.bls -save_pssm_after_last_round
### Iteration 3
~/Applications/ncbi-blast-2.12.0+/bin/psiblast -in_pssm iteration3.pssm -num_iterations 1 -db full_relabelled.affa -out_pssm iteration4.pssm -out iteration4.bls -save_pssm_after_last_round

parse_blast_hits.py

take a set of .bls files and parse the homologues for each iteration.

## TODO

1. Add check so that `--distance` is not greater than the length of the sequence (hamming) or bigger than can be achieved given a distance matrix (length*max_residue_distance)
