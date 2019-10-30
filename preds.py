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
