'''
Created on 2013 rugs. 11

@author: tomas_000
'''

set='ABCDEFGHIJKLMNOPQRSTUVWXYZ'
lambda_1=[10, 2, 21, 18, 23, 6, 16, 14, 8, 11, 1, 25, 15, 20, 0, 24, 17, 19, 22, 5, 4, 3, 9, 12, 13, 7]
lambda_2=[20, 3, 24, 18, 8, 5, 15, 4, 7, 11, 0, 13, 9, 22, 12, 23, 10, 1, 19, 21, 17, 16, 2, 25, 6, 14]
key=[13, 12]
cipher=[17, 18, 1, 4, 12, 6, 25, 8, 1, 22, 15, 10, 17, 23, 11, 8, 6, 24, 18, 14, 18, 24, 13, 1, 2, 20, 4, 17, 22, 25, 3, 23, 8, 9, 12, 11, 15, 12, 3, 22, 22, 2, 8, 19, 2, 8, 21, 10, 1, 5, 14, 14, 8, 16, 11, 25]

def lambda_1(c):
    return lambda_1[c]

def lambda_1_inv(c):
    return lambda_1.index(c)

def lambda_2(c):
    return lambda_2[c]

def lambda_2_inv(c):
    return lambda_2.index(c)

def ro(c, m):
    return (c + m) % len(set)
    
def decrypt(c, k):
    m1 = k % len(set)
    m2 = k // len(set)
    k1, k2 = key[0], key[1]
    c0 = ro(c, m2 + k2)
    c1 = lambda_2_inv(c0)
    c2 = ro(c1, 0 - m2 - k2)
    c3 = ro(c2, m1 + k1)
    c4 = lambda_1_inv(c3)
    c5 = ro(c4, 0 - m1 - k1)
    return c5
    
rez = ''
for i in range(0, len(cipher) - 1):
    d = decrypt(cipher[i], i)
    rez += set[d]
    
print(rez)
