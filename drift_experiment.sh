#! /usr/bin/bash

# generate sequence dbs
echo "generating sets with familes"
# python /home/dbuchan/Projects/profile_drift/create_family.py distance2.fa distance2
# python /home/dbuchan/Projects/profile_drift/create_family.py distance5.fa distance5
# python /home/dbuchan/Projects/profile_drift/create_family.py distance10.fa distance10
# python /home/dbuchan/Projects/profile_drift/create_family.py distance20.fa distance20
# python /home/dbuchan/Projects/profile_drift/create_family.py distance30.fa distance30
# python /home/dbuchan/Projects/profile_drift/create_family.py distance40.fa distance40
# python /home/dbuchan/Projects/profile_drift/create_family.py distance50.fa distance50

echo "run distance experiments"
for step in '2' '5' '10' '20' '30' '40' '50';
# for step in '2';
do
  for id in '1000' '1500' '2000' '2500' '3000' '3500' '4000' '4500' '5000' '5500' '6000' '6500' '7000' '7500' '8000' '8500' '9000' '9500';
  # for id in '1000';
  do
    db="distance"$step"_500cluster_"$id"cluster.fa"
    seed="distance"$step"_500_seed.fa"
    membership="distance"$step"_500cluster_"$id"cluster_membership.csv"
    averages="average_distances"$step"_500cluster_"$id"cluster.csv"
    raxml="RAxML_distances.distance"$step"_500cluster_"$id"cluster.dist"
    dist="distance"$step"_500cluster_"$id"cluster.dist"
    echo "/home/dbuchan/Applications/standard-RAxML/raxmlHPC-PTHREADS-AVX -T 6 -s $db -n $dist -m PROTGAMMABLOSUM62 -N2 -p 123 -f x > stdout 2> stderr"
    echo "python /home/dbuchan/Projects/profile_drift/run_blasts.py $db $seed 20 $membership $raxml $averages"
    /home/dbuchan/Applications/standard-RAxML/raxmlHPC-PTHREADS-AVX -T 6 -s $db -n $dist -m PROTGAMMABLOSUM62 -N2 -p 123 -f x > stdout 2> stderr
    python /home/dbuchan/Projects/profile_drift/run_blasts.py $db $seed 20 $membership $raxml $averages
  done
done
