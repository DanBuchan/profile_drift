import sys
import csv
from collections import defaultdict
from os.path import exists
import Bio

"""
python find_closest_family_rep.py ../iteration_summary.csv ~/Data/pfam/Pfam-A.full.uniprot
"""

def parse_pfam_alignments(pfam_aligns, drift_families):
    nr_list = set()
    for family in drift_families:
         nr_list.add(family)
         for item in drift_families[family]:
             nr_list.add(item)

    align_count = 0
    with open(pfam_aligns, "rb") as fh:
        align_name = ''
        msa = defaultdict(list)
        for line_binary in fh:
            try:
                line = line_binary.decode("utf-8")
            except Exception as e:
                print(e)
                print(line_binary)
                continue
            if line.startswith("//"):
                continue
            if line.startswith("# STOCKHOLM"):
                if align_count != 0:
                    if align_name in nr_list:
                        print(f"Printing: {align_name}")
                        with open(f"{align_name}.fa", "w") as fhOut:
                            for msa_line in msa[align_name]:
                                fhOut.write(f">{msa_line[0]}\n")
                                fhOut.write(f"{msa_line[1]}\n")             
                else:
                    align_count+=1
                align_name = ''
                msa = defaultdict(list)
            if line.startswith("#=GF AC   "):
                align_name = line[10:].rstrip()
                align_name = align_name.split(".", 1)[0]
            if not line.startswith("#"):
                entries = line.split()
                seq = entries[1].replace('-', '')
                seq = seq.replace('.', '')
                seq_data = (entries[0], seq)
                msa[align_name].append(seq_data)
        print(f"Printing: {align_name}")
        with open(f"{align_name}.fa") as fhOut:
            for msa_line in msa[align_name]:
                fhOut.write(f">{msa_line[0]}\n")
                fhOut.write(f"{msa_line[1]}\n")

    with open("families_list.txt") as fhOut:
        for entry in nr_list:
            fhOut.write(f'{entry}\n')
        


def read_drifts(file):
    drift_families = defaultdict(set)
    with open(file, "r") as fhIn:
        next(fhIn)
        iteration_reader = csv.reader(fhIn, delimiter=",")
        for row in iteration_reader:
            drift_families[row[1]].add(row[3])
    return drift_families

def read_generated_seqs(file):
    seqs = defaultdict(list)
    family_id = ''
    with open(file, "r") as fhIn:
        for line in fhIn:
            if line.startswith(">"):
                family_id = line[1:]
                family_id = family_id.rstrip()
                family_id = family_id.split("_")[0]
            else:
                seqs[family_id].append(line.rstrip().replace("-", ''))
    return seqs

def read_fasta_seqs(family_id, file):
    seqs = []
    with open(file, "r") as fhIn:
        for line in fhIn:
            if line.startswith(">"):
                pass
            else:
                seqs.append(line.rstrip().replace("-", ''))
    return seqs

# loop over every 
def find_closest_fasta(generated_seqs, pfam_family, families_hit):
    closest_count = defaultdict(dict)
    target_seqs = {}
    proceed_analysis = True
    for target in families_hit:
        if target in generated_seqs:
            target_seqs[target] = read_fasta_seqs(target, f"alignments/{target}.fa")
        else:
            proceed_analysis = False

    print(target_seqs)        
    if proceed_analysis:
        print(pfam_family)
        for seq in generated_seqs[pfam_family]:
            for target_family in target_seqs:
                for target_seq in target_seqs[target_family]:
                    print(target_seq)
                    # print("Comparing", seq, target_seq, "from", target_family)
    
    return closest_count


drift_families = read_drifts(sys.argv[1])
if not exists("families_list.txt"):
    parse_pfam_alignments(sys.argv[2], drift_families)

for file in ['masked_25.fa', 'masked_25.fa', 'masked_25.fa']:
    generated_seqs = read_generated_seqs(file)
    for pf_family in drift_families:
        # print(pf_family, drift_families[pf_family])
        results = find_closest_fasta(generated_seqs, pf_family, drift_families[pf_family])
        exit()
f