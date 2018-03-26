import hashlib

class Util:
	def _to_hex(inp):
		str_inp = str(inp)
		str_inp = str_inp.encode('utf-8')
		return bytearray(str_inp).hex()

	def _hex_hash(inp):
		inp = inp.encode('utf-8')
		return str(hashlib.sha256(inp).hexdigest())

	def get_hash(inp):
		return Util._hex_hash(Util._to_hex(inp))
