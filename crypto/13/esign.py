import gmpy
import math

letters ="abcdefghijklmnopqrstuvwxyz  "
def letters_to_num(msg):
    s = ""
    for char in msg:
        n_str = str(letters.index(char) + 1)
        if len(n_str) == 1:
            n_str = "0" + n_str
        s += n_str
    return int(s)

# su salyga kad msg < n
def hash(msg):
    return msg

def sign(msg, p, q, x, k, n):
    w = int(math.ceil(float((hash(msg) - pow(x, k, n)) % n) / float(p * q)))
    y = (w * gmpy.invert((k * pow(x, k - 1)), p)) % p
    s = (x + (y * p * q)) % n
    return s

def verify(msg, s, k, n):
    u = pow(s, k, n)
    z = hash(msg)
    zp = z + pow(2, int(math.ceil(float(math.log(n, 2) * 2.0 / 3.0))))
    if (u >= z) and (zp >= u):
        return True
    else:
        return False

p = int(gmpy.next_prime(30000))
q = int(gmpy.next_prime(25000))

n = pow(p, 2) * q
k = 12
x = 4321
x = 14

# p = 285311670673
# q = 387420499
# n = pow(p, 2) * q
# k = 7
# msg = 31111133 
# x = 45767


msg = letters_to_num("tomas")
# msg = 112233
print "pranesimas: ", msg

signature = sign(msg, p, q, x, k, n)
verified = verify(msg, signature, k, n)
# print verified

print "parasas: ", signature
# print "p =", p
# print "q =", q
print "n =", n
print "k =", k
# print "x =", x
