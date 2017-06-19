try:
    from .UQGlobal import *
    from .CUQEnS import UQEnS
    from .CUQDummy import UQDummy
    from .CUQESMDA import UQESMDA
    from .CUQEnKF import UQEnKF
except():
    from UQGlobal import *
    from CUQEnS import UQEnS
    from CUQDummy import UQDummy
    from CUQESMDA import UQESMDA
    from CUQEnKF import UQEnKF
import os
import sys
import numpy as npy
if os.getenv('UQ_USE_MPI') == "True":
    from mpi4py import MPI


class UQMain:
    def __init__(self, nm, nd, nr, alg, np=1, sim_master=None):
        self.nm_ = nm
        self.nd_ = nd
        self.nr_ = nr
        self.np_ = np
        self.alg_ = alg
        self.solver = None
        self.comm = None
        self.num_procs = 1
        self.rank = 0
        self.use_mpi = {
            None: False,
            "True": True,
            "False": False,
        }.get(os.getenv('UQ_USE_MPI'), False)
        if self.use_mpi:
            self.comm = MPI.COMM_WORLD
            self.num_procs = self.comm.Get_size()
            self.rank = self.comm.Get_rank()
        self.init_solver()
        self.sim_master = sim_master

    @property
    def sim_master(self):
        return self.solver.sim_master_

    @sim_master.setter
    def sim_master(self, value):
        self.solver.sim_master_ = value

    def init_solver(self):
        if self.rank == 0:
            # Master processor
            self.solver = {
                UQAlg.EnS: UQEnS(self.nm_, self.nd_, self.nr_),
                UQAlg.ES_MDA: UQESMDA(self.nm_, self.nd_, self.nr_),
                UQAlg.EnKF: UQEnKF(self.nm_, self.nd_, self.nr_, self.np_)
                # UQAlg.MCMC: None,
                # To be complete
            }.get(self.alg_, None)
            print('[MESSAGE] Master solver initialized.')
        else:
            # Dummy solver for the slave processors
            self.solver = UQDummy()
            print('[MESSAGE] Slave #' + str(self.rank) + ' solver initialized.')
        #self.solver.sim_master_ = self.sim_master_

    def solve(self):
        if self.solver is not None:
            self.solver.solve()
        else:
            sys.exit(1)

    def call(self, fun_name, data):
        if self.rank == 0:
            res = getattr(self.solver, fun_name)(data)
            return res
        else:
            return None

    def save_results(self):
        if self.rank == 0:
            npy.savetxt('m_post', self.solver.m_posterior_)
            npy.savetxt('d_post', self.solver.d_posterior_)

    def get_data(self, data_name: str):
        if self.rank == 0:
            data = getattr(self.solver, data_name)
        else:
            data = None
        return data

    def run_list_sim(self, m_list):
        if self.rank == 0:
            self.solver.sim_master_.run_list_sim(m_list)
        else:
            self.solver.sim_master_.slave_run()
        # stop slaves
        if self.rank == 0:
            self.solver.sim_master_.stop()


if __name__ == "__main__":
    main = UQMain()
    main.solve()
