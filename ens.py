import UQGlobal
# Global option for using MPI or not
UQGlobal.UQ_USE_MPI = False
#
from CSimMaster import SimMaster
from CUQMain import *
import shutil
import os
import numpy as npy


class MySim(SimMaster):
    # def __init__(self, nm=1.):
    #     super(MySim,self).__init__()

    def sim(self, m, tag):
        sub_dir = './run/real_' + str(tag)
        self.copy_model_file(sub_dir)
        self.write_perm(sub_dir, m)
        os.chdir(sub_dir)
        # Run the simulator
        os.system("..\\..\\simulator\\TwoFlow.exe model.dat")
        # Read data
        d = self.read_data()
        os.chdir('../../')
        shutil.rmtree(sub_dir)
        # print("My sim called...")
        return d

    def copy_model_file(self, sub_dir):
        if os.path.exists(sub_dir):
            shutil.rmtree(sub_dir)
        shutil.copytree('./model', sub_dir)
        return True

    def write_perm(self, sub_dir, m):
        perm_file = sub_dir + '/PERM.inc'
        npy.savetxt(perm_file, npy.exp(m), header='PERMI ALL', comments="")

    def read_data(self):
        data_file = 'model.well'
        d = npy.loadtxt(data_file, skiprows=4, usecols=(12,))
        return d[0:self.nd_]


class MySimEnkF(MySim):
    def __init__(self, nm=1, nd=1, np=1):
        super(MySimEnkF, self).__init__(nm, nd)
        self.np_ = np

    def sim(self, y, tag):
        sub_dir = './run/real_' + str(tag)
        self.copy_model_file(sub_dir)
        m = y[0:self.nm_]
        p = y[self.nm_:]
        self.write_perm(sub_dir, m)
        self.write_init(sub_dir, p)
        os.chdir(sub_dir)
        # Run the simulator
        os.system("..\\..\\simulator\\TwoFlow.exe model.dat")
        # Read data
        data = self.read_data()
        os.chdir('../../')
        shutil.rmtree(sub_dir)
        # print("My sim called...")
        return data

    def copy_model_file(self, sub_dir):
        if os.path.exists(sub_dir):
            shutil.rmtree(sub_dir)
        shutil.copytree('./model1', sub_dir)
        return True

    def write_init(self, subdir, p):
        init_file = subdir + '/initialization.inc'
        pres = p[0:self.nm_]
        sw = p[self.nm_:]
        with open(init_file, 'w') as fid:
            fid.write('PRES ALL\n')
            for data in pres:
                fid.write(str(data) + '\n')
            fid.write('\n\n')
            fid.write('SWI ALL\n')
            for data in sw:
                fid.write(str(data) + '\n')
            fid.write('\n\n')

    def read_data(self):
        data_file = 'model.well'
        d = npy.loadtxt(data_file, skiprows=4, usecols=(12,))
        d = npy.expand_dims(d, axis=0)
        pres_file = 'model.pres'
        pres = npy.loadtxt(pres_file, skiprows=43)
        sw_file = 'model.sw'
        sw = npy.loadtxt(sw_file, skiprows=43)
        data = npy.concatenate((d,pres, sw))
        return data


def read_m_prior(prior_dir, nm, nr):
    m_prior = npy.zeros((nm, nr))
    for i_run in range(0, nr):
        ind_str = '{0:03d}'.format(i_run + 1)
        perm_file = prior_dir + "./PERMI_" + ind_str + '.inc'
        data = npy.loadtxt(perm_file, skiprows=3)
        m_prior[:, i_run] = npy.log(data)
        # with open(perm_file, 'r') as fid:
        #     temp = fid.readline()
        #     temp = fid.readline()
        #     temp = fid.readline()
        #     for j in range(0, nm):
        #         m_prior[j, i_run] = float(fid.readline())
        #     fid.close()
    return m_prior


def read_d_obs(fn, nd):
    data = npy.loadtxt(fn, skiprows=7)
    d_obs = data[:, 1]
    return d_obs


def read_cm(fn, nm):
    cm = npy.zeros((nm, nm))
    data = npy.loadtxt(fn, skiprows=8)
    num_entry = data.shape[0]
    for i in range(0, num_entry):
        cm[data[i, 0] - 1, data[i, 1] - 1] = data[i, 2]
        cm[data[i, 1] - 1, data[i, 0] - 1] = data[i, 2]
    return cm


def main():
    # print("This is main.")
    nm = 31
    nd = 12
    nr = 100
    my_sim = MySim(nm, nd)
    m_prior = read_m_prior('./data/ens_01', nm, nr)
    d_obs = read_d_obs('./data/observed_data.txt', nd)
    cm = read_cm('./data/Cm.txt', nm)
    cd = npy.eye(nd)
    npy.savetxt('m_prior', m_prior)

    # ==================Ensemble smoother======================= #
    ens = UQMain(nm, nd, nr, UQAlg.EnS, sim_master=my_sim)
    ens.solver.input_m_prior(m_prior)
    ens.solver.input_d_uc('./data/duc1.txt')
    ens.solver.input_cm(cm)
    ens.solver.input_cd(cd)
    ens.solve()
    npy.savetxt('m_post_ens', ens.solver.m_posterior_)

    # =========================ES-MDA========================== #
    # es_mda = UQMain(nm, nd, nr, UQAlg.ES_MDA, my_sim)
    # es_mda.solver.input_m_prior(m_prior)
    # es_mda.solver.input_d_obs(d_obs)
    # es_mda.solver.input_cm(cm)
    # es_mda.solver.input_cd(cd)
    # es_mda.solver.set_na(10)
    # alpha = npy.array([57.017, 35.0, 25.0, 20.0, 18.0, 15.0, 12.0, 8.0, 5.0, 3.0])
    # es_mda.solver.set_alpha(alpha)
    # es_mda.solve()
    # npy.savetxt('m_post_esmda', es_mda.solver.m_posterior_)

    # =========================EnKF=========================== #
    # nd = 1
    # np = 2 * nm
    # my_sim_enkf = MySimEnkF(nm, nd+np)
    # enkf = UQMain(nm, nd, nr, UQAlg.EnKF, np=np, sim_master=my_sim_enkf)
    # num_step = 12
    # d_uc_all = npy.loadtxt('./data/duc1.txt')
    # p_prior = npy.zeros((np, nr))
    # p_prior[0:nm, :] = 3500
    # p_prior[nm:, :] = 0.2
    # enkf.solver.input_cm(cm)
    # enkf.solver.input_cd(npy.eye(nd))
    # for i in range(0, num_step):
    #     enkf.solver.input_m_prior(m_prior)
    #     enkf.solver.input_p_prior(p_prior)
    #     enkf.solver.input_d_uc(d_uc_all[[i], :])
    #     enkf.solve()
    #     m_prior = npy.copy(enkf.solver.m_posterior_)
    #     p_prior = npy.copy(enkf.solver.p_posterior_)
    # npy.savetxt('m_post_enkf', enkf.solver.m_posterior_)
    # a = input()

main()
