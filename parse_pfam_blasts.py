import glob
import sys
import os
import re
from collections import defaultdict

results_path = sys.argv[1]

for dir in os.walk(results_path):
    print(dir)
    for file in glob.glob(f"{dir}*.bls"):
        print(file)
