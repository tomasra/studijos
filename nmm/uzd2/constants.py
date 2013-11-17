class Constants:
    n = 20              # erdves rezoliucija - intervalu (ne tasku!) skaicius
    h = 1.0 / n         # zingsnis erdveje
    tau = 0.1           # zingsnis laike
    t_max = 2.0         # galutinis laiko momentas
    beta = 1            # kokia nors konstanta funkcijai F
    delta = 0.001       # netiesines lygciu sistemos sprendimo tikslumas

    # x taskai pagal nurodyta rezoliucija
    x_range = [i * h for i in range(0, n + 1)]

    # pradines algoritmo salygos
    # siuo atveju - pirmos rusies (kappa ir gamma - nuliai)
    kappa, gamma = [0, 0], [0, 0]

    # u^ daugiklis-konstanta, issireikstas pertvarkant NLS i TLS
    u_const = complex(2, -2 * pow(h, 2) / tau)
