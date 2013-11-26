from fractions import gcd

letters ="abcdefghijklmnopqrstuvwxyz  "

public_key = [12016012609141909200527091927191118250205120747, 14, 8180198761799715383015173242285248379954595476]
msg1 = 1921190920091119091305271401112009
sig1 = [11375434029679629258107042215028875613990377667, 6776965161040049534831262026647111547959325828]
msg2 = 1801200109270212151121152009
sig2 = [11375434029679629258107042215028875613990377667, 10612146558353825031634074117648568893035929010]

cipher = [4984032305387956929029725533597245279869845104, 5257659828316931971544780124944522897958103745]

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

def valid_signature(x, public_key, sig):
    left = (pow(public_key[2], sig[0], public_key[0]) * pow(sig[0], sig[1], public_key[0])) % public_key[0]
    right = pow(public_key[1], x, public_key[0])
    if (left == right):
        return True
    else:
        return False

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

def letters_to_num(msg):
    s = ""
    for char in msg:
        n_str = str(letters.index(char) + 1)
        if len(n_str) == 1:
            n_str = "0" + n_str
        s += n_str
    return int(s)

def decrypt_elgamal(c, a, p):
    return (c[1] * pow(modinv(c[0], p), a, p)) % p

def sign_elgamal(a, p, alpha, beta, k, msg):
    gamma = pow(alpha, k, p)
    delta = ((msg - a * k) * modinv(k, p - 1)) % (p - 1)
    return [gamma, delta]

print "Pirmas parasas patikrintas:", valid_signature(msg1, public_key, sig1)
print "Antras parasas patikrintas:", valid_signature(msg2, public_key, sig2)
d = gcd(sig1[1] - sig2[1], public_key[0] - 1)
# print d

p1 = (public_key[0] - 1) / d
a1 = ((sig1[1] - sig2[1]) / d) + p1   # gaunasi neigiamas, todel reikia imti moduli, bet ne siaip moduli su abs, o pridedant p1
b1 = (msg1 - msg2) / d
a1_inv = modinv(a1, p1)
k = (b1 * a1_inv) % p1

while True:
    if (sig1[0] == pow(public_key[1], k, public_key[0])):
        break
    else:
        k += p1

# privataus rakto radimas
pm = public_key[0] - 1
gamma_inv = modinv(sig1[0], pm)

a = ((msg1 - (sig1[1] * k)) * gamma_inv) % pm
print "Algio privatus raktas:", a

message = decrypt_elgamal(cipher, a, public_key[0])
print message
print "Desifruotas pranesimas:", num_to_letters(message)

# suklastotas Algio parasas
msg = letters_to_num("labas")
fake_signature = sign_elgamal(a, public_key[0], public_key[1], public_key[2], k, msg)
print "Suklastotas Algio parasas:", fake_signature
