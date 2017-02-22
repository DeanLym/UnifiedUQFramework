import numpy as np
from scipy import sparse


class UQBase:
    def __init__(self, nm=1, nd=1, nr=1):
        self.nm_ = nm
        self.nd_ = nd
        self.nr_ = nr
        self.d_obs_ = np.zeros((nd, 1))
        self.m_prior_ = np.zeros((nm, nr))
        self.d_prior_ = np.zeros((nd, nr))
        self.m_posterior_ = np.zeros((nm, nr))
        self.d_posterior_ = np.zeros((nd, nr))
        self.cd_ = sparse.eye(nd)
        self.cm_ = sparse.eye(nm)
        self.sim_master_ = None
        self.mpi_run = False

    def solve(self):
        print("UQBase solve is called.")

    # def solve(self):
    #     self.m_posterior_ = np.zeros((self.nm_, self.nr_))
    #     self.d_posterior_ = np.zeros((self.nd_, self.nr_))

    # def simulate(self, m, nr):
    #     # m: matrix of nm_ * nr_
    #     d = np.zeros(self.nd_, nr)
    #     return d
    #
    # def data_mismatch(self):



# uq = UQBase(10,10)
# print(uq.alg_)


