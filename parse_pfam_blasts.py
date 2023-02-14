import glob
import sys
import re
from collections import defaultdict

results_path = sys.argv[1]

for file in glob.glob("*.bls"):
    print(file)
