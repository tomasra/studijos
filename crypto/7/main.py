'''
Created on Oct 16, 2013

@author: tomas
'''

def pair_xor(a, b):
    return [a[0] ^ b[0], a[1] ^ b[1]]

def rotate_right(num,n):
    return num[-n:] + num[:-n]

def rotate_left(num,n):
    return num[n:] + num[:n]

getBin = lambda x, n: x >= 0 and str(bin(x))[2:].zfill(n) or "-" + str(bin(x))[3:].zfill(n)

def bits_to_decimal(bits):
    out = 0
    for bit in bits:
        out = (out << 1) | int(bit)
    return out

def tea_it(m,k):
    dn=256
    sm0=getBin(m[0],8)
    m1=(int(rotate_left(sm0,2),2)+k)%dn
    m2=(int(rotate_right(sm0,2),2)+k)%dn
    m0=(m[0]+k)%dn
    c=((m0^m1^m2)+m[1])%dn
    return [c,m[0]]

def encrypt(m, k):
    return tea_it(tea_it(m, k[0]), k[1])

def hash1(message, h0):
    rez = encrypt(message[0], h0)
    for i in range(1, len(message)):
        rez = encrypt(message[i], pair_xor(message[i], rez))
    return rez

def hash2(message, h0):
    e_in = pair_xor(message[0], h0)
    rez = encrypt(e_in, e_in)
    for i in range(1, len(message)):
        e_in = pair_xor(rez, message[i])
        rez = encrypt(e_in, e_in)
    return rez
    

# pirmas variantas
p = [[116, 111], [109, 114], [97, 105]]
x = [[1, 1]]
h0 = [88, 88]
print "h0 =", h0, "\n"

h_star3 = hash1(x, h0)
b = [pair_xor(h0, h_star3)]

u1 = x + b + p
u2 = b + p

print("pirmas variantas")
print u1, " => ", hash1(u1, h0)
print u2, " => ", hash1(u2, h0)


# antras variantas
x = [[66, 66]]
z = [[77, 77]]

h_star = hash2(p, h0)
h_star2 = hash2(p + x, h0)
y = [pair_xor(pair_xor(h_star, h_star2), z[0])]

u1 = p + x + y
u2 = p + z

print
print("antras variantas")
print u1, " => ", hash2(u1, h0)
print u2, " => ", hash2(u2, h0) 
