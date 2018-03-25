class Util:
    def _to_hex(self, inp):
		str_inp = str(inp)
		str_inp = str_inp.encode('utf-8')
		return bytearray(str_inp).hex()

	def _hex_hash(self, inp):
		inp = inp.encode('utf-8')
		return str(hashlib.sha256(inp).hexdigest())

    def get_hash
