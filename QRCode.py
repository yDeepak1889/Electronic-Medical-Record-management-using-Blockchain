import pyqrcode
from qrtools.qrtools import QR

class QRCode(object):

	def decodeQR(self, img):
		qr = QR(filename = 'QRCode1.png')
		qr.decode()
		print qr.data 


c = QRCode()
c.decodeQR('QRCode1.png')