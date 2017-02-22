from CSimMaster import SimMaster
from CUQMain import *
import numpy as np
import sys

class MySim(SimMaster):
    # def __init__(self):
    #     super(MyUQMain,self).__init__()

    def sim(self, m):
        print("My sim called...")
        d = np.zeros((self.nd_,1))
        return


if __name__ == "__main__":
    # print("This is main.")
    nm = 10
    nd = 10
    mpi_run = True
    my_sim = MySim(nm, nd, mpi_run)
    main = UQMain(my_sim, mpi_run)
    # main.init()
    main.alg_ = UQAlg.EnS
    main.solve()
    # a = input()
