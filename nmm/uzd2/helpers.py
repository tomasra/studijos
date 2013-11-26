import random

# kelios naudingos funkcijos darbui su kompleksiniu skaiciu masyvais
class Helpers:
    default_error = 1e-10

    # kompleksiniu skaiciu masyvu realiosios ir menamosios dalys
    @staticmethod
    def real_list(cl):
        return [c.real for c in cl]

    @staticmethod
    def imag_list(cl):
        return [c.imag for c in cl]

    # kompleksiniu skaiciu masyvo pagaminimas is dvieju realiu skaiciu masyvu
    @staticmethod
    def new_complex_list(real, imag):
        if (len(real) != len(imag)):
            raise ValueError('Nesutampa masyvu ilgiai')
        return [complex(real[i], imag[i]) for i in range(0, len(real))]

    # kompleksiniu skaiciu masyvu palyginimas
    @staticmethod
    def almost_equal_complex(cl1, cl2, e = default_error):
        r1, r2 = Helpers.real_list(cl1), Helpers.real_list(cl2)
        i1, i2 = Helpers.imag_list(cl1), Helpers.imag_list(cl2)
        return Helpers.almost_equal_float(r1, r2, e) & Helpers.almost_equal_float(i1, i2, e)

    # realiu skaiciu masyvu palyginimas
    # e - mazas skaicius, leistina paklaida
    @staticmethod
    def almost_equal_float(l1, l2, e = default_error):
        if (len(l1) != len(l2)):        # masyvu ilgiai turi sutapti
            raise ValueError('Nesutampa masyvu ilgiai')

        err_count = [i for i in range(0, len(l1)) if abs(l1[i] - l2[i]) > e]
        if len(err_count) > 0:          # atsirado skaiciu kurie skiriasi daugiau nei per e
            return False
        else:
            return True

    # siek tiek randomizuoja realiu skaiciu masyva, pridedant arba atimant po nedidele reiksme
    @staticmethod
    def randomize_list_float(l, e = 1e-1):
        return [a + random.uniform(-1*e, e) for a in l]

    # spausdinimas
    @staticmethod
    def pretty_print_complex(l):
        for c in l:
            print [c.real, c.imag]

    # ar seka mazejanti
    @staticmethod
    def sequence_descending(s):
        for i in range(1, len(s)):
            if s[i] > s[i-1]:
                return False
        return True
