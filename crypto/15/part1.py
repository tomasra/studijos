import gmpy

p = 239072435685151324847167
q = 7209228505070602643
g = 67332150070409616365263
y = 166738915315590346552185

x = [940110410289, 770903256433, 463764902067, 135167295358, 54468654560, 391148879848, 73429896341, 50755978287, 82248045821, 118191465299]
cipher = [29708035188402105108185, 126943082817005467420944]

s_8 = 6923832041646401739
s_4 = 2074954860875989474

z8 = pow(cipher[0], s_8, p)
z9 = 38190505040432290393541
z4 = pow(cipher[0], s_4, p)

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

def decrypt(cipher, xs, zs, p, q):
    b = []
    for i, xi in enumerate(xs):
        bi = 1
        for j, xj in enumerate(xs):
            if (i != j):
                bi *= xj
                bi *= gmpy.invert(xj - xi, q)
        bi = bi % q
        b.append(bi)    

    z = 1
    for i, bi in enumerate(b):
        z *= pow(zs[i], bi, p)

    msg = cipher[1] * gmpy.invert(z, p) % p
    return num_to_letters(msg)


msg = decrypt(cipher, [x[3], x[7], x[8]], [z4, z8, z9], p, q)
print msg
