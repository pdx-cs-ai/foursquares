# foursquare-sat: Solve Foursquare puzzles using a SAT engine
Bart Massey

## The Four Squares Puzzle

Given these four pieces

        +-----+  +-----+  +-----+  +-----+
        |  3  |  |  3  |  |  2  |  |  1  |
        |4   1|  |2   4|  |4   1|  |2   4|
        |  2  |  |  1  |  |  3  |  |  3  |
        +-----+  +-----+  +-----+  +-----+

we can rearrange and rotate them arbitrarily and assemble
them into a square

        +-----+-----+
        |  4  |  3  |
        |3   1|1   4|
        |  2  |  2  |
        +-----+-----+
        |  2  |  4  |
        |3   1|2   3|
        |  4  |  1  |
        +-----+-----+

Can we make a square such that all the edges match?

Our solution strategy will involve:

* Creating a SAT formula from the instance
* Solving that formula with an off-the-shelf solver
* Interpreting the SAT soln as an instance solution 

## Running

You must have `picosat` installed to use this code as-is. It
can be easily modified for other DIMACS-format SAT
solvers. To try it out:

    sh foursquare-sat.sh puzzles/orig.txt

You should see the puzzle and its solution.

You can say `python3 puzgen.py` to get more puzzles. Puzzle
format is one piece per row with the edge numbers listed in
counterclockwise order.

## Modeling Foursquares

### Setup

* Number the pieces 1..4, the positions in the square
  1..4. We will number the square positions clockwise
  starting from the upper left. We will number the edges of
  the piece counterclockwise starting from the right edge.

        l(s, p) iff piece p is in square s  (location)

* Number the coordinates of the edges of each square 1..4

        m(s, e, n) iff piece in square s at edge e is n (match)

* Number the edges of each piece 1..4

        v(p, e, n) iff piece p at edge e is n (value)

* Number the rotations of each piece 0..3. Rotations will be
  counterclockwise.

        r(p, k) iff piece p has rotation k


### Basic Constraints

* Every piece is at some location

        forall s . exists p . l(s, p)

* No location contains more than one piece

        forall s . forall p1, p2 | p1 =/= p2 . not l(s, p1) or not l(s, p2)

* First piece is in first corner (remove rotational
  symmetry)
  
        l(1, 1)

* Every location has a piece

        forall p . exists s . l(s, p)

* No piece is at more than one location

        forall p . forall s1, s2 | s1 =/= s2 . not l(s1, p) or not l(s2, p)

* Every piece is at some rotation

        forall p . exists k . r(p, k)

* No piece has more than one rotation

        forall p . forall k1, k2 | k1 =/= k2 . not r(p, k1) or not r(p, k2)

### Fancy Constraints

* Square coordinates are a function of piece location and rotation

        forall s, p, k, e, n .
            m(s, e, n) if l(p, s) and r(p, k) and v(p, (4 - k + e) mod 4, n)

* No square edge can have more than one value

        forall s, e . forall n1, n2 | n1 =/= n2 .
            not m(s, e, n1) or not m(s, e, n2)

* Edges must match

        forall s1, e1, s2, e2 |
           s1 = 1 and e1 = 1 and s2 = 2 and e2 = 3 or … .
               forall n . m(s1, e1, n) iff m(s2, e2, n)
