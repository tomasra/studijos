import gmpy

n = 172715641261096853401048362599712313972398900377
e = 1234517253129999781811663939

# r = [int(gmpy.rand('next')) for i in range(0, 5)]
r = [988599573, 330206918, 1368162448, 136093815, 118190388]
m = [100999, 200999, 300999, 250999, 150999]
c = [(m[i] * pow(r[i], e, n)) % n for i in range(0, 5)]
for ci in c:
    print str(ci)

# balsavimas:
# 1. siusti abu pasirasytus biuletenius (biuleteniai pasirasymui) keliant laipsniu d
# 2. visiems rinkejams uzsiregistravus, imti kiekvieno rezultata ir kelti laipsniu e
