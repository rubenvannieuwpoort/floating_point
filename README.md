# Floating point

This repository contains software implementations of some floating point algorithms. This implementation does not support denormals! This makes it different from the hardware implementation in most CPU's.

Currently supported operations: addition, subtraction, multiplication.

The tests are adapted from [IBM's FPgen testset](https://www.research.ibm.com/haifa/projects/verification/fpgen/). Testcases which throw exceptions are not used at the moment, and denormals are flushed to zero.


## Why are denormals not supported?

I plan to make a VHDL-based hardware implementation, and denormals are a pain in the ass to implement in hardware. For this reasons, many hardware implementation do not support denormals. I might add support later, but I probably won't. You're always welcome to open a pull request, though.


## Usage example

    import float
    
    # Pack gives you the binary representation from the (sign, exponent, mantissa) representation
    # Binary32 is the float format
    op1 = float.binary32.pack(0, 5, 0)
    op2 = float.binary32.pack(0, 1, 0)
    result = float.add(op1, op2, float.binary32)
    
    print(float.binary32.format(op1) + ' + ' + float.binary32.format(op2) + ' = ' + float.binary32.format(result))
