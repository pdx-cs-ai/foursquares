#!/usr/bin/python3

import sys

from preds import *

# List of clauses to output.
clauses = []

# Add a new clause to the list.
def clause(*lits):
    clauses.append(lits)

# Every piece is at some location.
for p in range(4):
    clause(*[l(s, p) for s in range(4)])

# No piece is at more than one location.
for p in range(4):
    for s1 in range(4):
        for s2 in range(s1+1, 4):
            clause(-l(s1, p), -l(s2, p))

# Every square has a piece.
for s in range(4):
    clause(*[l(s, p) for p in range(4)])

# No square has more than one piece.
for s in range(4):
    for p1 in range(4):
        for p2 in range(s1+1, 4):
            clause(-l(s, p1), -l(s, p2))

# Piece 0 is in location 0 (remove rotational symmetry).
clause(l(0, 0))


# Every piece is at some rotation.
for p in range(4):
    clause(*[r(p, k) for k in range(4)])

# No piece has more than one rotation.
for p in range(4):
    for k1 in range(4):
        for k2 in range(k1+1, 4):
            clause(-r(p, k1), -r(p, k2))

# Square coordinates are a function of piece location and rotation.
for s in range(4):
    for e in range(4):
        for p in range(4):
            for k in range(4):
                x = (4 - k + e) % 4
                for n in range(4):
                    clause(-l(s, p), -r(p, k), -v(p, x, n), m(s, e, n))

# Edges have unique values.
for s in range(4):
    for e in range(4):
        for n1 in range(4):
            for n2 in range(n1+1, 4):
                clause(-m(s, e, n1), -m(s, e, n2))

# Edges must match.
central_edges = [
     (0, 0, 1, 2),
     (1, 3, 2, 1),
     (2, 2, 3, 0),
     (3, 1, 0, 3),
]
for n in range(4):
    for s1, e1, s2, e2 in central_edges:
        clause(-m(s1, e1, n), m(s2, e2, n))
        clause(m(s1, e1, n), -m(s2, e2, n))

# Load pieces.
with open(sys.argv[1], "r") as f:
    for p, piece in enumerate(f):
        for e, n in enumerate(piece.split()):
            clause(v(p, e, int(n) - 1))

# Print problem.
print("p", "cnf", r(3, 3), len(clauses))
for c in clauses:
    print(*c, 0)
