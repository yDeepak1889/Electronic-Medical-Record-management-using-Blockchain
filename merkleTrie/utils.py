from operator import itemgetter
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

	def getIndex (ch) :
		if ord(ch) >= ord('a') and ord(ch) <= ord('f'):
			curPos = (ord(ch) - ord('a')) + 10
		else:
			curPos = ord(ch) - ord('0')

		return curPos

	def sortItemBytransID (trans):
		newlist = sorted(trans, key=itemgetter('to'))
		return newlist 
