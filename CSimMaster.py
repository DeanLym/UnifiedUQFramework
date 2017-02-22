import numpy as np
from mpi4py import MPI
from enum import IntEnum


class SimMaster:
    def __init__(self, nm=1, nd=1, mpi_run=False):
        # self.num_run_ = 1
        self.nm_ = nm
        self.nd_ = nd
        self.mpi_run = mpi_run
        self.comm = None
        self.num_procs = 1
        self.rank = 0
        if self.mpi_run:
            self.comm = MPI.COMM_WORLD
            self.num_procs = self.comm.Get_size()
            self.rank = self.comm.Get_rank()

    def run_list_sim(self, m_list):
        if self.mpi_run:
            if self.rank == 0:
                self.master_run(m_list)
        return True

    def run(self):
        if self.rank != 0:
            self.slave_run()

    def sim(self, m):
        # The black-box simulator d=g(m)
        # Overwrite this function for your problem
        print("SimBase sim is called.")
        d = np.zeros((self.nd_, 1))
        return d

    def master_run(self,m_list):
        print("-------------------------------Master sending X signal...")
        for k in range(1, self.num_procs):
            data = "X"
            self.comm.send(data, dest=k)
        print("-------------------------------Master receiving Ready signal...")
        for k in range(1, self.num_procs):
            data = self.comm.recv(source=k)
            print("Master" + str(self.rank) + " received signal " + data + " from slave #" +str(k))
        print("-------------------------------Master sending Run signal...")
        for k in range(1, self.num_procs):
            data = "R"
            self.comm.send(data, dest=k)
        print("-------------------------------Master receiving data...")
        for k in range(1, self.num_procs):
            d = self.comm.recv(source=k)
            print("d from slave #"+str(k))
            print(d)
        print("-------------------------------Master sending Stop signal...")
        for k in range(1, self.num_procs):
            data = "S"
            self.comm.send(data, dest=k)
        print("-------------------------------Master run..")

    def slave_run(self):
        # while True:
            # self.comm.receive()
        cpt = 0
        while True:
            cpt += 1
            print("Slave #" + str(self.rank) + "loop #" + str(cpt))
            signal = self.comm.recv(source=0)
            print("Slave #" + str(self.rank) + " received signal " + signal + "...")
            if signal == "X":
                self.comm.send("R",dest=0)
            if signal == "R":
                d = np.random.rand(self.nd_)
                self.comm.send(d,dest=0)
            if signal == "S":
                break
        print("Slave #" + str(self.rank) + " breaked from while loop...")
        # for k in range(0,1):
        #     print("Slave #" + str(self.rank) + " running...")
        #     self.sim(1)

    # def run(self, rank):
    #     for k in range(0,2):
    #         print("Slave #" + str(rank) + " running...")
    #         self.sim(1)



