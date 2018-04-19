
from Crypto.PublicKey import RSA
from Crypto import Random as rnd


class KeyPair(object):

    '''Generates a key pair and returns the RSA Object'''
    def gen_keyPair(self):
        random_gen = rnd.new().read
        key = RSA.generate(1024, random_gen)

        return key

    '''Encrypts the data and returns the encrypted data'''
    def encrypt_data(self, key, data):
        pub_key = key.publickey()
        enc_data = pub_key.encrypt(data, 32)

        return enc_data

    '''Decrypts the data and returns the original data'''
    def decrypt_data(self, key, enc_data):
        data = key.decrypt(enc_data)
        return data

'''
Tests :-

k = KeyPair()
key = k.gen_keyPair()
key1 = k.gen_keyPair()
print(key)
enc_data = k.encrypt_data(key,b'Hello')
print(k.decrypt_data(key1, enc_data))

'''
