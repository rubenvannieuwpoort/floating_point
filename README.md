# Floating point

This repository contains software implementations of some floating point algorithms. This implementation does not support denormals! This makes it different from the hardware implementation in most CPU's.


## Why are denormals not supported?

I plan to make a VHDL-based hardware implementation, and denormals are a pain in the ass to implement in hardware. For this reasons, many hardware implementation do not support denormals. I might add *some* support later, but probably not. You're always welcome to open a pull request, though.


## Usage example

    import float
    
    # Pack gives you the binary representation from the (sign, exponent, mantissa) representation
    # Binary32 is the float format
    op1 = float.binary32.pack(0, 5, 0)
    op2 = float.binary32.pack(0, 1, 0)
    result = float.add(op1, op2, float.binary32)
    
    print(float.binary32.format(op1) + ' + ' + float.binary32.format(op2) + ' = ' + float.binary32.format(result))
