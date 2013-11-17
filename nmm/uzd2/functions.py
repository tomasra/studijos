import cmath
from constants import Constants

class Functions:
    # funkcija f(x,t)
    @staticmethod
    def f(x, t):
        # f1 = -3 * x * (x - 1) * cmath.sin(3 * t)
        # f2 = complex(-2, 1) * cmath.cos(3 * t)
        # f3 = -3 * Constants.beta * pow(x, 2) * pow(x - 1, 2) * (2 * x - 1) * pow(cmath.cos(3 * t), 3)
        # return f1 + f2 + f3
        f1 = x * (x-1) * -2 * t * cmath.sin(pow(t,2))                                # du/dt
        f2 = 2 * cmath.cos(pow(t,2))                                                 # d^2u/dx^2
        f3 = 3 * pow((x-1),2) * pow(x,2) * (2*x-1) * pow(cmath.cos(pow(t,2)), 2)     # d(|u|^2*u)/dx
        return f1 - complex(0,1) * f2 - Constants.beta * f3

    # tikslaus sprendinio funkcija
    @staticmethod
    def u_exact(x, t):
        # return x * (x - 1) * cmath.cos(3 * t)
        return x * (x-1) * cmath.cos(pow(t, 2))

    # funkcijos f(x,t) reiksmiu masyvas duotu laiko momentu
    @staticmethod
    def f_range(t):
        return [Functions.f(x, t) for x in Constants.x_range]

    # tikslaus sprendinio masyvas duotu laiko momentu
    @staticmethod
    def u_exact_range(t):
        return [Functions.u_exact(x, t) for x in Constants.x_range]

    # toliau seka tas gargaras F i kuri netiesiskai ieina u^, f() esamu bei sekanciu laiko momentu ir t.t.
    # zodziu viskas kas lieka desineje TLS lygybes puseje, kai is jos issireiskiami ieskomi u^
    # jei is viso tasku turime n+1, sita funkcija grazins n-1 reiksmiu
    # likusios dvi - is krastiniu salygu
    
    # u - funkcijos reiksmes dabartiniu laiko momentu (t)
    # u_old - funkcijos reiksmiu tarpiniai iverciai sekanciam laiko momentui (t + tau)
    # f - f(x,t) reiksmes dabartiniu laiko momentu (t)
    # f_next - f(x,t) reiksmes sekanciu laiko momentu (t + tau)
    @staticmethod
    def f_prime(u, u_old, f, f_next):
        res = []
        for i in range(1, Constants.n):
            u0, u1, u2 = u[i-1], u[i], u[i+1]                 # dabartiniai u taskai
            v0, v1, v2 = u_old[i-1], u_old[i], u_old[i+1]     # sekantys u taskai (tikslinami iverciai)
            u_tmp = (pow(abs(v2), 2) * v2) - (pow(abs(v0), 2) * v0) + (pow(abs(u2), 2) * u2) - (pow(abs(u0), 2) * u0)
            
            # p1 = complex(0, 1) * Constants.beta * Constants.h / complex(2, 0) * u_tmp
            # p2 = complex(-1, 0) * (u2 - complex(2, 0) * u1 + u0)
            # p3 = complex(0, 1) * pow(Constants.h, 2) * (f_next[i] + f[i])
            # p4 = complex(0, 2) * pow(Constants.h, 2) * u1 / Constants.tau

            p1 = u2 - 2 * u1 + u0
            p2 = -0.5 * Constants.beta * Constants.h * complex(0,1) * u_tmp 
            p3 = -1 * complex(0,1) * pow(Constants.h, 2) * (f_next[i] + f[i])
            p4 = 2 * pow(Constants.h, 2) * complex(0,1) * u1 / Constants.tau
            res.append(p1 + p2 + p3 + p4)
        return res
