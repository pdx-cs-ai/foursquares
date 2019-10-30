#!/usr/bin/python3

import random

edges = list(range(1, 5))
random.shuffle(edges)
etop = edges[0]
eleft = edges[1]
eright = edges[2]
ebottom = edges[3]

def piece(*e):
    es = set(range(1, 5)) - (set(e) - {None})
    tofill = list(es)
    random.shuffle(tofill)
    p = []
    for i in range(4):
        if e[i] == None:
            p.append(tofill.pop())
        else:
            p.append(e[i])
    assert not tofill
    print(*p)

piece(etop, None, None, eleft)
piece(None, None, etop, eright)
piece(None, eright, ebottom, None)
piece(ebottom, eleft, None, None)
