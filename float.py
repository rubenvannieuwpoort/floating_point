#!/usr/bin/env python3

# TODO: Are common and format even necessary? Aren't these exported by addition???
from addition import add, sub
from prettyprint import prettyprint
from format import binary32

# Some software implementations of floating point numbers.
# Might be the basis for a VHDL implementation later on.
# Note that denormals are *not supported* (as in many hardware implementations).

# TODO:
#  1. Multiplication
#  2. Division
#  3. Remainder
#  4. Comparisons
#  5. Conversions to other floating point formats
#  6. Conversions to integers
#  7. Min and max
#  8. Add support for traps and/or flags (see https://docs.oracle.com/cd/E19957-01/806-3568/ncg_handle.html)
#   (maybe: squareroot, trigonometric functions, log?)
