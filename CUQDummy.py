

class UQDummy:
    def __init__(self, nm=1, nd=1, nr=1):
        self.sim_master_ = None
        self.mpi_run = False

    def solve(self):
        self.sim_master_.run()
        # print("UQBase solve is called.")