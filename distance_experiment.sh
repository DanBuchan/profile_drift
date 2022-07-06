#! /usr/bin/bash

# generate sequence dbs
echo "generating sequences"
python /home/dbuchan/Projects/profile_drift/sequence_generator.py --num_string 10000 --distance 2 --random_pathing 20 --output_file distance2.fa --starting_string_file /home/dbuchan/Projects/profile_drift/data/test_file_150.fa
python /home/dbuchan/Projects/profile_drift/sequence_generator.py --num_string 10000 --distance 5 --random_pathing 20 --output_file distance5.fa --starting_string_file /home/dbuchan/Projects/profile_drift/data/test_file_150.fa
python /home/dbuchan/Projects/profile_drift/sequence_generator.py --num_string 10000 --distance 10 --random_pathing 20 --output_file distance10.fa --starting_string_file /home/dbuchan/Projects/profile_drift/data/test_file_150.fa
python /home/dbuchan/Projects/profile_drift/sequence_generator.py --num_string 10000 --distance 20 --random_pathing 20 --output_file distance20.fa --starting_string_file /home/dbuchan/Projects/profile_drift/data/test_file_150.fa

### Generate distance matrices
echo "calculating distances"
/home/dbuchan/Applications/standard-RAxML/raxmlHPC-PTHREADS-AVX -T 6 -s distance2.fa -n full_db.dist -m PROTGAMMABLOSUM62 -N2 -p 123 -f x > stdout 2> stderr
/home/dbuchan/Applications/standard-RAxML/raxmlHPC-PTHREADS-AVX -T 6 -s distance5.fa -n full_db.dist -m PROTGAMMABLOSUM62 -N2 -p 123 -f x > stdout 2> stderr
/home/dbuchan/Applications/standard-RAxML/raxmlHPC-PTHREADS-AVX -T 6 -s distance10.fa -n full_db.dist -m PROTGAMMABLOSUM62 -N2 -p 123 -f x > stdout 2> stderr
/home/dbuchan/Applications/standard-RAxML/raxmlHPC-PTHREADS-AVX -T 6 -s distance20.fa -n full_db.dist -m PROTGAMMABLOSUM62 -N2 -p 123 -f x > stdout 2> stderr
