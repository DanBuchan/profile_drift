import glob
import sys
import os
import re
from collections import defaultdict

results_path = sys.argv[1]

subfolders = [ f.path for f in os.scandir(results_path) if f.is_dir() ]
for dir in subfolders:
    for file in glob.glob(f"{dir}/*.bls"):
        print(file)
