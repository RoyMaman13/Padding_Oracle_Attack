from Cryptodome.Cipher import DES
from Cryptodome.Util.Padding import pad,unpad
import sys

def oracle(ciphertext, key, iv):
    try:
        cipher = DES.new(key, DES.MODE_CBC, iv)
        unpad(cipher.decrypt(ciphertext), DES.block_size)
        return True
    except (ValueError, TypeError):
        return False

def convert_to_byte_array(num):
    if num == 0 :
        return bytes([0])
    else:
        byte_count = (num.bit_length() + 7) // 8
        byte_order = 'big'
        return num.to_bytes(byte_count, byte_order)

def xor(num1, num2, num3):
    num1_bytes = convert_to_byte_array(num1)
    num2_bytes = convert_to_byte_array(num2)
    num3_bytes = convert_to_byte_array(num3)
    result = bytearray(len(num1_bytes))
    for i in range(len(num1_bytes)):
        result[i] = num1_bytes[i] ^ num2_bytes[i] ^ num3_bytes[i]
    if not bytes(result):
        return b'\x00'
    return bytes(result)

def find_xj(c, key, iv, i):
    for k in range(256):
        c = c[:7-i] + bytes([k]) + c[8-i:]
        if oracle(c, key, iv):
            return k


def main():
    ciphertext = bytes.fromhex(sys.argv[1])
    key = (sys.argv[2]).encode()
    iv = bytes.fromhex(sys.argv[3])

    Total_plain_text = bytes()
    total_blocks = int(len(ciphertext)/8)
    # iterating over every block
    for block_ind in range(1, total_blocks+1):
        # c = Xj || Ci
        c = b'\x00\x00\x00\x00\x00\x00\x00\x00' + ciphertext[-8:]
        current_block_plaintext = [None] * 8
        # Need to know if should use Ci-1 or iv
        if block_ind != total_blocks:
            # iterating over every byte              
            for i in range(8):
                # finding Xj[i]
                Xj_i = find_xj(c, key, iv, i)
                # finding the true plaintext byte, P[i] = P'[x]^Ci-1[x]^Xj[x]        
                Pj_i = xor(i+1,ciphertext[len(ciphertext)-9-i], Xj_i)
                current_block_plaintext[7-i] = Pj_i
                # iterating over block X from the end each time to adjust my wish, And setting c to the next round
                for j in range(i+1):            
                    fake_byte = xor(i+2,ciphertext[len(ciphertext)-9-j], int(current_block_plaintext[7-j].hex(), 16))
                    c = c[:7-j] + fake_byte + c[8-j:]
            # when finished adding the block to the final message
            Total_plain_text = (b''.join(current_block_plaintext)) + Total_plain_text
            ciphertext = ciphertext[:-8]
        else:
            # doing the same thing but instead using Ci-1 we will use iv
            for i in range(8):
                Xj_i = find_xj(c, key, iv, i)
                Pj_i = xor(i+1,iv[7-i], Xj_i)
                current_block_plaintext[7-i] = Pj_i

                for j in range(i+1):            
                    fake_byte = xor(i+2,iv[7-j], int(current_block_plaintext[7-j].hex(), 16))
                    c = c[:7-j] + fake_byte + c[8-j:]
            Total_plain_text = (b''.join(current_block_plaintext)) + Total_plain_text

    print(unpad(Total_plain_text, DES.block_size).decode())
    
main()