#!/usr/bin/python3

# Number the pieces 0..3, the positions in the square 0..3.
# Atom: piece p is in square s (location).
def l(s, p):
    return 1 + s * 4 + p

# Number the coordinates of the edges of each square 0..3.
# Atom: piece in square s at edge e is n (match).
def m(s, e, n):
    return l(3, 3) + 1 + s * 4**2 + e * 4 + n

# Number the edges of each piece 0..3
# Atom: piece p at edge e is n (value).
def v(p, e, n):
    return m(3, 3, 3) + 1 + p * 4**2 + e * 4 + n

# Number the rotations of each piece 0..3.
# Atom: piece p has rotation k.
def r(p, k):
    return v(3, 3, 3) + 1 + p * 4 + k

clauses = []

def clause(*lits):
    clauses.append(lits)

# Every piece is at some location.
for s in range(4):
    clause(*[l(s, p) for p in range(4)])

# No piece is at more than one location.
for s in range(4):
    for p1 in range(4):
        for p2 in range(4):
            if p1 == p2:
                continue
            clause(-l(s, p1), -l(s, p2))

# Every piece is at some rotation.
for s in range(4):
    clause(*[r(s, k) for k in range(4)])

# No piece has more than one rotation.
for p in range(4):
    for k1 in range(4):
        for k2 in range(4):
            if k1 == k2:
                continue
            clause(-r(p, k1), -r(p, k2))

# Square coordinates are a function of piece location and rotation.
for s in range(4):
    for p in range(4):
        for k in range(4):
            for e in range(4):
                k0 = (e + k) % 4
                for n in range(4):
                    clause(-l(p, s), -r(p, k), -v(p, k0, n), m(s, e, n))
                    clause(-m(s, e, n), l(p, s))
                    clause(-m(s, e, n), r(p, k))
                    clause(-m(s, e, n), v(p, k0, n))

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

# Print problem.
print(r(3, 3), len(clauses))
for c in clauses:
    print(*c, 0)
