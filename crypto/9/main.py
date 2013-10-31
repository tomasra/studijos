'''
Created on Oct 30, 2013

@author: tomas
'''

import fractions

def bits_to_decimal(bits):
    out = 0
    for bit in bits:
        out = (out << 1) | int(bit)
    return out

# atvirkstinis skaicius moduliu p
def invmodp(a, p):
    for d in xrange(1, p):
        r = (d * a) % p
        if r == 1:
            break
    else:
        raise ValueError('%d has no inverse mod %d' % (a, p))
    return d

# iskrausto kuprine pagal duota rakta ir grazina 1 baita
def decrypt_bag(c, key):
    m = [0] * 8
    for i, k in reversed(list(enumerate(key))):
        if k <= c:
            c -= k
            m[i] = 1
    return bits_to_decimal(m)       
            

public = [134878, 89630, 189849, 91995, 52230, 140919, 108445, 96683]
private1 = 1064
p = 194330
cipher = [479919, 609076, 420398, 517081, 581073, 576602, 189849, 620838, 376162, 536837, 376162, 479919, 376162, 576602, 189849, 620838, 517081, 576602, 609076, 576602]


d = fractions.gcd(public[0], p)
vs = invmodp(public[0] / d, p / d)

s = vs * (private1 / d)
s2 = s + p / d


# sparciai didejanti seka - privatus raktas
private = []
for publ in public:
    private.append((publ * s2) % p)

# desifravimas
message = ""
for c in cipher:
    cs = (c * s2) % p
    m = decrypt_bag(cs, private)
    message += chr(m)
    
print private
print message
