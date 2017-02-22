from CUQBase import UQBase
import numpy as np
from scipy import sparse
from mpi4py import MPI


class UQEn(UQBase):
    def __init__(self, nm=1, nd=1, nr=1):
        super(UQEn, self).__init__(nm, nd, nr)
        # Nm, Nd defined is UQBase
        # Nr - ensemble size
        self.np_ = 0 # Size of the state vector (0 for smoothers and non-zero for filters)
        # Cd definded in UQBase
        self.cyd_ = np.zeros((self.nm_, self.nd_))
        self.cdd_ = np.zeros((self.nd_, self.nd_))
        self.duc_ = np.zeros((self.nd_, self.nr_))
        self.dn_ = np.zeros((self.nd_, self.nr_))

    def forecast(self):
        # forecast step
        return True

    def update(self):
        # update step
        return True

    def mpirun(self):
        # parallel run
        print("UQEn mpirun is called.")
        self.sim_fun()
        return True

    def run(self):
        # serial run
        print("UQEn run is called.")
        self.sim_fun()
        return True

    def solve(self):
        print("UQEn solve is called.")
        if self.mpi_run:
            self.mpirun()
        else:
            self.run()

        # serial run
        return True

    def sim(self):
        # The function to overwrite
        return True



