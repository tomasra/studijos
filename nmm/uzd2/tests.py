import unittest
from thomas import ThomasAlgorithm
# from algorithm import Algorithm
from functions import Functions
from constants import Constants
from helpers import Helpers

# perkelties metodo testai
class ThomasTests(unittest.TestCase):
    def testSolve(self):
        t = 2.7                             # koks nors laiko momentas
        u = Functions.u_exact_range(t)      # laukiamos tikslios reiksmes

        # sufabrikuotos desines lygybes puses reiksmes (F)
        fake_f_prime = []
        for i in range(1, len(u) - 1):
            f = u[i+1] - (Constants.u_const * u[i]) + u[i-1]
            # butinai reikia padauginti is -1, nes algoritmas tikisi F reiksmiu, bet desinese lygybiu pusese yra -F
            f *= -1
            fake_f_prime.append(f)

        # testas
        actual = ThomasAlgorithm.solve(Constants.u_const, fake_f_prime, Constants.kappa, Constants.gamma)
        equal = Helpers.almost_equal_complex(u, actual)
        self.assertTrue(equal)
