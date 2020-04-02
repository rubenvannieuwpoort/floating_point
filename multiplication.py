#!/usr/bin/env python3

from common import *
import rounding, format

def mul(bits1, bits2, fmt = format.default, rounding_scheme = None):
	
	# Unpack
	(sign1, exponent1, mantissa1) = fmt.unpack(bits1)
	(sign2, exponent2, mantissa2) = fmt.unpack(bits2)
	
	if fmt.is_nan(bits1) or fmt.is_nan(bits2) or \
	  (fmt.is_inf(bits1) and fmt.is_zero(bits2)) or \
	  (fmt.is_zero(bits1) and fmt.is_inf(bits2)):
		return fmt.nan()
	if fmt.is_inf(bits1) or fmt.is_inf(bits2):
		return fmt.inf(sign1 ^ sign2)
	if fmt.is_zero(bits1) or fmt.is_zero(bits2):
		return fmt.zero(0)
	
	# Align mantissas
	sign = sign1 ^ sign2
	exponent = exponent1 + exponent2
	mantissa = mantissa1 * mantissa2
	
	# TODO: Handle case where exponent out of representable range
	
	# TODO: Handle case where #mantissa_bits < 3
	g = 1 if (mantissa & (1 << (fmt.mantissa - 1))) > 0 else 0
	r = 1 if (mantissa & (1 << (fmt.mantissa - 2))) > 0 else 0
	s = 1 if (mantissa & ((1 << (fmt.mantissa - 2)) - 1)) > 0 else 0
	mantissa = mantissa >> fmt.mantissa
	msb = 1 << fmt.mantissa
	if mantissa > 2 * msb:
		s = s | r
		r = g
		g = mantissa & 1
		mantissa = mantissa >> 1
		exponent = exponent + 1
	
	if exponent > fmt.max_exponent:
		return fmt.inf(sign)
	
	assert (mantissa & msb) > 0
	assert (mantissa < (msb * 2))
	
	mantissa = rounding.round(sign, mantissa, g, r, s, rounding_scheme)
	return fmt.pack(sign, exponent, mantissa)
