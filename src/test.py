from Crypto.Cipher import AES
import Crypto.Random

to = "dsadasdawsds"
to = to.encode('utf-8')
b = "aaaaaaaaaaaaaaaa"
key = bytes(b.encode())

nonce = bytes(b.encode())

cipher = AES.new(key, AES.MODE_EAX, nonce)
to = cipher.encrypt(to)
print(to)
cipher_dec = AES.new(key, AES.MODE_EAX, nonce)
to = cipher_dec.decrypt(to)
print(to.decode('utf-8'))


