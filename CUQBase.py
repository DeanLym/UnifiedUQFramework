import numpy as np
from scipy import sparse
from multimethod import multimethod


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

    # @multimethod(np.array)
    # def input_m_prior(self, m_prior):
    #     self.m_prior_ = m_prior
    #     if self.m_prior_.shape[0] != self.nm_ or self.m_prior_.shape[1] != self.nr_:
    #         print("[ERROR] Dimension mismatch for m_prior.")
    #         exit(1)
    #
    # @multimethod(None, str)
    def input_m_prior(self, m_prior_file):
        self.m_prior_ = np.loadtxt(m_prior_file)
        if self.m_prior_.shape[0] != self.nm_ or self.m_prior_.shape[1] != self.nr_:
            print("[ERROR] Dimension mismatch for m_prior.")
            exit(1)

    # @multimethod(np.array)
    def input_d_obs(self, d_obs):
        self.d_obs_ = d_obs
        if self.d_obs_.shape[0] != self.nd_ or self.d_obs_.shape[1] != 1:
            print("[ERROR] Dimension mismatch for d_obs.")
            exit(1)
    #
    # @multimethod(str)
    # def input_d_obs(self, d_obs_file):
    #     self.d_obs_ = np.loadtxt(d_obs_file)
    #     if self.d_obs_.shape[0] != self.nd_ or self.d_obs_.shape[1] != 1:
    #         print("[ERROR] Dimension mismatch for d_obs.")
    #         exit(1)

    def solve(self):
        print("UQBase virtual solve is called.")

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


