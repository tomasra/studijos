from constants import Constants
from functions import Functions
from thomas import ThomasAlgorithm

class Algorithm:
    # maksimalus skirtumas tarp buvusiu ir patikslintu u reiksmiu - a.k.a progresas
    @staticmethod
    def _progress(u_old, u_new):
        return max([abs(u_new[i] - u_old[i]) for i in range(0, Constants.n)])

    # maksimalus apskaiciuotu ir tiksliu u reiksmiu skirtumas nurodytu laiko momentu
    @staticmethod
    def _u_deviation(u, t):
        return max([abs(u[i] - u_exact) for i, u_exact in enumerate(Functions.u_exact_range(t))])

    # u reiksmiu radimas sekanciam laiko momentui
    # sprendziama TLS serija, tikslinant sprendinius iki tam tikro lygio (Constants.delta)
    # u - funkcijos reiksmes dabartiniu laiko momentu
    # t - dabartinis laikas
    @staticmethod
    def _iteration_block(u, t):
        u_old = u                                       # pradinis grubus ivertis sekanciam laiko momentui
        u_new = []                                      # ieskomi sprendiniai
        f = Functions.f_range(t)                        # f(x,t) dabartiniu laiko momentu
        f_next = Functions.f_range(t + Constants.tau)   # f(x,t) sekanciu laiko momentu

        progress = Constants.delta * 2      # gali buti ir kitaip, svarbu kad butu daugiau uz delta
        while (progress >= Constants.delta):
            f_prime = Functions.f_prime(u, u_old, f, f_next)
            # patikslintas sprendinys
            u_new = ThomasAlgorithm.solve(Constants.u_const, f_prime, Constants.kappa, Constants.gamma)
            progress = Algorithm._progress(u_old, u_new)
            u_old = u_new
        return u_new

    # viso algoritmo vykdymas
    @staticmethod
    def run():
        t = 0.0                             # pradinis laiko momentas
        u = Functions.u_exact_range(t)      # pradines u reiksmes (tikslios)
        results = [u]                       # issisaugom visas u reiksmes ir paklaidas
        deviations = [0]                    # pradzioje nulis, nes pradines u reiksmes yra tikslios
        while (t < Constants.t_max):
            u = Algorithm._iteration_block(u, t)
            results.append(u)                                   # rezultatai
            deviations.append(Algorithm._u_deviation(u, t))     # paklaidos
            t += Constants.tau

        # baigta
        return results
