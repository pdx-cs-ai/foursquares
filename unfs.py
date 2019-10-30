#!/usr/bin/python3

import sys

from preds import *

# Load solution.
lits = []
with open(sys.argv[1], "r") as f:
    next(f)
    for row in f:
        for val in row.split():
            lits.append(int(val))
    assert lits.pop() == 0
    lits = set(lits)
    
# Decode solution.
for s in range(4):
    for p in range(4):
        if l(s, p) in lits:
            for k in range(4):
                if r(p, k) in lits:
                    print(s, p, k)
