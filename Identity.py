import scrypt
import pyqrcode


#Code to generate PNG out of QR code object
#big_code.png('code.png', scale=6, module_color=[0, 0, 0, 128], background=[0xff, 0xff, 0xcc])



class Identity(object):
	
	def generateKey(self, password):
		randomSalt = "HelloWorld"
		pubKey = scrypt.hash(password, randomSalt)
		QR = pyqrcode.create(str(pubKey), error='L', version=8, mode='binary')	
		return pubKey, QR


i = Identity()
pubKey, QR = i.generateKey("Hello there")
print(pubKey)

#QR.png('QRCode1.png', scale=6, module_color=[0, 0, 0, 128], background=[0xff, 0xff, 0xcc])