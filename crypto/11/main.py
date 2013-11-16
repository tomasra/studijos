from fractions import gcd

letters ="abcdefghijklmnopqrstuvwxyz"

n = 2104903025234833471775486482272866481730934732974913
e = 473720615723
d = 720930475171975594380526798111014258055849077148775
rsa_cipher = 121206496725978013967440935883388217378665611169373

algis_n = 2104903025234833471775486482272866481730934732974913
algis_e = 623897610559
algis_rsa_cipher = 1128916061998562807287454311431110681347575254065290
algis_rabin_cipher = 1578706594331054334016039598356012241101007599848149

# atvirkstinis skaicius moduliu p
def invmodp(a, p):
    for d in xrange(1, p):
        r = (d * a) % p
        if r == 1:
            break
    else:
        raise ValueError('%d has no inverse mod %d' % (a, p))
    return d

def egcd(a, b):
    if a == 0:
        return (b, 0, 1)
    else:
        g, y, x = egcd(b % a, a)
        return (g, x - (b // a) * y, y)

def modinv(a, m):
    g, x, y = egcd(a, m)
    if g != 1:
        raise Exception('modular inverse does not exist')
    else:
        return x % m

def num_to_letters(n):
    s = str(n)
    # truksta nulio pradzioje?
    if (len(s) % 2 != 0):
        s = "0" + s

    m = ""
    for i in xrange(0, len(s), 2):
        idx = int(s[i:i + 2])
        if idx <= len(letters):
            m += letters[idx - 1]
        else:
            m += "-"
    return m

def decrypt_rsa(c, d, n):
    m = pow(c, d, n)
    return num_to_letters(m)

def find_t(d, e):
    t = (d * e) - 1
    while True:
        if (t % 2 == 0):
            t = t // 2
        else:
            break
    return t

def find_p(a, t, n):
    i, a_new = 0, 0
    a_old = pow(a, t, n)
    while True:
        a_new = pow(a_old, 2, n)
        if (a_new == 1):
            break
        else:
            a_old = a_new
    return gcd(a_old + 1, n)

def find_algio_d(e, t, n):
    p = find_p(7, t, n)
    q = n / p
    fi = (p - 1) * (q - 1)
    return modinv(e, fi), p, q

def decrypt_rabin(p, q, c):
    n = p * q
    m1 = pow(c, (p + 1) / 4, p)
    m2 = pow(c, (q + 1) / 4, q)
    u = modinv(q, p)
    v = modinv(p, q)
    m_1 = ((m1 * u * q) + (m2 * v * p)) % n
    m_2 = ((m1 * u * q * -1) + (m2 * v * p)) % n
    m_3 = ((m1 * u * q) + (m2 * v * p * -1)) % n
    m_4 = ((m1 * u * q * -1) + (m2 * v * p * -1)) % n
    print m_1
    print m_2
    print m_3
    print m_4
    return num_to_letters(m_1), num_to_letters(m_2), num_to_letters(m_3), num_to_letters(m_4)

print decrypt_rsa(rsa_cipher, d, n)
t = find_t(d, e)
# print t

algio_d, p, q = find_algio_d(algis_e, t, n)
print "algio_d = " + str(algio_d)
print "p = " + str(p) + ", q = " + str(q)
print decrypt_rsa(algis_rsa_cipher, algio_d, n)

# -------------------------------------------------------------
print "Rabino sifras:"
m1, m2, m3, m4 = decrypt_rabin(p, q, algis_rabin_cipher)
print m1
print m2
print m3
print m4

# p = find_p(7, t, n)
# q = n / p
# print "n = " + str(n)
# print "p = " + str(p)
# print "q = " + str(q)
