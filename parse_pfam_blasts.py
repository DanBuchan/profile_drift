import glob
import sys
import os
import re
from collections import defaultdict

results_path = sys.argv[1]

subfolders = [ f.path for f in os.scandir(results_path) if f.is_dir() ]

result_list_pattern = re.compile(r"^(.+?)\s+(.+?)\s+(.+?)\n")
print("Query,iteration,hit,hit_family\n")
for dir in subfolders:
    results = defaultdict(list)
    seen = []
    quert = ''
    for file in glob.glob(f"{dir}/*.bls"):
        print(file)
        file_parts = file.split("_")
        query = file_parts[0][len(dir)+1:]
        iteration = int(file_parts[1].split(".")[0][9:])
        print(query, iteration)
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
                                results[iteration].append(result.groups()[0])
                                seen.append(result.groups()[0])
                            #print(result.groups()[0])

    for iteration in results.keys():
        for hit in results[iteration]:
            print(query,iteration,hit)
            #print(f'{iteration},{hit}')
    exit()
