#!/bin/sh
# Copyright © 2020 Bart Massey
# [This program is licensed under the "MIT License"]
# Please see the file COPYING in the source
# distribution of this software for license terms.

# Driver for SAT-solver-based Foursquare solver.

# Set some things up.
PGM="`basename $0`"
USAGE="$PGM: usage: $PGM <problem>"
PROBTMP=/tmp/prob.$$
SOLNTMP=/tmp/soln.$$
trap "rm -f $PROBTMP $SOLNTMP" 0 1 2 3 15

# Read from a supplied file, else from standard input.
case $# in
    1) python3 fs.py "$1" >$PROBTMP ;;
    *) echo "$USAGE" >&2 ; exit 1 ;;
esac

# Finally, invoke a solver to solve the SAT instance.
picosat $PROBTMP >$SOLNTMP
# Could the solver find an assignment? These return codes are
# apparently standard. We will use them too.
case $? in
    10)
	;;
    20)
	echo "problem has no legal solution" >&2
	exit 20
	;;
    *)
	echo "unexpected picosat exit code $?"
	exit 1
	;;
esac
python3 unfs.py "$SOLNTMP"
exit 10
