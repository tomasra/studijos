import gmpy

p = 3138428376749
x = [2266191296753, 1316255262493, 1198072250506]
s = [838794127471, 936064268135, 2851937681015]
t = 3

def find_secret(x, s, p):
    b = []
    for i, xi in enumerate(x):
        bi = 1
        for j, xj in enumerate(x):
            if (i != j):
                bi *= xj
                bi *= gmpy.invert(xj - xi, p)
        bi = bi % p
        b.append(bi)
    secret = sum([s[i] * b[i] for i in range(0, len(b))]) % p
    return secret

print find_secret(x, s, p)
