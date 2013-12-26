import gmpy

bt = [154548578950615559181444, 30569435350143066472799, 109031095432736362241622, 35448298417168930888219, 165951977248246428756278, 135036879337527364949950, 113626874926796075840884, 125677764525961286522470, 59690354315375193893398, 119799271284916809065529]

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

letters ="abcdefghijklmnopqrstuvwxyz  "
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

p, q = 239072435685151324847167, 7209228505070602643
gamma, delta = [1702066632772176684, 474452932680040502]
a = 5042000814892294844
x = 11012009140119

k = ((x + a * gamma) * gmpy.invert(delta, q)) % q
print k
print num_to_letters(k)

# todo: alpha = g (pirmos dalies)?
