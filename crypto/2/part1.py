'''
Created on Sep 18, 2013

@author: tomas
'''
from itertools import chain

def f(m, k):
    return (m^k)&((k//16)|m) 

def encrypt(message, key):
    cipher = []
    for pair in message:
        left, right = pair[0], pair[1]
        for k in key:
            f_out = f(right, k)
            left = left ^ f_out
            left, right = right, left
        # paskutines iteracijos outputo nereikia apkeisti, tai atkeiciam atgal:
        left, right = right, left
        cipher.append([left, right])
    return cipher

def decrypt(cipher, key):
    # desifruojant raktas apsukamas
    key_rev = key
    key_rev.reverse();
    return encrypt(cipher, key_rev)
    
def blocks_to_str(blocks):
    message = ''
    for c in chain.from_iterable(blocks):
        message += chr(c)
    return message
    
# pirmas
cipher1 = [[103, 96], [114, 101], [115, 37], [114, 97], [105, 110], [97, 118]]
key1 = [69, 82, 65]
message1 = decrypt(cipher1, key1)
print(blocks_to_str(message1))

# antras
# message2 = [[65, 66]]
message2 = [[97, 98]]
key2 = [245, 217]
# print(encrypt(message2, key2))


cipher3 = [[106, 91], [118, 69], [107, 93], [46, 92], [102, 77], [109, 88], [104, 3]]
key3 = [245, 217, 69]
print(blocks_to_str(decrypt(cipher3, key3)))

fo = 8
for i in range(0, 255):
    key = [245, 217, i]
    print i, blocks_to_str(decrypt(cipher3, key))
    
