#!/usr/bin/python3

import sys

from preds import *

# Load solution.
lits = []
with open(sys.argv[1], "r") as f:
    head = next(f)
    assert head == "s SATISFIABLE\n"
    for row in f:
        cols = row.split()
        assert cols[0] == "v"
        for val in cols[1:]:
            lits.append(int(val))
    assert lits.pop() == 0
    lits = set(lits)

def pp(p, e):
    for n in range(4):
        if v(p, e, n) in lits:
            return n + 1
    assert False

def render_piece(p, k):
    def r(e):
        return (4 + e - k) % 4

    return [
        "+-----+",
        "|  {}  |".format(pp(p, r(1))),
        "|{}   {}|".format(pp(p, r(2)), pp(p, r(0))),
        "|  {}  |".format(pp(p, r(3))),
        "+-----+",
    ]

def adjoin(r1, r2):
    return [r1[i] + r2[i] for i in range(5)]

def pr(r):
    print('\n'.join(r))

rp = render_piece(0, 0)
for p in range(1, 4):
    rp = adjoin(rp, render_piece(p, 0))

pr(rp)

# Decode solution.
soln = []
for s in range(4):
    for p in range(4):
        if l(s, p) in lits:
            for k in range(4):
                if r(p, k) in lits:
                    soln.append((p, k))

assert len(soln) == 4
assert sorted([soln[s][0] for s in range(4)]) == list(range(4))

print()
print(soln[0], soln[1])
print(soln[3], soln[2])
print()
pr(adjoin(render_piece(*soln[0]), render_piece(*soln[1])))
pr(adjoin(render_piece(*soln[3]), render_piece(*soln[2])))
