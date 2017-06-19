try:
    from .CUQEn import UQEn
except():
    from CUQEn import UQEn
import numpy as npy


class UQESMDA(UQEn):
    def __init__(self, nm=1, nd=1, nr=1):
        super(UQESMDA, self).__init__(nm, nd, nr)
        self.na_ = 1
        self.i_na_ = 0
        self.alpha_ = npy.ones((self.na_, 1)) * self.na_

    def input_na(self, na: int):
        self.na_ = na
        if self.na_ < 1:
            print('[ERROR] Invalid Na value')
            exit(1)

    def input_alpha(self, alpha: npy.ndarray):
        self.alpha_ = alpha
        if npy.abs(npy.sum(1/self.alpha_) - 1) > 1e-3:
            print('[ERROR] Sum of multiplication coefficients not equal to 1.')
            exit(1)

    def initialize(self):
        self.m_k_ = npy.copy(self.m_prior_)

    def perturb_observation(self):
        for i in range(0, self.nr_):
            self.d_uc_[:, i] = self.d_obs_ + \
                               npy.random.multivariate_normal(npy.zeros(self.nd_), self.alpha_[self.i_na_] * self.cd_, 1)

    def update(self):
        self.perturb_observation()
        npy.savetxt('duc_' + str(self.i_na_), self.d_uc_)
        npy.savetxt('mf_' + str(self.i_na_), self.m_k_)
        npy.savetxt('d_' + str(self.i_na_), self.d_k_)
        m_ave = npy.mean(self.m_k_, 1, keepdims=True)
        d_ave = npy.mean(self.d_k_, 1, keepdims=True)
        ones = npy.ones((1, self.nr_))
        self.cmd_ = npy.dot(self.m_k_ - npy.dot(m_ave, ones),
                            npy.transpose(self.d_k_ - npy.dot(d_ave, ones))) / (self.nr_ - 1)
        self.cdd_ = npy.dot(self.d_k_ - npy.dot(d_ave, ones),
                            npy.transpose(self.d_k_ - npy.dot(d_ave, ones))) / (self.nr_ - 1)
        cd_inv = npy.linalg.inv(self.cdd_ + self.alpha_[self.i_na_] * self.cd_)
        for i in range(0, self.nr_):
            self.m_k_[:, i] = npy.copy(self.m_k_[:, i]) + npy.dot(npy.dot(self.cmd_, cd_inv), self.d_uc_[:, i] - self.d_k_[:, i])
        npy.savetxt('ma_' + str(self.i_na_), self.m_k_)
        self.i_na_ += 1

    def save_result(self):
        self.d_posterior_ = npy.copy(self.d_k_)
        self.m_posterior_ = npy.copy(self.m_k_)

    def solve(self):
        self.initialize()
        while self.i_na_ < self.na_:
            self.forecast()
            self.update()
        self.save_result()
        self.sim_master_.stop()