from Cryptodome.Cipher import DES
from Cryptodome.Util.Padding import pad,unpad
import sys
import binascii

plaintext = b'Roy'
iv = '3faf089c7a924a7b'
padded_plaintext = pad(plaintext, 8)
ciphertext = DES.new(b'greatkey', DES.MODE_CBC,bytes.fromhex(iv)).encrypt(padded_plaintext)
print(ciphertext.hex())