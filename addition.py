#!/usr/bin/env python3

from common import *
import rounding, format

def sub(bits1, bits2, fmt, rounding_scheme = None):
	# Negate second operand and continue with normal addition
	return add(bits1, neg(bits2, fmt), fmt, rounding_scheme)

def add(bits1, bits2, fmt = format.default, rounding_scheme = None):
	
	# Unpack
	(sign1, exponent1, mantissa1) = fmt.unpack(bits1)
	(sign2, exponent2, mantissa2) = fmt.unpack(bits2)
	
	# Handle special cases (NaN, Inf, zero)
	if fmt.is_nan(bits1) or fmt.is_nan(bits2):
		return fmt.nan()
	if fmt.is_inf(bits1) and not(fmt.is_inf(bits2)):
		return fmt.inf(sign1)
	if not(fmt.is_inf(bits1)) and fmt.is_inf(bits2):
		return fmt.inf(sign2)
	if fmt.is_inf(bits1) and fmt.is_inf(bits2):
		if sign1 == sign2: return fmt.inf(sign1)
		else: return fmt.nan()
	if fmt.is_zero(bits2):
		if fmt.is_zero(bits1):
			# Clear sign bit (that's right, zero is not an identity element
			# when you use IEEE 754 floating point arithmetic)
			return bits1 & (~(1 << (fmt.exponent + fmt.mantissa)))
		return bits1
	if fmt.is_zero(bits1):
		if fmt.is_zero(bits2):
			return bits2 & (~(1 << (fmt.exponent + fmt.mantissa)))
		return bits2
	
	# Align mantissas
	if (exponent2 > exponent1):
		(sign1, exponent1, mantissa1), (sign2, exponent2, mantissa2) = \
		(sign2, exponent2, mantissa2), (sign1, exponent1, mantissa1)
	
	exponent = exponent1
	
	# Selective complement
	if sign1 != sign2: mantissa1 = -mantissa1
	sign = sign2
	
	# Align mantissas
	# Add three bits (guard, round, sticky) at the end for rounding
	mantissa1, mantissa2 = mantissa1 << 3, mantissa2 << 3
	
	shiftright = exponent1 - exponent2
	assert shiftright >= 0
	
	if shiftright < fmt.mantissa + 3:
		# Shift right with sticky bit
		for i in range(0, shiftright):
			mantissa2 = (mantissa2 >> 1) | (mantissa2 & 1)
	else: mantissa2 = 1 # 1 for the sticky bit? Although it shouldn't matter, I think...
	                    # The bound can probably also be one lower if we use 1...
	
	# Actual adding
	mantissa = mantissa1 + mantissa2
	
	if mantissa == 0:
		return fmt.zero(0)
	
	if mantissa < 0:
		mantissa = -mantissa
		sign = 1 - sign
	
	# Postshift if necessary
	msb = 1 << (fmt.mantissa + 3)
	if 0 < mantissa and mantissa < msb:
		while (mantissa & msb) == 0:
			mantissa <<= 1
			exponent -= 1
		assert (mantissa & (1 << (fmt.mantissa + 3))) > 0
	elif (mantissa >= 2 * msb):
		mantissa = (mantissa >> 1) | (mantissa & 1)
		exponent += 1
	
	mantissa, g, r, s = (mantissa >> 3), mantissa & 4, mantissa & 2, mantissa & 1
	mantissa = rounding.round(sign, mantissa, g, r, s, rounding_scheme)
	
	if mantissa == 0: return fmt.zero(sign)
	if exponent > fmt.max_exponent: return fmt.inf(sign)
	
	msb = 1 << fmt.mantissa
	if mantissa >= 2 * msb:
		mantissa >>= 1
		exponent += 1
	
	return fmt.pack(sign, exponent, mantissa)
