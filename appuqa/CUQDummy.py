
class UQDummy:
    def __init__(self, nm=1, nd=1, nr=1):
        self.sim_master_ = None
        self.mpi_run = False

    def input_m_prior(self, fn):
        pass

    def input_d_obs(self, d_obs_file):
        pass

    def input_d_uc(self, d_uc_file):
        pass

    def input_cd(self, cd_file):
        pass

    def input_cm(self, cm):
        pass

    def solve(self):
        self.sim_master_.slave_run()
