import gmpy

p = 21726401
ps = [43452811, 86905607, 173811257]
s = [32588314, 32588284, 32588327]

a = gmpy.invert(ps[1] * ps[2], ps[0])
b = gmpy.invert(ps[0] * ps[2], ps[1])
c = gmpy.invert(ps[0] * ps[1], ps[2])

t0 = s[0] * a * ps[1] * ps[2]
t1 = s[1] * b * ps[0] * ps[2]
t2 = s[2] * c * ps[0] * ps[1]

xs = (t0 + t1 + t2) % (ps[0] * ps[1] * ps[2])
s = xs % p

print s
