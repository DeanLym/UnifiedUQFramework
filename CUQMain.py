from UQGlobal import *
from CUQBase import UQBase
from CUQEn import UQEn
from CUQDummy import UQDummy
from mpi4py import MPI
import sys


class UQMain:
    def __init__(self, nm, nd, nr, alg, sim_master=None, mpi_run=True):
        self.nm_ = nm
        self.nd_ = nd
        self.nr_ = nr
        self.sim_master_ = sim_master
        self.mpi_run = mpi_run
        self.alg_ = alg
        self.solver = None
        self.comm = None
        self.num_procs = 1
        self.rank = 0
        if self.mpi_run:
            self.comm = MPI.COMM_WORLD
            self.num_procs = self.comm.Get_size()
            self.rank = self.comm.Get_rank()
        self.init_solver()

    def init_solver(self):
        if self.rank == 0:
            # Master processor
            self.solver = {
                UQAlg.EnS: UQEn(self.nm_, self.nd_, self.nr_),
                UQAlg.MCMC: None,
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
