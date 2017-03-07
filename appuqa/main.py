import UQGlobal
# Global option for using MPI or not
UQGlobal.UQ_USE_MPI = False
#
from CSimMaster import SimMaster
from CUQMain import *


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
    my_sim = MySim(nm, nd)
    main = UQMain(nm, nd, nr, UQAlg.EnS, my_sim)
    main.solver.input_m_prior('data/m_prior.txt')
    main.solve()
    print(main.solver.d_posterior_)
    # a = input()
