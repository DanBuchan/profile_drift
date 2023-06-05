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
* --probability_selection : when selecting a substitution draw it from the distance matrix as though it were a probability distribution

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
average between family distance in cath is 11

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

Take the dbs we created in distance experiment. Take the distanceX_membership.csv from the distance experiment and select sequences n distnace away so they are on the search path. So each of those generate 500 sequences that are 1 step apart (a denser region). Then make paired databases with the first pick and the ones further and further away. Rerun the run_blasts.py and plot the results and see what happens.

#### create_family.py

read fasta and distanceX_membership.csv. for every alternate iteration (2, 4, 6...) pick a seed sequence that is some distance from the start. This ensures all seeds are on the search path of blast. Each new seed can't be a previous seed.

For instance files are named

distance40_12_seed.fa - A seed sequences taken from the distance 40 file/db
                        and is a seed from the 12th iteration
distance40_12cluster.fa - a cluster of "near" sequences generated from that seed
distance40_6cluster_12cluster.fa - fasta database built from the distance40 file
                                   adding the 2 clusters at the 6th and 12th iterations

### DRIFT EXPERIMENT

#### drift_experiment.sh

create the families then run the blasts for the 30, 40 and 50 distance backgrounds

#### plot_average_blast_growth.R

Run this again to see what the memberships look like. and plot the average distances per iteration

#### count_growth_members.py

Quick script to look through the drift hits to see what cluster members are
picked up at each iteration.

produces *.membercount the shows you the recruiting numbers from each pseudo-family and the background

#### plot_member_count.R

Take the membercount graphs and plot some nice histograms.

#### detect_change.py

Use this differentiation https://stackoverflow.com/questions/47519626/using-numpy-scipy-to-identify-slope-changes-in-digital-signals to find inflection points on the graphs

#### find_inflection_points.py

Take the member counts. Find out when 1st cluster members stop being recruited or when 2nd members. Calculate the
detect changes and see how often we're within n iterations of being right (TF) or how often we miss (FN)

### CATH BLAST GROWTH EXPERIMENT

#### run_cath_rep_blasts.py

take a rep from each H family and blast against the annotated dom-seq set

#### calculate_cath_drift.py

read in reps.fa (/cath_distances/REPS) to get the mapping of seq index to cath domain ID.
parse the various blasts at different distances to see when overlapping H families are recruited

outputs:
parsed_blast_rep_iteration_data.csv: summarise which domain were hit and their H-family

ABORTED AS REPS vs REPS isn't dense enough for drift. See Pfam A version

### Pfam BLAST GROWTH EXPERIMENTS

### calculate_pfam_distances.py

Takes an annotated pfam seqs file uses mafft to build alignments of each and then runs RAxML to work out the distances. Produces .dist files in the pfam_distances dir

python3 ../calculate_pfam_distances.py ~/Data/pfam/reps_renumbered.fasta.fa

### run_pfam_rep_blasts.py

take a rep from each pfam family and blast against the annotated pfam_fasta that we
built from the Stockholm format interpro data

### parse_pfam_blasts.py

Short script to collate the information in all the pfam blasts on myriad so I can delete the 1tb of files.

outputs: parsed_pfam_blasts.csv

### find_drift.py

take the parsed_pfam_blasts and find families where drift has occurred. And output some summary stats for plotting such families

outputs: parsed_pfam_iteration_data.csv

### rearrange_pfam_drift_data.py

rearrange parsed_pfam_iteration_data.csv for use with ggplot

iteration_summary.csv

### plot_pfam_growth.R

Take iteration_summary.csv and plot some barcharts.

### calculate_drift_types.py

Take iteration_summary.csv and work out what kinds of drift and stats we can see

Average number of iterations before a contaminant family appears
Average number of contaminating families

# ESM MSATransformer experiment

## esm_seq_generator.py

Here we use MSAtransformer to generate new sequences for pfam alignments masked with
differing amounts

masked_25.fa, masked_50.fa, masked_75.fa

25 = 25% of the seq is masked out before prompting the network

## find_closest_family_rep.py

Open the list of drift families (parsed_pfam_iteration_data.csv). 

Calculate which pfam families our new sequences are closest to. Open parsed_pfam_iteration_data.csv to work out which families were are working on. 
Open ~/Data/pfam/Pfam-A.full.uniprot to get all the family members for each of these. 

Output them to some files as we don't have to process the whole pfam file each time.

Then take our generated seqs (i.e. masked_25.fa) and all against all fasta them against 
the family and drift family members. Taken an n-nearest (1, 3, and 5) nearest neighbour vote.

Produces summarised_msa_model_results.csv. Note some seqs fail to find a good match even when compared to the "drift" families

## esm_seq_generator_single.py

same as esm_seq_generator.py but using the single seq model

## count_profile_memberships.py

Counts up how often we see "drift" in ESM and HMM generated sequences.



# TODO

1. Add check so that `--distance` is not greater than the length of the sequence (hamming) or bigger than can be achieved given a distance matrix (length*max_residue_distance)

2. Check fam family size. see if it is correlated to elimination. i.e. bigger families are more likely to eliminate smaller ones as they can pull the cluster centroid to them
