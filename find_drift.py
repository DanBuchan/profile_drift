import sys
import csv
from collections import defaultdict


def process_data(current_query, data):
    summary = {}
    # seen = []
    pfam_family_set = set()
    for iteration in sorted(data):
        counts = defaultdict(int)
        for data_row in data[iteration]:
            # if not data_row[2] in seen:
            #     seen.append(data_row[2])
            counts[data_row[3]] += 1
            pfam_family_set.add(data_row[3])
        summary[iteration] = counts

    seen_count = len(pfam_family_set)
    output_string = f'{current_query},{seen_count},'
    for iteration in summary:
        output_string = output_string+f"|{iteration},"
        for family in summary[iteration]:
            output_string = output_string+f"|{family},{summary[iteration][family]},"
    print(output_string)

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
            process_data(current_query, data)
            data = defaultdict(list)
            query_count+=1
            current_query = row[0]
            exit()
        if not current_query:
            current_query = row[0]
            data[int(row[1])].append(row)

        current_query = row[0]
        data[int(row[1])].append(row)

process_data(current_query, data)
query_count+=1
print(f"Processed pfam families: {query_count}")
