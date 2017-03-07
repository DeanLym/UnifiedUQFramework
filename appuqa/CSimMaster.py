try:
    from .UQGlobal import *
except():
    from UQGlobal import *
import numpy as np
from enum import IntEnum
if UQ_USE_MPI:
    from mpi4py import MPI


class SIGNAL(IntEnum):
    SIM = 0
    WAIT = 1
    STOP = 2


class SimMaster:
    def __init__(self, nm=1, nd=1):
        # self.num_run_ = 1
        self.nm_ = nm
        self.nd_ = nd
        self.comm = None
        self.num_procs = 1
        self.rank = 0
        if UQ_USE_MPI:
            self.comm = MPI.COMM_WORLD
            self.num_procs = self.comm.Get_size()
            self.rank = self.comm.Get_rank()

    def run_list_sim(self, m_list):
        num_run = m_list.shape[1]
        d_list = np.zeros((self.nd_, num_run))
        if UQ_USE_MPI:
            if self.rank == 0:
                d_list = self.master_run(m_list)
        else:
            for i_run in range(0, num_run):
                d_list[:, i_run] = self.sim(m_list[:, i_run], i_run)
        return d_list

    # def run(self):
    #     if self.rank != 0:
    #         self.slave_run()

    def sim(self, m, tag):
        # The black-box simulator d=g(m)
        # Overwrite this function for your problem
        print("SimBase sim is called.")
        d = np.zeros((self.nd_, 1))
        return d

    def master_run(self, m_list):
        num_run = m_list.shape[1]
        print("Number of run: " + str(num_run))
        i_run = 0
        i_data = 0
        d_list = np.zeros((self.nd_, num_run))
        while i_run < num_run:
            print("-------------------------------Master sending Run signal...")
            for k in range(1, self.num_procs):
                if i_run < num_run:
                    msg = {
                        'signal': SIGNAL.SIM,
                        'data': m_list[:, i_run],
                        'tag': i_run,
                    }
                else:
                    msg = {
                        'signal': SIGNAL.WAIT
                    }
                self.comm.send(msg, dest=k)
                i_run += 1

            print("-------------------------------Master receiving data...")
            for k in range(1, self.num_procs):
                d = self.comm.recv(source=k)
                if i_data < num_run:
                    d_list[:, i_data] = d
                else:
                    pass
                i_data += 1
                print("d from slave #"+str(k))
                # print(d)

        print("-------------------------------Master run..")
        return d_list

    def slave_run(self):
        # while True:
            # self.comm.receive()
        cpt = 0
        while True:
            cpt += 1
            print("Slave #" + str(self.rank) + "loop #" + str(cpt))
            msg = self.comm.recv(source=0)
            print("Slave #" + str(self.rank) + " received signal " + msg.get("signal") + "...")
            if msg.get("signal") == SIGNAL.SIM:
                m = msg.get("data")
                tag = msg.get("tag")
                d = self.sim(m, tag)
                self.comm.send(d, dest=0)
            if msg.get("signal") == SIGNAL.WAIT:
                self.comm.send('', dest=0)
            if msg.get("signal") == SIGNAL.STOP:
                break
        print("Slave #" + str(self.rank) + " breaked from while loop...")

    def stop(self):
        if UQ_USE_MPI:
            print("-------------------------------Master sending Stop signal...")
            # Stop the slaves
            for k in range(1, self.num_procs):
                msg = {
                    'signal': SIGNAL.STOP,
                }
                self.comm.send(msg, dest=k)


