# kelios naudingos funkcijos darbui su kompleksiniu skaiciu masyvais
class Helpers:
    # kompleksiniu skaiciu masyvu realiosios ir menamosios dalys
    @staticmethod
    def real_list(cl):
        return [c.real for c in cl]

    @staticmethod
    def imag_list(cl):
        return [c.imag for c in cl]

    # kompleksiniu skaiciu masyvu palyginimas
    @staticmethod
    def almost_equal_complex(cl1, cl2):
        r1, r2 = Helpers.real_list(cl1), Helpers.real_list(cl2)
        i1, i2 = Helpers.imag_list(cl1), Helpers.imag_list(cl2)
        return Helpers.almost_equal_float(r1, r2) & Helpers.almost_equal_float(i1, i2)

    # realiu skaiciu masyvu palyginimas
    @staticmethod
    def almost_equal_float(l1, l2):
        e = 1e-10                       # mazas skaicius - paklaida
        if (len(l1) != len(l2)):        # masyvu ilgiai turi sutapti
            raise ValueError('Nesutampa masyvu ilgiai')

        err_count = [i for i in range(0, len(l1)) if abs(l1[i] - l2[i]) > e]
        if len(err_count) > 0:          # atsirado skaiciu kurie skiriasi daugiau nei per e
            return False
        else:
            return True
