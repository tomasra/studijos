import gmpy
import shamir

s = 10863200
p = 21726401
t = 5

def a(s, x, p):
    a = 14      # bet koks
    return (s + a * x) % p

xi = [18, 53, 67, 82, 99]
si = [a(s, x, p) % p for x in xi]

print xi[:t]
print si[:t]
print shamir.find_secret(xi[:t], si[:t], p)
