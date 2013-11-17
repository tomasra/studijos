__author__ = 'tomas'
import math
import cmath

# triistrizaines tiesiniu lygciu sistemos sprendimas Thomas algoritmu
def tdma_solve(a, b, c, d):
    if len(set([len(a), len(b), len(c), len(d)])) > 1:
        raise Exception("Nesutampa masyvu ilgiai")

    n = len(a)
    if (n == 0):
        raise Exception("Masyvai tusti")

    # tiesiogine eiga - nauji koeficientai
    c_new = []
    d_new = []
    c_new.append(-1.0 * c[0] / b[0])
    d_new.append(d[0] / b[0])

    for i in range(1, n):
        if (i < n - 1):
            c_new.append(-1.0 * c[i] / (a[i] * c_new[i - 1] + b[i]))
        d_new.append((d[i] - d_new[i - 1] * a[i]) / (c_new[i - 1] * a[i] + b[i]))

    # atbuline eiga - sprendiniu surinkimas
    x = [0] * n
    x[n - 1] = d_new[n - 1]
    for i in reversed(range(0, n - 1)):
        x[i] = c_new[i] * x[i + 1] + d_new[i]

    return x

def u(x, t):
    return x * (x - 1.0) * cos(3.0 * t)

def f(x, t, beta):
    f1 = -3.0 * x * (x - 1) * math.sin(3.0 * t)
    f2 = -2.0 * 1j * math.cos(3.0 * t)
    f3 = -3.0 * beta * (x ** 2) * ((x - 1.0) ** 2) * (2.0 * x - 1.0) * math.cos(3.0 * t) ** 3
    return f1 + f2 + f3



# a = [0.0, -1.0, -1.0]
# b = [2.0, 2.0, 2.0]
# c = [-1.0, -1.0, 0.0]
# d = [1.0, 0.0, 1.0]
# x = tdma_solve(a, b, c, d)
# print x

for i in range(0, 10):
    print f(i * 0.1, 0, 1)
