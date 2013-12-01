from mpi4py import MPI
from src.constants import Constants
from src.functions import Functions
from src.algorithm import Algorithm

# kiek kartu bus mazinami zingsniai ir vykdomas algoritmas
runs = 6

# skirtingu parametru rinkinys
def create_params():
    params_h, params_tau = [], []               # erdves ir laiko zingsniai
    for i in range(0, runs):
        h = 0.2 / pow(2, i)
        tau = 0.2 / pow(2, i)
        params_h.append(h)
        params_tau.append(tau)
    return params_h, params_tau    

# algoritmo vykdymas
def run(h, tau):
    Constants.n = int(1.0 / h)
    Constants.tau = tau
    u_initial = Functions.u_exact_range(0)
    func_points, time_points = Algorithm.run(u_initial)
    error_total = Functions.u_error_total(func_points, time_points)
    return error_total

comm = MPI.COMM_WORLD
proc_id = comm.Get_rank()
workers = comm.Get_size() - 1                   # skaiciavimo procesu skaicius

# pagrindinis procesas skirstantis darbus kitiems
if (proc_id == 0):
    started, finished = 0, 0                    # skaiciavimu progresas
    results = [0.0] * runs                      # rezultatai - netiktys su skirtingais h ir tau
    params_h, params_tau = create_params()

    for i in range(0, min(runs, workers)):      # pradzioj isdalijami darbai visiems procesams
        worker_id = i + 1                       # skaiciavimu procesu ID'ai prasideda nuo vieneto
        comm.send(True, dest = worker_id)       # informuojam procesa apie siunciama nauja uzduoti
        comm.send({'h': params_h[started], 'tau': params_tau[started]}, dest = worker_id, tag = started)
        started += 1

    while (finished < runs):
        st = MPI.Status()                       # gauto pranesimo statusas su siuntejo ID
        result = comm.recv(source = MPI.ANY_SOURCE, tag = MPI.ANY_TAG, status = st)
        results[st.tag] = result
        finished += 1
        
        # jei dar yra like darbu - duodamas naujas darbas procesui kuris savo ka tik baige
        if (started < runs):
            comm.send(True, dest = st.source)
            comm.send({'h': params_h[started], 'tau': params_tau[started]}, dest = st.source, tag = started)
            started += 1

        # jei ne, visiem procesams pranesam kad darbas baigtas
        if (finished == runs):
            for i in range(1, workers + 1):
                comm.send(False, dest = i)

    # baigta, viska isspausdinam
    for i in range(0, runs):
        print "h = %.5f, tau = %.5f, netiktis: %.10f" % (params_h[i], params_tau[i], results[i])

# salutinis procesas skaiciavimams
else:
    while (True):
        more_work = comm.recv(source = 0)
        if (more_work):
            st = MPI.Status()
            task = comm.recv(source = 0, tag = MPI.ANY_TAG, status = st)
            result = run(task['h'], task['tau'])                    # algoritmo vykdymas
            comm.send(result, dest = 0, tag = st.tag)
        else:
            break
