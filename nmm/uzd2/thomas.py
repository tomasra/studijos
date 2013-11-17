from constants import Constants

class ThomasAlgorithm:
    # sprendzia tiesiniu lygciu sistema perkelties metodu
    # sistema turi buti tokio pavidalo: 
    # y(j) = a(j+1) * y(j+1) + b(j-1), 

    # argumentai:
    # c - kompleksine konstanta
    # f - F kompleksiniu reiksmiu masyvas
    # kappa, gamma - pradines salygos (reiksmiu poros)
    @staticmethod
    def solve(c, f, kappa, gamma):
        n = Constants.n + 1                 # erdves tasku skaicius (intervalu skaicius + 1)
        y = [complex(0, 0)] * n             # sprendiniai - kompleksiniai skaiciai
        a = [complex(0, 0)] * (n-1)         # alfa koeficientai - pirmam taskui nera
        b = [complex(0, 0)] * (n-1)         # beta koeficientai

        # pirmos alfa ir beta reiksmes - is pradiniu salygu
        a[0] = kappa[0]
        b[0] = gamma[0]

        # kitos alfa ir beta reiksmes
        for i in range(1, n-1):
            a[i] = 1 / (c - a[i-1])
            b[i] = (b[i-1] + f[i-1]) / (c - a[i-1])

        # galinis sprendinys - is pradiniu salygu bei priespaskutinio sprendinio israiskos
        y[n-1] = (gamma[1] + kappa[1] * b[n-2]) / (1 - kappa[1] * a[n-2])

        # atgal
        for i in reversed(range(0, n-1)):
            # skiriasi ab ir y masyvu ilgiai, todel a[i] ir b[i] cia atitinka lygties a(j+1) ir b(j+1)
            y[i] = a[i] * y[i+1] + b[i]

        # baigta
        return y

    # TODO
    # bendras perkelties metodo atvejis
    # a, b, c, d - atitinkami triistrizaines matricos koeficientai
    def solve_generic(a, b, c, d):
        return None
