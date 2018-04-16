from npre import bbs98

pre = bbs98.PRE()

#sk_x, pk_x denotes secret key and public key of User x.

sk_a = pre.gen_priv(dtype=bytes)
pk_a = pre.priv2pub(sk_a)

sk_b = pre.gen_priv(dtype=bytes)
pk_b = pre.priv2pub(sk_b)

#To be used as an input to proxy reencryption function
passphrase = pre.gen_priv(dtype=bytes)


#Let's encrypt msg with pk_a
msg = b'Hello world'
emsg = pre.encrypt(pk_a, msg)

#The reencryption key generation function needs two inputs :- 1. secret key of User a, another key (any random passphrase)
reencrypt_key = pre.rekey(sk_a, passphrase)
emsg_reencrypted = pre.reencrypt(reencrypt_key, emsg)


#Check if b can decrypt the reencrypted msg without the reencryption reencrypt_key
if(msg == pre.decrypt(sk_b, emsg_reencrypted)):
    print("It can!")
else:
    print("Nope! Not a chance")


#Decrypt reencrypted msg using the reencrypt_key
e  = pre.decrypt(passphrase, emsg_reencrypted)
print(e)
