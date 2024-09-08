from Cryptodome.Cipher import DES
from Cryptodome.Util.Padding import pad, unpad
import subprocess


def test(test_id, plaintext, key, iv):
    padded_plaintext = pad(plaintext, DES.block_size)
    cipher = DES.new(key, DES.MODE_CBC, iv)
    ciphertext = cipher.encrypt(padded_plaintext)
    script_command = ['python3', 'ex1.py', str(
        ciphertext.hex()), key.decode(), str(iv.hex())]
    output = subprocess.check_output(script_command, universal_newlines=True)
    try:
        if output[:-1] == plaintext.decode():
            print(u'\N{check mark}',
                  'Pass test {0} successfully! '.format(str(test_id)))
        else:
            print(u'\N{cross mark}', 'Failed test {3}. The arguments are: {0} {1} {2}.'.format(
                str(ciphertext.hex()), key.decode(), str(iv.hex())), test_id)
    except:
        print(u'\N{cross mark}', 'Error occured in test {3}. The arguments are: {0} {1} {2}.'.format(
            str(ciphertext.hex()), key.decode(), str(iv.hex())), test_id)


# tester script for ex1! adjust the arguments as you want :)
test(1, b'Hello World', b'mydeskey', b'00000000')
test(2, b'HelloWorld', b'mydeskey', b'00000000')
test(3, b'HelloWorldHelloWorld', b'mydeskey', b'11111111')
test(4, b'abcdefghijklmnopqrstuvwxyz', b'poaisfun', b'00000000')
test(5, b'Hello', b'mydeskey', b'10101010')
test(6, b'POAPOApoaPOA', b'mysecret', b'00001111')
