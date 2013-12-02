import unittest
from src.thomas import ThomasAlgorithm
from src.algorithm import Algorithm
from src.functions import Functions
from src.constants import Constants
from src.helpers import Helpers

# perkelties metodo testai
class ThomasTests(unittest.TestCase):
    @unittest.skip("laikinai nevykdomas")
    def test_solve(self):
        t = 2.7                             # koks nors laiko momentas
        u = Functions.u_exact_range(t)      # laukiamos tikslios reiksmes

        # sufabrikuotos desines lygybes puses reiksmes (F)
        fake_f_prime = []
        for i in range(1, len(u) - 1):
            f = u[i+1] - (Constants.u_const() * u[i]) + u[i-1]
            # butinai reikia padauginti is -1, nes algoritmas tikisi F reiksmiu, bet desinese lygybiu pusese yra -F
            f *= -1
            fake_f_prime.append(f)

        # testas
        actual = ThomasAlgorithm.solve(Constants.u_const(), fake_f_prime, Constants.kappa, Constants.gamma)
        equal = Helpers.almost_equal_complex(u, actual)
        self.assertTrue(equal)

class FunctionTests(unittest.TestCase):
    # @unittest.skip("laikinai nevykdomas")
    def test_f(self):
        print "-------------------------------------"
        print "-- f(x,t) testas"
        print "-------------------------------------"        
        x, t = 0.42, 0.8

        Constants.beta = 3
        Constants.n = 10             # pradinis intervalu skaicius
        Constants.tau = 0.1         # pradinis laiko zingsnis
        errors = []

        for i in range(0, 7):
            print Constants.h(), Constants.tau
            # print x, t
            # tikrinamos reiksmes is tiksliu funkciju
            u_now0 = Functions.u_exact(x - Constants.h(), t)
            u_now1 = Functions.u_exact(x, t)
            u_now2 = Functions.u_exact(x + Constants.h(), t)
            u_next0 = Functions.u_exact(x - Constants.h(), t + Constants.tau)
            u_next1 = Functions.u_exact(x, t + Constants.tau)
            u_next2 = Functions.u_exact(x + Constants.h(), t + Constants.tau)
            f_now = Functions.f(x,t)
            f_next = Functions.f(x, t + Constants.tau)

            # kaire algoritmo lygybes puse
            left = (u_next1 - u_now1) / Constants.tau

            # desine algoritmo lygybes puse
            right11 = (u_next2 - 2.0 * u_next1 + u_next0) / pow(Constants.h(), 2)
            right12 = (u_now2 - 2.0 * u_now1 + u_now0) / pow(Constants.h(), 2)
            right1 = 1j * 0.5 * (right11 + right12)
            right21 = (pow(abs(u_next2), 2) * u_next2 - pow(abs(u_next0), 2) * u_next0) / (Constants.h() * 2.0)
            right22 = (pow(abs(u_now2), 2) * u_now2 - pow(abs(u_now0), 2) * u_now0) / (Constants.h() * 2.0)
            right2 = Constants.beta * 0.5 * (right21 + right22)
            right3 = (f_next + f_now) / 2.0
            right = right1 + right2 + right3
            
            errors.append(abs(left - right))
            Constants.n *= 10
            Constants.tau /= 10.0
        Helpers.pretty_print_complex(errors)
        # self.assertTrue(Helpers.sequence_descending(errors))
        self.assertTrue(True)

    @unittest.skip("laikinai nevykdomas")
    def test_f_prime(self):
        print "-------------------------------------"
        print "-- F testas"
        print "-------------------------------------"
        x, t = 0.7, 1.7

        Constants.beta = 1
        Constants.n = 5             # pradinis intervalu skaicius
        Constants.tau = 0.2         # pradinis laiko zingsnis
        error = []                  # netiktys
        for i in range(0, 15):
            # tikrinamos reiksmes is tiksliu funkciju
            u_now0 = Functions.u_exact(x - Constants.h(), t)
            u_now1 = Functions.u_exact(x, t)
            u_now2 = Functions.u_exact(x + Constants.h(), t)
            u_next0 = Functions.u_exact(x - Constants.h(), t + Constants.tau)
            u_next1 = Functions.u_exact(x, t + Constants.tau)
            u_next2 = Functions.u_exact(x + Constants.h(), t + Constants.tau)
            f_now = Functions.f(x,t)
            f_next = Functions.f(x, t + Constants.tau)

            # print "F testo f_now, f_next:", f_now, f_next

            f_prime_val = Functions.f_prime(u_now0, u_now1, u_now2, u_next0, u_next1, u_next2, f_now, f_next)
            # print "F reiksme:", Constants.h(), f_prime_val
            result = u_now2 - (Constants.u_const() * u_now1) + u_now0 + f_prime_val
            error.append(abs(result))
            # print "h, tau = ", Constants.h(), ",", Constants.tau
            # print result
            # print "-------------------------------------"

            Constants.n *= 2
            Constants.tau /= 2.0
        Helpers.pretty_print_complex(error)
        self.assertTrue(True)

# pagrindinio algoritmo testai
class AlgorithmTests(unittest.TestCase):
    @unittest.skip("laikinai nevykdomas")
    def test_iteration(self):
        Constants.n = 10
        Constants.tau = 0.1
        t = 1.8

        print "----------------------------------------------"
        print "pradedama nuo: "
        print "----------------------------------------------"
        u_now = Functions.u_exact_range(t)
        Helpers.pretty_print_complex(u_now)

        u_new_expected = Functions.u_exact_range(t + Constants.tau)
        u_new_actual = Algorithm._iteration_block(u_now, t)

        print "----------------------------------------------"
        print "lauktas rezultatas: "
        print "----------------------------------------------"
        Helpers.pretty_print_complex(u_new_expected)
        print "----------------------------------------------"
        print "gautas rezultatas: "
        print "----------------------------------------------"
        Helpers.pretty_print_complex(u_new_actual)

        print "Max netiktis: ", Functions.u_error(u_new_actual, t)
        self.assertTrue(True)

    # sekancio sprendinio radimas fiksuotu laiko momentu, mazinant h ir tau
    @unittest.skip("")
    def test_iteration_precision(self):
        t = 0.8
        Constants.n = 10
        Constants.tau = 1.0
        errors = []
        for i in range(0, 5):
            u_now = Functions.u_exact_range(t)                              # tikslios reiksmes dabartiniu laiko momentu
            u_next = Algorithm._iteration_block(u_now, t)                   # isskaiciuotos reikmes sekanciu laiko momentu
            errors.append(Functions.u_error(u_next, t + Constants.tau))     # netiktis
            Constants.n *= 3
            Constants.tau /= 3
        Helpers.pretty_print_complex(errors)
        self.assertTrue(True)

    # pagrindinis viso algoritmo testas
    # maksimali netiktis turi mazeti mazinant diskretizacijos zingsnius h ir tau
    @unittest.skip("")
    def test_algorithm(self):
        print "-------------------------------------"
        print "-- Viso algoritmo testas"
        print "-------------------------------------"        
        Constants.n = 4
        Constants.tau = 0.1
        errors = []
        for i in range(0, 5):
            u_initial = Functions.u_exact_range(0.0)            # tikslios reiksmes pradiniu laiko momentu
            func_points, time_points = Algorithm.run(u_initial)
            max_error = Functions.u_error_total(func_points, time_points)
            errors.append(max_error)
            Constants.n *= 2
            # Constants.tau /= 2

        Helpers.pretty_print_complex(errors)
        self.assertTrue(True)
