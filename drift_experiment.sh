#! /usr/bin/bash

# generate sequence dbs
echo "generating sets with familes"
# python /home/dbuchan/Projects/profile_drift/create_family.py distance2.fa distance2_membership.csv distance2
# python /home/dbuchan/Projects/profile_drift/create_family.py distance5.fa distance5_membership.csv distance5
# python /home/dbuchan/Projects/profile_drift/create_family.py distance10.fa distance10_membership.csv distance10
# python /home/dbuchan/Projects/profile_drift/create_family.py distance20.fa distance20_membership.csv distance20
# python /home/dbuchan/Projects/profile_drift/create_family.py distance30.fa distance30_membership.csv distance30
# python /home/dbuchan/Projects/profile_drift/create_family.py distance40.fa distance40_membership.csv distance40
# python /home/dbuchan/Projects/profile_drift/create_family.py distance50.fa distance50_membership.csv distance50

echo "run distance experiments"
for step in '2' '5' '10' '20' '30' '40' '50';
# for step in '2';
do
  for entry in "./distance"$step"_"*"cluster_"*"cluster.fa";
  # for id in '1000';
  do
    echo $entry
    read step start id <<<${entry//[^0-9]/ }
    db="distance"$step"_"$start"cluster_"$id"cluster.fa"
    seed="distance"$step"_"$start"_seed.fa"
    membership="distance"$step"_"$start"cluster_"$id"cluster_membership.csv"
    averages="average_distances"$step"_"$start"cluster_"$id"cluster.csv"
    raxml="RAxML_distances.distance"$step"_"$start"cluster_"$id"cluster.dist"
    dist="distance"$step"_"$start"cluster_"$id"cluster.dist"
    echo "/home/dbuchan/Applications/standard-RAxML/raxmlHPC-PTHREADS-AVX -T 6 -s $db -n $dist -m PROTGAMMABLOSUM62 -N2 -p 123 -f x > stdout 2> stderr"
    echo "python /home/dbuchan/Projects/profile_drift/run_blasts.py $db $seed 20 $membership $raxml $averages"
    /home/dbuchan/Applications/standard-RAxML/raxmlHPC-PTHREADS-AVX -T 6 -s $db -n $dist -m PROTGAMMABLOSUM62 -N2 -p 123 -f x > stdout 2> stderr
    python /home/dbuchan/Projects/profile_drift/run_blasts.py $db $seed 20 $membership $raxml $averages
  done
done
