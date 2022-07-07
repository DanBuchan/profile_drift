#! /usr/bin/bash

# generate sequence dbs
echo "generating sequences"
python /home/dbuchan/Projects/profile_drift/sequence_generator.py --num_string 10000 --distance 2 --random_pathing 20 --output_file distance2.fa --starting_string_file /home/dbuchan/Projects/profile_drift/data/test_file_150.fa
python /home/dbuchan/Projects/profile_drift/sequence_generator.py --num_string 10000 --distance 5 --random_pathing 20 --output_file distance5.fa --starting_string_file /home/dbuchan/Projects/profile_drift/data/test_file_150.fa
python /home/dbuchan/Projects/profile_drift/sequence_generator.py --num_string 10000 --distance 10 --random_pathing 20 --output_file distance10.fa --starting_string_file /home/dbuchan/Projects/profile_drift/data/test_file_150.fa
python /home/dbuchan/Projects/profile_drift/sequence_generator.py --num_string 10000 --distance 20 --random_pathing 20 --output_file distance20.fa --starting_string_file /home/dbuchan/Projects/profile_drift/data/test_file_150.fa

### Generate distance matrices
echo "calculating distances"
/home/dbuchan/Applications/standard-RAxML/raxmlHPC-PTHREADS-AVX -T 6 -s distance2.fa -n distance2.dist -m PROTGAMMABLOSUM62 -N2 -p 123 -f x > stdout 2> stderr
/home/dbuchan/Applications/standard-RAxML/raxmlHPC-PTHREADS-AVX -T 6 -s distance5.fa -n distance5.dist -m PROTGAMMABLOSUM62 -N2 -p 123 -f x > stdout 2> stderr
/home/dbuchan/Applications/standard-RAxML/raxmlHPC-PTHREADS-AVX -T 6 -s distance10.fa -n distance10.dist -m PROTGAMMABLOSUM62 -N2 -p 123 -f x > stdout 2> stderr
/home/dbuchan/Applications/standard-RAxML/raxmlHPC-PTHREADS-AVX -T 6 -s distance20.fa -n distance20.dist -m PROTGAMMABLOSUM62 -N2 -p 123 -f x > stdout 2> stderr

echo "run distnace experiments"
python ../../run_blasts.py ./distance2.fa ../../data/test_file_150.fa 20 distance2_membership.csv ./RAxML_distances.distance2.dist average_distances2.csv
python ../../run_blasts.py ./distance5.fa ../../data/test_file_150.fa 20 distance5_membership.csv ./RAxML_distances.distance5.dist average_distances5.csv
python ../../run_blasts.py ./distance10.fa ../../data/test_file_150.fa 20 distance10_membership.csv ./RAxML_distances.distance10.dist average_distances10.csv
python ../../run_blasts.py ./distance20.fa ../../data/test_file_150.fa 20 distance20_membership.csv ./RAxML_distances.distance20.dist average_distances20.csv
