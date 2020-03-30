#!/usr/bin/env bin

import format

def prettyprint(bits, fmt):
	sign, exponent, mantissa = fmt.unpack(bits)
	if fmt.is_nan(bits):
		print('NaN')
		return
	if fmt.is_inf(bits):
		if sign: print('-∞')
		else: print('+∞')
		return
	if fmt.is_zero(bits):
		if sign: print('-0')
		else: print('+0')
		return
	
	output = ('-' if sign == 1 else ' ') + '1.' + bin(mantissa)[3:] + ' x 2^' + str(exponent)
	print(output)
