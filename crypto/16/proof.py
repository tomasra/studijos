import gmpy

p,g_1,g_2 = 129746337890647, 102, 204
x,y_1,y_2 = 193139816415, 92977709205453, 113088046585719

print(pow(g_1, x, p))
print(pow(g_2, x, p))

# x - 2as elementas
# v1, v2, w = gmpy.rand('next'), gmpy.rand('next'), gmpy.rand('next')
v1, v2, w = 988599573 330206918 1368162448

print v1, v2, w

