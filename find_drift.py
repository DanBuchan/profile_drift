import sys
import csv
from collections import defaultdict


def process_data(data):
    seen = []
    summary = {}
    for iteration in sorted(data):
        counts = defaultdict(int)
        for data_row in data[iteration]:
            if not data_row[2] in seen:
                seen.append(data_row[2])
                counts[data[3]] += 1
        summary[iteration] = counts
    print(summary)

blast_summary_file = sys.argv[1]
current_query = None
query_count = 0
data = defaultdict(list)
with open(blast_summary_file, 'r') as datafile:
    blast_reader = csv.reader(datafile, delimiter=',',)
    next(blast_reader)
    next(blast_reader)

    for row in blast_reader:
        if current_query and not row[0] == current_query:
            process_data(data)
            data = defaultdict(list)
            query_count+=1
            current_query = row[0]
            exit()
        if not current_query:
            current_query = row[0]
            data[int(row[1])].append(row)

        current_query = row[0]
        data[int(row[1])].append(row)

process_data(data)
query_count+=1
print(f"Processed pfam families: {query_count}")
