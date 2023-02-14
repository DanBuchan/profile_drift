import glob
import sys
import os
import re
from collections import defaultdict

results_path = sys.argv[1]

subfolders = [ f.path for f in os.scandir(results_path) if f.is_dir() ]
results = defaultdict(list)
seen = []
result_list_pattern = re.compile(r"^(.+?)\s+(.+?)\s+(.+?)\n")
for dir in subfolders:
    for file in glob.glob(f"{dir}/*.bls"):
        print(file)
        file_parts = file.split("_")
        query = file_parts[0]
        iteration = file_parts[1].split(".")[0][9:]
        print(query, iteration)
        count+=1
        read = False
        with open(file, "r") as fh:
            for line in fh:
                if line.startswith('Sequences producing significant'):
                     read = True
                     continue
                if line.startswith('>'):
                    read = False
                    continue
                if read:
                    result = re.match(result_list_pattern, line)
                    if result:
                        if float(result.groups()[2]) < 1e-5:
                            if result.groups()[0] not in seen:
                                results[count].append(result.groups()[0])
                                seen.append(result.groups()[0])
                            #print(result.groups()[0])

        for iteration in results.keys():
            for hit in results[iteration]:
                pass
                #print(f'{iteration},{hit}')
        exit()
