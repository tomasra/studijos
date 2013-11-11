__author__ = 'tomas'

p = 223092907
v = [41540574, 202450503, 106793425, 63009048, 153417918, 137608372, 94975062, 12564080]
cipher = [157249106, 166325132, 173930021, 166325132, 106793425, 126259402, 166325132, 102342587, 156543129, 173930021, 166325132, 106793425, 7047853, 173930021, 156543129, 173930021]
p_0 = 19


# atvirkstinis skaicius moduliu p
def invmodp(a, p):
    for d in xrange(1, p):
        r = (d * a) % p
        if r == 1:
            break
    else:
        raise ValueError('%d has no inverse mod %d' % (a, p))
    return d

def bits_to_decimal(bits):
    out = 0
    for bit in bits:
        out = (out << 1) | int(bit)
    return out

def find_s(v0, p0, p):
    s = 1
    while True:
        if ((v0 ** s) % p == p0):
            return s
        else:
            s += 1

def decrypt_one(private, c):
    m = ""
    for pr in private:
        if c % pr == 0:
            m += "1"
        else:
            m += "0"
    #print m
    return bits_to_decimal(m)

s = find_s(v[0], p_0, p)

# privatus raktas
private = [(int)(pbl ** s % p) for pbl in v]
#sinv = invmodp(s, p)
sinv = 162249387
t = sinv + (p - 1)

# desifravimas
m = ''.join([chr(decrypt_one(private, (c ** s) % p)) for c in cipher])

#print s, sinv
#print t
print private
print m
