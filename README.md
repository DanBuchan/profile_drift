# Some code to study the nature of profile drift in sequence search

## Code

### sequence_generator.py

Script that takes a seed sequence and generates an artificial database
of protein sequences where each sequence is some fixed distance from its parent.

Current it just random walks from each generated sequence and ensures it doesn't
generate a sequence it has seen before. Distance is just the raw substitution
distance (like a hamming distance).

## TODO

Add flag/behaviour so that distance can be either the substitution distance or
a blosum62 distance. Which would mean replacing `replacements = random.sample(range(0, alphabet_size), args.distance)` with some function that selects a set of substitutions that are approximately the provided distance from.
