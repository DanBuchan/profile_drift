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

a) python sequence_generator.py --num_string 10000 --distance 2 --random_pathing 20 --output_file test.fa --starting_string_file data/test_file_150.fa

#### relabel_headers.py

small script will renumber generated fasta headers so no two are the same

#### Iterate_walk.py

Will run sequence generator in sequence if you want to run it once and then use the final seq as a
seed in a new run

### RAxML

/home/dbuchan/Applications/standard-RAxML/raxmlHPC-PTHREADS-AVX -T 6 -s full_db.afa -n full_db.dist -m PROTGAMMABLOSUM62 -N2 -p 123 -f x > stdout 2> stderr

single core execution:
100x100 took 2 seconds

1000x1000 took 1:40 mins
10000x10000 took 98mins
100000x1000000 took 6 and a half days


## CATH DISTANCES

Some scripts for calculating the average distance between cath h family members and between cath H families (about 1.6 and 11 respectively)

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

### run_blasts.py

Given a fasta file and a set of RAxML distances this script runs n iterations of blast and compiles
the results.

### plot_average_blast_growth.R

Plots the average distance at each iteration of the blasts in run_blasts.py

## EXPERIMENTS

### Distance experiment

How and at what rate are sequences recruited to profiles given a db density? We run this with both hhblits and psiblast to compare to common profile based search methods

#### Distance_experiment.sh

Script runs the seq generator, calculates distances and then runs serial blasts and compiles the stats

### Drift experiment

Take the dbs we created in distance experiment. From the seed sequence pick a first sequence n steps away then another n steps away and so on. So each of those generate 500 sequences that are 1 step apart (a denser region). Then make paired databases with the first pick and the ones further and further away. Rerun the run_blasts.py and plot the results and see what happens.

### create_family.py

Take a fa file, read it's distance matrix. Take First seq 1000 (away from the start), then take seqs at 2000, 3000 etc... but skip 10,000. Generate 500 sequences at step 1 from these. Then create databases that cat first family, nth family and the parent fa file

## TODO

1. Add check so that `--distance` is not greater than the length of the sequence (hamming) or bigger than can be achieved given a distance matrix (length*max_residue_distance)
