import sys
import csv
from collections import defaultdict

blast_summary_file = sys.argv[1]
current_query = None
query_count = 0
data = {}
with open(blast_summary_file, 'r') as datafile:
    blast_reader = csv.reader(datafile, delimiter=',',)
    next(blast_reader)
    next(blast_reader)

    for row in blast_reader:
        if not current_query:
            current_query = row[0]
        elif (not current_query) and not row[0] == current_query:
            #process prior data
            count+=1
            current_query = row[0]
            print(data)
            exit()
        data[int(row[1])] = row

print(f"Processed pfam families: {count}")
