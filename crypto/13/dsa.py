import gmpy

letters ="abcdefghijklmnopqrstuvwxyz  "
def letters_to_num(msg):
    s = ""
    for char in msg:
        n_str = str(letters.index(char) + 1)
        if len(n_str) == 1:
            n_str = "0" + n_str
        s += n_str
    return int(s)

def get_q(p):
    q = 10
    while True:
        q = gmpy.next_prime(q)
        if (p-1) % q == 0:
            return q

def sign(msg, alpha, a, p, q, k):
    gamma = pow(alpha, k, p) % q
    delta = ((msg + a * gamma) * gmpy.invert(k, q)) % q
    return gamma, delta

def verify(msg, alpha, beta, gamma, delta, p, q):
    delta_inv = gmpy.invert(delta, q)
    e1 = (msg * delta_inv) % q
    e2 = (gamma * delta_inv) % q
    left = (pow(alpha, e1, p) * pow(beta, e2, p)) % p
    right = gamma % q
    if ((left % q) == right):
        return True
    else:
        return False

p = gmpy.next_prime(100000)     # 100003
q = get_q(p)                    # 2381

# print "p, q:", p, q

a = 2013
k = 1234
g = 333
# alpha = 1432
alpha = pow(g, ((p-1)/q), p)
beta = pow(alpha, a) % p

msg = letters_to_num("tomas")
# print msg
gamma, delta = sign(msg, alpha, a, p, q, k)

# print "alpha, beta: ", alpha, beta
# print "signature: ", gamma, delta

print "pranesimas:", msg
print "parasas:", gamma, delta
print "alpha =", alpha
print "beta =", beta
# print "gamma =", gamma
# print "delta =", delta
print "p =", p
print "q =", q

verified = verify(msg, alpha, beta, gamma, delta, p, q)
print verified
