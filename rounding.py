#!/usr/bin/env python3

rtne = 1     # Round to nearest, ties to even (default)
rtna = 2     # Round to nearest, ties away from zero
inward = 3   # Round toward zero
upward = 4   # Round toward +infinity
downward = 5 # Round toward -infinity

scheme = rtne

def round(sign, mantissa, g, r, s, rounding_scheme = scheme):
	if rounding_scheme == None: rounding_scheme = scheme
	if rounding_scheme == rtne:
		if g > 0 and (r > 0 or s > 0): return mantissa + 1
		elif g == 0: return mantissa
		return mantissa + (mantissa & 1) # tie, round up (in magnitude) only if mantissa is odd
	
	elif rounding_scheme == rtna:
		return mantissa + 1 if g > 0 else mantissa
	
	elif rounding_scheme == inward:
		return mantissa
	
	elif rounding_scheme == upward:
		return mantissa + 1 if sign == 0 and (g > 0 or r > 0 or s > 0) else mantissa
	
	elif rounding_scheme == downward:
		return mantissa + 1 if sign > 0 and (g > 0 or r > 0 or s > 0) else mantissa
	
	assert False
