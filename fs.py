#!/usr/bin/python3

import sys

# All arguments are in the range 0..3.
def inrange(*args):
    for a in args:
        if a < 0 or a >= 4:
            return False
    return True

# Number the pieces 0..3, the positions in the square 0..3.
# Atom: piece p is in square s (location).
def l(s, p):
    assert inrange(s, p)
    return 1 + s * 4 + p

# Number the coordinates of the edges of each square 0..3.
# Atom: piece in square s at edge e is n (match).
def m(s, e, n):
    assert inrange(s, e, n)
    return l(3, 3) + 1 + s * 4**2 + e * 4 + n

# Number the edges of each piece 0..3
# Atom: piece p at edge e is n (value).
def v(p, e, n):
    assert inrange(p, e, n)
    return m(3, 3, 3) + 1 + p * 4**2 + e * 4 + n

# Number the rotations of each piece 0..3.
# Atom: piece p has rotation k.
def r(p, k):
    assert inrange(p, k)
    return v(3, 3, 3) + 1 + p * 4 + k

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
                    clause(-m(s, e, n), l(s, p))
                    clause(-m(s, e, n), r(p, k))
                    clause(-m(s, e, n), v(p, x, n))

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
