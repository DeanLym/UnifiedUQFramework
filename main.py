from CSimMaster import SimMaster
from CUQMain import *
import numpy as np
import sys

class MySim(SimMaster):
    # def __init__(self):
    #     super(MyUQMain,self).__init__()

    def sim(self, m):
        print("My sim called...")
        d = m[0:5]
        return d


if __name__ == "__main__":
    # print("This is main.")
    nm = 10
    nd = 5
    nr = 5
    mpi_run = True
    my_sim = MySim(nm, nd, mpi_run)
    main = UQMain(nm, nd, nr, UQAlg.EnS, my_sim, mpi_run)
    main.solver.input_m_prior('m_prior.txt')
    main.solve()
    # a = input()
