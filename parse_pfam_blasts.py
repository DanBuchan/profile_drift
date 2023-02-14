import glob
import sys
import os
import re
from collections import defaultdict

results_path = sys.argv[1]

for path_data in os.walk(results_path):
    for dir in path_data[1]:
        for file in glob.glob(f"{dir}*.bls"):
            print(file)
