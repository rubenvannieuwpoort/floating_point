#!/usr/bin/env python3

class FloatingPointFormat:
	def __init__(self, exponent, mantissa):
		self.exponent = exponent
		self.mantissa = mantissa
		self.bias = (1 << (self.exponent - 1)) - 1
		self.min_exponent = -self.bias
		self.max_exponent = (1 << exponent) - 1 - self.bias - 1
	
	def unpack(self, bits):
		sign = bits >> (self.exponent + self.mantissa)
		exponent = (bits & ((1 << (self.exponent + self.mantissa)) - 1)) >> self.mantissa
		mantissa = (1 << self.mantissa) + (bits & ((1 << self.mantissa) - 1))
		return (sign, exponent - self.bias, mantissa)
	
	def pack(self, sign, exponent, mantissa):
		#assert (mantissa & (1 << self.mantissa)) > 0 #TODO: can also be inf or nan
		assert mantissa < (1 << (self.mantissa + 1))
		return (sign << (self.exponent + self.mantissa)) \
			 + (((exponent + self.bias) & ((1 << self.exponent) - 1)) << self.mantissa) \
			 + (mantissa & ((1 << self.mantissa) - 1))
	
	def is_nan(self, bits):
		sign, exponent, mantissa = self.unpack(bits)
		return exponent == self.max_exponent + 1 and mantissa > 0
	
	def is_inf(self, bits):
		sign, exponent, mantissa = self.unpack(bits)
		return exponent == self.max_exponent + 1 and mantissa == 0
	
	def is_zero(self, bits):
		sign, exponent, mantissa = self.unpack(bits)
		return (exponent + self.bias) == 0 and mantissa == 0
	
	def nan(self):
		return self.pack(0, ((1 << self.exponent) - 1) - self.bias, 1)
	
	def inf(self, sign = 0):
		return self.pack(sign, ((1 << self.exponent) - 1) - self.bias, 0)
	
	def zero(self, sign = 0):
		return self.pack(sign, -self.bias, 0)
	
	def format(self, bits):
		sign, exponent, mantissa = self.unpack(bits)
		if self.is_nan(bits):
			return 'NaN'
		if self.is_inf(bits):
			if sign: return '-∞'
			else: return '+∞'
			return
		if self.is_zero(bits):
			if sign: return '-0'
			else: return '+0'
			return
		
		return ('-' if sign == 1 else ' ') + '1.' + bin(mantissa)[3:] + ' x 2^' + str(exponent)

binary32 = FloatingPointFormat(8, 23)
default = binary32

