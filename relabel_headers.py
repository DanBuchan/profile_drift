import sys

count = 0
with open(sys.argv[1], "r") as fh:
    for line in fh:
        if line.startswith(">"):
            count+=1
            print(f'>{count}')
        else:
            line = line.rstrip()
            print(line)
