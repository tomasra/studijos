import cmath
from constants import Constants

class Functions:
    # funkcija f(x,t)
    @staticmethod
    def f(x, t):
        f1 = (x-1) * x * (cmath.cos(pow(t,2)) - 2 * t * (t + 1j) * cmath.sin(pow(t,2)))
        f2 = 2 * (t + 1j) * cmath.cos(pow(t,2))
        f3 = 3 * (t + 1j) * (pow(t,2) + 1) * pow(x-1, 2) * pow(x, 2) * (2*x-1) * pow(cmath.cos(pow(t,2)), 3)
        return f1 - (1j * f2) - (Constants.beta * f3)

    # tikslaus sprendinio funkcija
    @staticmethod
    def u_exact(x, t):
        return x * (x-1) * (1j + t) * cmath.cos(pow(t, 2))

    # funkcijos f(x,t) reiksmiu masyvas duotu laiko momentu
    @staticmethod
    def f_range(t):
        return [Functions.f(x, t) for x in Constants.x_range()]

    # tikslaus sprendinio masyvas duotu laiko momentu
    @staticmethod
    def u_exact_range(t):
        return [Functions.u_exact(x, t) for x in Constants.x_range()]

    # toliau seka tas gargaras F i kuri netiesiskai ieina u^, f() esamu bei sekanciu laiko momentu ir t.t.
    # zodziu viskas kas lieka desineje TLS lygybes puseje, kai is jos issireiskiami ieskomi u^
    # jei is viso tasku turime n+1, sita funkcija grazins n-1 reiksmiu
    # likusios dvi - is krastiniu salygu
    
    # u_now0, u_now1, u_now2 - atitinkamai: u(j-1), u(j), u(j+1)
    # tas pats ir su u_next
    # f_now - f(x,t) reiksme dabartiniu laiko momentu
    # f_next - f(x,t) reiksme sekanciu laiko momentu
    @staticmethod
    def f_prime(u_now0, u_now1, u_now2, u_next0, u_next1, u_next2, f_now, f_next):
        u_tmp = (pow(abs(u_next2), 2) * u_next2) - (pow(abs(u_next0), 2) * u_next0) + (pow(abs(u_now2), 2) * u_now2) - (pow(abs(u_now0), 2) * u_now0)
        p1 = u_now2 - 2.0 * u_now1 + u_now0
        p2 = -0.5 * Constants.beta * Constants.h() * complex(0,1) * u_tmp 
        p3 = -1.0 * complex(0,1) * pow(Constants.h(), 2) * (f_next + f_now)
        p4 = -2.0 * pow(Constants.h(), 2) * complex(0,1) * u_now1 / Constants.tau
        return p1 + p2 + p3 + p4

    # F reiksmes visam erdves intervalui
    # svarbu: F reiksmiu yra N-2, jei N - erdves tasku skaicius
    @staticmethod
    def f_prime_range(u_now, u_next, f_now, f_next):
        res = []
        for j in range(1, Constants.n):
            u_now0, u_now1, u_now2 = u_now[j-1], u_now[j], u_now[j+1]
            u_next0, u_next1, u_next2 = u_next[j-1], u_next[j], u_next[j+1]
            f_now1, f_next1 = f_now[j], f_next[j]
            res.append(Functions.f_prime(u_now0, u_now1, u_now2, u_next0, u_next1, u_next2, f_now1, f_next1))
        return res

    # netiktis - maksimalus tiksliu ir isskaiciuotu u reiksmiu skirtumas laiko momentu t
    @staticmethod
    def u_error(u_calc, t):
        return max([abs(u_calc[i] - u_exact) for i, u_exact in enumerate(Functions.u_exact_range(t))])

    # maksimali viso algoritmo rezultato netiktis
    @staticmethod
    def u_error_total(u_calc_list, t_list):
        return max([Functions.u_error(u_calc, t_list[i]) for i, u_calc in enumerate(u_calc_list)])
