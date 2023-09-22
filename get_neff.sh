# get Neff for all alignments.
# We will use CD-HIT with a sequence identity threshold of 62%.

if [ -z "$1" ]; then
    echo "usage: $0 seqs.fasta"
    echo '    seqs.fasta should be a set of *unaligned* sequences.'
    exit 0
fi

cdhit="${HOME}/miniconda3/bin/cd-hit"

input="$(readlink -f $1)"

$cdhit -i "${input}" -o "${input}.cdhit.out" -T 4 -c 0.62 -n 4 > "${input}.cdhit.out2"
grep -Ec "^>" "${input}.cdhit.out.clstr" > "${input}.neff" # count the number of lines starting with '>'

rm "${input}.cdhit.out2" "${input}.cdhit.out.clstr"

#for n in $1/*.afa; do
#    printf '.'
#    $cdhit -i $n -o $n.cdhit.out -T 4 -c 0.62 -n 4 > $n.cdhit.out2
#    grep -Ec "^>" $n.cdhit.out.clstr > ${n}.neff # count the number of lines starting with '>'
#done

#echo 'Done!'
