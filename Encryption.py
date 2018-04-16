from cryptography.fernet import Fernet as ft

class Encryption(object):

    '''takes the data to be encrypted during initialization'''
    def __init__(self, data=None):
        self.data = data

    '''encrypts the given data and returns the key and encrypted_data'''
    def encrypt(self):
        key = ft.generate_key()
        f = ft(key)
        encrypted_data = f.encrypt(self.data)

        return encrypted_data, key

    '''takes encrypted_data and key, returns decrypted data'''
    def decrypt(self, encrypted_data, key):
        f = ft(key)
        data = f.decrypt(encrypted_data)

        return data

'''
e = Encryption(b"Hello World")
token, key = e.encrypt()
print(e.decrypt(token, key))

f = Encryption(b"Hey")
token1, key = f.encrypt()

print(e.decrypt(token,key))
'''
