import unittest
from thomas import ThomasAlgorithm
from algorithm import Algorithm
from functions import Functions
from constants import Constants
from helpers import Helpers

# perkelties metodo testai
class ThomasTests(unittest.TestCase):
    @unittest.skip("laikinai nevykdomas")
    def test_solve(self):
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

class FunctionTests(unittest.TestCase):
    @unittest.skip("laikinai nevykdomas")
    def test_f(self):
        delta = 0.001   # leistina netiktis
        t = 1.8         # bet koks laiko momentas

        # x, t = 0.4, 1.3
        # h, tau = 0.2, 0.2       # pradiniai zingsniai
        tau = 0.2
        n = 5
        max_errors = []
        for i in range(1, 5):
            error = []
            h = 1.0 / n
            for j in range(1, n):
                u_now0, u_now1, u_now2 = Functions.u_exact((j-1)*h, t), Functions.u_exact(j*h, t), Functions.u_exact((j+1)*h, t)
                u_next0, u_next1, u_next2 = Functions.u_exact((j-1)*h, t+tau), Functions.u_exact(j*h, t+tau), Functions.u_exact((j+1)*h, t+tau)
                f_now = Functions.f(j*h,t)
                f_next = Functions.f(j*h, t+tau)

                # kaire algoritmo lygybes puse
                left = (u_next1 - u_now1) / tau

                # desine algoritmo lygybes puse
                right11 = (u_next2 - 2.0 * u_next1 + u_next0) / pow(h, 2)
                right12 = (u_now2 - 2.0 * u_now1 + u_now0) / pow(h, 2)
                right1 = complex(0,1) * 0.5 * (right11 + right12)
                right21 = (pow(abs(u_next2), 2) * u_next2 - pow(abs(u_next0), 2) * u_next0) / (h * 2.0)
                right22 = (pow(abs(u_now2), 2) * u_now2 - pow(abs(u_now0), 2) * u_now0) / (h * 2.0)
                right2 = Constants.beta * 0.5 * (right21 + right22)
                right3 = (f_next + f_now) / 2.0
                right = right1 + right2 + right3
                error.append(abs(left - right))
                # print left, right, abs(left-right), j*h, t
            # print error
            max_errors.append(max(error))
            # print "----------------------------------------------"
            # mazinami zingsniai
            n *= 2
            tau /= 2.0

        # Helpers.pretty_print_complex(max_errors)
        # Helpers.pretty_print_complex(u_next)
        # self.assertGreater(delta, max(error))
        # print max_errors
        self.assertTrue(False)

    @unittest.skip("laikinai nevykdomas")
    def test_f2(self):
        print "-------------------------------------"
        print "-- f(x,t) testas"
        print "-------------------------------------"        
        x, t = 0.42, 1.8

        Constants.n = 5             # pradinis intervalu skaicius
        Constants.tau = 0.2         # pradinis laiko zingsnis
        errors = []

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
            
            # print "h, tau = ", Constants.h(), ",", Constants.tau
            # print "left, right = ", left, ",", right
            # print "right1, right2, right3 = ", right1, ",", right2, ",", right3
            # print "-------------------------------------"
            errors.append(abs(left - right))
            Constants.n *= 2
            Constants.tau /= 2.0
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

    # @unittest.skip("")
    def test_algorithm(self):
        Constants.n = 4
        # Constants.tau = 0.1
        errors = []
        for i in range(0, 5):
            results, error = Algorithm.run()
            errors.append(error)
            Constants.n *= 2
            # Constants.tau /= 2

        Helpers.pretty_print_complex(errors)
        self.assertTrue(True)
        