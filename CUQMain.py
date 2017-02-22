from UQGlobal import *
from CUQBase import UQBase
from CUQEn import UQEn


class UQMain():
    def __init__(self):
        self.alg_ = UQAlg.EnS
        self.solver = None
        self.mpi_run = False

    def solve(self):
        print(self.alg_)
        if self.alg_ == UQAlg.EnS:
            print("EnS")
        if self.alg_ == UQAlg.MCMC:
            print("MCMC")
        self.solver = UQEn(1, 1, 1)
        self.solver.sim_fun = self.sim
        self.solver.mpi_run = self.mpi_run
        self.solver.solve()

    def sim(self):
        print("Sim...")


if __name__ == "__main__":
    main = UQMain()
    main.solve()
