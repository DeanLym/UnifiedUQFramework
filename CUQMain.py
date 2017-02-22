from UQGlobal import *
from CUQBase import UQBase
from CUQEn import UQEn
from CUQDummy import UQDummy
from mpi4py import MPI


class UQMain:
    def __init__(self, sim_master=None, mpi_run=True):
        self.alg_ = UQAlg.EnS
        self.sim_master_ = sim_master
        self.solver = None
        self.comm = None
        self.num_procs = 1
        self.rank = 0
        self.mpi_run = mpi_run
        if self.mpi_run:
            self.comm = MPI.COMM_WORLD
            self.num_procs = self.comm.Get_size()
            self.rank = self.comm.Get_rank()

    def solve(self):
        if self.rank == 0: # is master
            print(self.alg_)
            if self.alg_ == UQAlg.EnS:
                self.solver = UQEn(1, 1, 1)
                print("EnS")
            if self.alg_ == UQAlg.MCMC:
                print("MCMC")
            self.solver.sim_master_ = self.sim_master_
            self.solver.solve()
        else:
            self.solver = UQDummy()
            self.solver.sim_master_ = self.sim_master_
            self.solver.solve()
            # self.sim_master_.run(self.rank)

    def sim(self):
        print("Sim...")


if __name__ == "__main__":
    main = UQMain()
    main.solve()
