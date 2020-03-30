#!/usr/bin/env python3

import format

def neg(bits, fmt = format.default):
	sign, exponent, mantissa = fmt.unpack(bits)
	return fmt.pack(1 - sign, exponent, mantissa)

