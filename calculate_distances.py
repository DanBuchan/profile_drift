import subprocess
import sys
import os

fasta_data = {}
with open('output.fa', encoding="utf-8", mode="r") as fafile:
    name = ''
    for line in fafile:
        if line.startswith(">"):
            entries = line.split(";")
            name = entries[0][1:]
        else:
            fasta_data[name] = line.rstrip()

stretcher_args = ['/home/dbuchan/Applications/EMBOSS-6.6.0/emboss/stretcher',
                  '-asequence',
                  'tmpA.fa',
                  '-bsequence',
                  'tmpB.fa',
                  '-aformat',
                  'fasta',
                  '-outfile',
                  'stretch_tmp.fa']

distmat_args = ['/home/dbuchan/Applications/EMBOSS-6.6.0/emboss/distmat',
                'stretch_tmp.fa',
                '-protmethod',
                '1',
                '-outfile',
                'dist.tmp']

fhOut = open("pairwise_distance.csv", "w", encoding="utf-8")
fhOut.write("prot1,prot2,distance\n")
for name in fasta_data:
    for name2 in fasta_data:
        if name == name2:
            continue
        with open('tmpA.fa', "w", encoding="utf-8") as outfh:
            outfh.write(f'>{name}\n')
            outfh.write(f'{fasta_data[name]}\n')
        with open('tmpB.fa', "w", encoding="utf-8") as outfh:
            outfh.write(f'>{name2}\n')
            outfh.write(f'{fasta_data[name2]}\n')
        try:
            code = subprocess.call(' '.join(stretcher_args), shell=True)
        except Exception as e:
            print(str(e))
            sys.exit(1)
        if code != 0:
            print("Non Zero Exit status: "+str(code))
            raise OSError("Non Zero Exit status: "+str(code))
        try:
            code = subprocess.call(' '.join(distmat_args), shell=True)
        except Exception as e:
            print(str(e))
            sys.exit(1)
        if code != 0:
            print("Non Zero Exit status: "+str(code))
            raise OSError("Non Zero Exit status: "+str(code))

        distfile = open('dist.tmp', encoding="utf-8", mode="r")
        content = distfile.readlines()
        results = content[-2].split()
        if results[1] == "-nan":
            exit()
        fhOut.write(f'{name},{name2},{results[1]}\n')

fhOut.close()
os.remove("tmpA.fa")
os.remove("tmpB.fa")
os.remove("stretch_tmp.fa")
os.remove("dist.tmp")
