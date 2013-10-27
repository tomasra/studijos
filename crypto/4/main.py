'''
Created on Sep 25, 2013

@author: tomas
'''
from itertools import chain
    
get_bin = lambda x: x >= 0 and str(bin(x))[2:] or "-" + str(bin(x))[3:]

getBin = lambda x, n: x >= 0 and str(bin(x))[2:].zfill(n) or "-" + str(bin(x))[3:].zfill(n)

def pair_xor(pair1, pair2):
    return [pair1[0] ^ pair2[0], pair1[1] ^ pair2[1]]

def __dec_to_bin(dec):
    return (int)(get_bin(dec))

def rotate_right(num,n):
#     l = get_bin(num)
#     return int(l[-n:] + l[:-n], 2)
#     return str(int(l[-n:] + l[:-n], 2))
    return num[-n:] + num[:-n]

def rotate_left(num,n):
#     l = get_bin(num)
#     return int(l[n:] + l[:n], 2)
#     return str(int(l[n:] + l[:n], 2))
    return num[n:] + num[:n]

def tea_it(m,k):
    sm0=getBin(m[0], 8)
    m1=(int(rotate_left(sm0,2))+k[1])%256
    m2=(int(rotate_right(sm0,2))+k[2])%256 # dn=2^8=256
    m0=(m[0]+k[0])%256
    c=((m0^m1^m2)+m[1])%256
    return [c,m[0]]

def tea_itd(m,k):
    sm0=getBin(m[0], 8)
    m1=(int(rotate_left(sm0,2))+k[1])%256
    m2=(int(rotate_right(sm0,2))+k[2])%256
    m0=(m[0]+k[0])%256
    c=(256-(m0^m1^m2)+m[1])%256
    return [c,m[0]]

def tea(x, key):
    lk1 = (__dec_to_bin(rotate_left(x, 2) + key[1])) % 256
    lk2 = (__dec_to_bin(rotate_right(x, 2) + key[2])) % 256
    lk3 = (x + key[0]) % 256
    l = lk1 ^ lk2 ^ lk3
    return l

def encrypt(pair, key):    
    left = pair[0]
    right = pair[1]
    return [(tea_it(left, key) + right) % 256, left]

def decrypt(pair, key):
    left = pair[0]
    right = pair[1]
    return [right, (left - tea_itd(pair, key)) % 256]

def encrypt_iter(pair, key):
    k0 = [key[0], key[1], key[2]]
    k1 = [key[1], key[2], key[0]]
    k2 = [key[2], key[0], key[1]]
    p0 = tea_it(pair, k0)
    p1 = tea_it(p0, k1)
    p2 = tea_it(p1, k2)
    return [p2[1], p2[0]]
    
def decrypt_iter(pair, key):
    k0 = [key[0], key[1], key[2]]
    k1 = [key[1], key[2], key[0]]
    k2 = [key[2], key[0], key[1]]
    p0 = tea_itd(pair, k2)
    p1 = tea_itd(p0, k1)
    p2 = tea_itd(p1, k0)
#     return p2
    return [p2[1], p2[0]]

def encrypt_ecb(message, key):
    cipher = []
    for m in message:
        cipher.append(encrypt_iter(m, key))
    return cipher

def decrypt_ecb(cipher, key):
    message = []
    for c in cipher:
        message.append(decrypt_iter(c, key))
    return message

def encrypt_cbc(message, key, iv):
    cipher = []
    xor_input = iv    # pradzioje - IV, po to sifro blokai
    for m in message:
        xor_input = encrypt_iter(pair_xor(m, xor_input), key)
        cipher.append(xor_input)
    return cipher
     
def decrypt_cbc(cipher, key, iv):
    message = []
    xor_input = iv
    for c in cipher:
        m = decrypt_iter(c, key)
        message.append(pair_xor(m, xor_input))
        xor_input = c
    return message

def encrypt_ofb(message, key, iv):
    cipher = []
    m_in = iv
    for m in message:
        m_in = encrypt_iter(m_in, key)
        cipher.append(pair_xor(m_in, m))
    return cipher

def decrypt_ofb(cipher, key, iv):
    message = []
    c_in = iv
    for c in cipher:
        c_in = encrypt_iter(c_in, key)
        message.append(pair_xor(c_in, c))
    return message

def blocks_to_str(blocks):
    message = ''
    for c in chain.from_iterable(blocks):
        message += chr(c)
    return message

key = [101, 114, 97]
iv_cbc = [101, 108]
iv_ofb = [109, 97]
# key = [1, 2, 4]
# message = [0, 0]
# encrypted = encrypt_iter(message, key)
# decrypted = decrypt_iter(encrypted, key)
# print(message)
# print(encrypted)
# print(decrypted)

ecb = [[191, 32], [137, 23], [173, 2], [79, 108], [119, 73], [121, 136], [217, 93], [79, 40], [56, 62], [197, 18], [66, 32]]
cbc = [[92, 48], [65, 247], [212, 16], [168, 176], [7, 138], [86, 85], [102, 136], [130, 95], [223, 100], [203, 1]]
ofb = [[251, 24], [84, 196], [1, 232], [250, 109], [229, 88], [99, 27], [199, 52], [98, 109]]

print(blocks_to_str(decrypt_ecb(ecb, key)))
# gerai praleidote laika

print(blocks_to_str(decrypt_cbc(cbc, key, iv_cbc)))
# didelis pasisekimas

print(blocks_to_str(decrypt_ofb(ofb, key, iv_ofb)))
# margas pasaulis

