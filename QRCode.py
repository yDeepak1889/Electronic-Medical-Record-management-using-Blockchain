import pyqrcode
import qrtools

class QRCode(object):

	def decodeQR(self, img):
		qr = qrtools.QR()
		qr.decode(img)

		print(qr.data)


c = QRCode()
c.decodeQR('QRCode1.png')