#!/usr/bin/env python3

# Some software implementations of floating point numbers.
# Might be the basis for a VHDL implementation later on.
# Note that denormals are *not supported* (as in many hardware implementations).

# TODO:
#   1. Add tests
#   2. Multiplication
#   3. Division
#   4. Remainder
#   5. Comparisons
#   6. Conversions to other floating point formats
#   7. Conversions to integers
#   8. Min and max
#   9. Different rounding modes
#  10. Add support for traps and/or flags (see https://docs.oracle.com/cd/E19957-01/806-3568/ncg_handle.html)
#   (maybe: squareroot, trigonometric functions, log?)


class FloatingPointFormat:
	def __init__(self, exponent, mantissa):
		self.exponent = exponent
		self.mantissa = mantissa

def unpack(bits, fmt):
	bias = (1 << (fmt.exponent - 1)) - 1
	sign = bits >> (fmt.exponent + fmt.mantissa)
	exponent = (bits & ((1 << (fmt.exponent + fmt.mantissa)) - 1)) >> fmt.mantissa
	mantissa = (1 << fmt.mantissa) + (bits & ((1 << fmt.mantissa) - 1))
	return (sign, exponent - bias, mantissa)

def pack(unpacked, fmt):
	(sign, exponent, mantissa) = unpacked
	assert (mantissa & (1 << fmt.mantissa)) > 0
	assert mantissa < (1 << (fmt.mantissa + 1))
	bias = (1 << (fmt.exponent - 1)) - 1
	return (sign << (fmt.exponent + fmt.mantissa)) \
	     + (((exponent + bias) & ((1 << fmt.exponent) - 1)) << fmt.mantissa) \
	     + (mantissa & ((1 << fmt.mantissa) - 1))

def is_nan(exponent, mantissa, fmt):
	bias = (1 << (fmt.exponent - 1)) - 1
	return (exponent + bias) == ((1 << fmt.exponent) - 1) and mantissa > 0

def is_inf(exponent, mantissa, fmt):
	bias = (1 << (fmt.exponent - 1)) - 1
	return (exponent + bias) == ((1 << fmt.exponent) - 1) and mantissa == 0

def is_zero(exponent, mantissa, fmt):
	bias = (1 << (fmt.exponent - 1)) - 1
	return (exponent + bias) == 0 and mantissa == 0

def nan_bits(fmt):
	bias = (1 << (fmt.exponent - 1)) - 1
	return pack(0, ((1 << fmt.exponent) - 1) - bias, 0)

def inf_bits(sign, fmt):
	bias = (1 << (fmt.exponent - 1)) - 1
	return pack(sign, ((1 << fmt.exponent) - 1) - bias, 1)

def zero_bits(sign, fmt):
	bias = (1 << (fmt.exponent - 1)) - 1
	return pack(sign, -bias, 0)

def fp_neg(bits, fmt):
	return bits ^ (1 << (1 << (fmt.exponent + fmt.mantissa)))

def fp_sub(bits1, bits2, fmt):
	# Negate second operand and continue with normal addition
	return fp_add(bits1, fp_neg(bits2, fmt)), fmt)

def fp_add(bits1, bits2, fmt):
	
	# Unpack
	(sign1, exponent1, mantissa1) = unpack(bits1, fmt)
	(sign2, exponent2, mantissa2) = unpack(bits2, fmt)
	
	# Handle special cases (NaN, Inf, zero)
	if is_nan(exponent1, mantissa1, fmt) or is_nan(exponent2, mantissa2, fmt):
		return nan_bits(fmt)
	if is_inf(exponent1, mantissa1, fmt) and not(is_inf(exponent2, mantissa2, fmt)):
		return inf_bits(sign1, fmt)
	if not(is_inf(exponent1, mantissa1, fmt)) and is_inf(exponent2, mantissa2, fmt):
		return inf_bits(sign2, fmt)
	if is_inf(exponent1, mantissa1, fmt) and is_inf(exponent2, mantissa2, fmt):
		if sign1 == sign2: return inf_bits(sign1, fmt)
		else: return nan_bits(fmt)
	if is_zero(exponent2, mantissa2, fmt):
		if is_zero(exponent1, mantissa1, fmt):
			# Clear sign bit (that's right, zero is not an identity element
			# when you use IEEE 754 floating point arithmetic)
			return bits1 & (~(1 << (fmt.exponent + fmt.mantissa)))
		return bits1
	if is_zero(exponent1, mantissa1, fmt):
		if is_zero(exponent2, mantissa2, fmt):
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
	mantissa1 <<= 3 # Add three bits (guard, round, sticky) at the end
	mantissa2 <<= 3 # These are for rounding
	
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
		mantissa >>= 1
		exponent += 1
	
	mantissa, g, r = (mantissa >> 3), mantissa & 4, mantissa & 2
	mantissa = round_to_nearest_ties_away_from_zero(mantissa, g, r)
	
	msb = 1 << (fmt.mantissa + 1)
	if mantissa >= 2 * msb:
		mantissa >>= 1
		exponent += 1
	
	return pack((sign, exponent, mantissa), fmt)

def round_to_nearest_ties_away_from_zero(mantissa, g, r):
	if g > 0: return mantissa + 1
	else: return mantissa

def prettyprint(bits, fmt):
	sign, exponent, mantissa = unpack(bits, fmt)
	if is_nan(exponent, mantissa, fmt):
		print('NaN')
		return
	if is_inf(exponent, mantissa, fmt):
		if sign: print('-∞')
		else: print('+∞')
		return
	if is_zero(exponent, mantissa, fmt):
		if sign: print('-0')
		else: print('+0')
		return
	
	output = ('-' if sign == 1 else ' ') + '1.' + bin(mantissa)[3:] + ' x 2^' + str(exponent)
	print(output)

