try:
    from .UQGlobal import *
    from .CUQEnS import UQEnS
    from .CUQDummy import UQDummy
    from .CUQESMDA import UQESMDA
    from .CUQEnKF import UQEnKF
except():
    from UQGlobal import *
    from CUQEnS import UQEnS
    from CUQDummy import UQDummy
    from CUQESMDA import UQESMDA
    from CUQEnKF import UQEnKF
if UQ_USE_MPI:
    from mpi4py import MPI
import sys


class UQMain:
    def __init__(self, nm, nd, nr, alg, np=1, sim_master=None):
        self.nm_ = nm
        self.nd_ = nd
        self.nr_ = nr
        self.np_ = np
        self.sim_master_ = sim_master
        self.alg_ = alg
        self.solver = None
        self.comm = None
        self.num_procs = 1
        self.rank = 0
        if UQ_USE_MPI:
            self.comm = MPI.COMM_WORLD
            self.num_procs = self.comm.Get_size()
            self.rank = self.comm.Get_rank()
        self.init_solver()

    def init_solver(self):
        if self.rank == 0:
            # Master processor
            self.solver = {
                UQAlg.EnS: UQEnS(self.nm_, self.nd_, self.nr_),
                UQAlg.ES_MDA: UQESMDA(self.nm_, self.nd_, self.nr_),
                UQAlg.EnKF: UQEnKF(self.nm_, self.nd_, self.nr_, self.np_)
                # UQAlg.MCMC: None,
                # To be complete
            }.get(self.alg_, None)
        else:
            # Dummy solver for the slave processors
            self.solver = UQDummy()
        self.solver.sim_master_ = self.sim_master_

    def solve(self):
        if self.solver is not None:
            self.solver.solve()
        else:
            sys.exit(1)


if __name__ == "__main__":
    main = UQMain()
    main.solve()
