import sys
import csv

blast_summary_file = sys.argv[1]
current_query = None
query_count = 0
with open(blast_summary_file, 'r') as datafile:
    blast_reader = csv.reader(datafile, delimiter=',',)
    next(blast_reader)
    for row in blast_reader:
        print(row)
        exit()
