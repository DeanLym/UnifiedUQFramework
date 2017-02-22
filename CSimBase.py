import numpy as np


class SimBase:
    def __init__(self, nm=1, nd=1):
        # self.num_run_ = 1
        self.nm_ = nm
        self.nd_ = nd

    def sim(self, m):
        d = np.zeros((self.nd_,1))
        return d
