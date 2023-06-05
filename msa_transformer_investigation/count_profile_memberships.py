import csv
import sys
import pandas as pd
from collections import defaultdict
"""
useage: count_profile_memberships.py ./generated_seqs/summarised_msa_model_results.csv
"""

# parsing csv of format:"
# file,generated_family,query_name,best_hit_family,best_hit_score"
# we check if the best hit (col 3) is the same as the
# input seq source or generating model (col 1)
# col 0 is the modelling assumpt we worked with.
df = pd.read_csv(sys.argv[1], na_filter=False)
group_sizes = df.groupby(["file", "generated_family", "best_hit_family"]).size()
size_frame = group_sizes.to_frame().reset_index()

group_totals = defaultdict(lambda: defaultdict(int))
for index, row in size_frame.iterrows():
    group_totals[row['file']][row['generated_family']] += row[0]

results = defaultdict(lambda: defaultdict(lambda: defaultdict(int)))
for idx, row in df.iterrows():
    if len(row['best_hit_family']) == 0 or 'NA' in row['best_hit_family']:
        results[row['file']][row['generated_family']]['OUT_OF_DRIFT_SEQ']+=1 
        continue
    if row['best_hit_family'] == row['generated_family']:
        results[row['file']][row['generated_family']]['FAMILY_MATCH']+=1
    else:
        results[row['file']][row['generated_family']]['DRIFT_MATCH']+=1

print("file,total_families,with_drift,with_out_of_bounds")
for file_set in results:
    total_families = 0
    total_with_drift_hits = 0
    total_with_out_of_hits = 0
    for family in results[file_set]:
        total_families+=1
        if 'OUT_OF_DRIFT_SEQ' in results[file_set][family].keys():
            total_with_out_of_hits+=1
        if 'DRIFT_MATCH' in results[file_set][family].keys():
            total_with_drift_hits+=1
        results[file_set][family]['DRIFT_MATCH'] =results[file_set][family]['DRIFT_MATCH']/group_totals[file_set][family]
        results[file_set][family]['FAMILY_MATCH'] =results[file_set][family]['FAMILY_MATCH']/group_totals[file_set][family]
        results[file_set][family]['OUT_OF_DRIFT_SEQ'] =results[file_set][family]['OUT_OF_DRIFT_SEQ']/group_totals[file_set][family]    
    print(file_set,total_families,total_with_drift_hits,total_with_out_of_hits)        

# print(results)