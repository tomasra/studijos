class Constants:
    n = 10              # erdves rezoliucija - intervalu (ne tasku!) skaicius
    # h = 1.0 / n         # zingsnis erdveje
    tau = 0.1           # zingsnis laike
    t_max = 2.0         # galutinis laiko momentas
    beta = 0            # kokia nors konstanta funkcijai F
    delta = 0.000001      # netiesines lygciu sistemos sprendimo tikslumas

    @staticmethod
    def h():
        return 1.0 / Constants.n

    # x taskai pagal nurodyta rezoliucija
    @staticmethod
    def x_range():
        return [i * Constants.h() for i in range(0, Constants.n + 1)]

    # pradines algoritmo salygos
    # siuo atveju - pirmos rusies (kappa ir gamma - nuliai)
    kappa, gamma = [0, 0], [0, 0]

    # u^ daugiklis-konstanta, issireikstas pertvarkant NLS i TLS
    @staticmethod
    def u_const():
        return 2.0 - (2.0 * pow(Constants.h(), 2) * 1j / Constants.tau)
