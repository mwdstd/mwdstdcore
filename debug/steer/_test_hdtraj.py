import numpy as np
from numpy import pi
import matplotlib.pyplot as plt
from mwdstdcore.datamodel import TfStation, CIStation
from mwdstdcore.core.common.mincurv import mincurv_int
from mwdstdcore.steer.cinc2traj import cinc2traj
from mwdstdcore.steer.opt4hd import opt4hd


md = np.arange(0., 500., 25.)
stn_num = md.shape[0]
inc = np.linspace(0., 90., stn_num) * pi / 180
inc[1::2] = inc[:-1:2]
az = np.linspace(90., 90., stn_num) * pi / 180
tf = np.linspace(0., 360., stn_num) * pi / 180
traj_ = np.c_[md, inc, az, tf]
stn = [TfStation(md=traj_[i, 0], inc=traj_[i, 1], az=traj_[i, 2], tf=traj_[i, 3]) for i in range(0, stn_num)
       if i % 2 == 0]

md_cinc = np.arange(0., 500., 2.)
[table_cinc, _] = mincurv_int(md_cinc, traj_)
table_cinc[:, 1] += 1.0 * pi / 180 + np.random.randn(md_cinc.shape[0]) * 0.3 * pi / 180
cinc_ = [CIStation(md=table_cinc[i, 0], inc=table_cinc[i, 1]) for i in range(0, table_cinc.shape[0])]
[stn_hd_, qc_hd_, _] = cinc2traj(cinc_, stn)
traj_hd_ = np.array([[s.md, s.inc, s.az, s.tf] for s in stn_hd_])

md_stat = [s.md for s in stn]
stn_hd_opt = opt4hd(md_stat, list(md_cinc), stn_hd_)
traj_hd_opt = np.array([[s.md, s.inc, s.az, s.tf] for s in stn_hd_opt])

fig = plt.figure()
incplt = fig.add_subplot(111)

incplt.plot(table_cinc[:, 0], table_cinc[:, 1] * 180 / pi, 'r.')
incplt.plot(traj_hd_[:, 0], traj_hd_[:, 1] * 180 / pi, 'b')
incplt.plot(traj_[::2, 0], traj_[::2, 1] * 180 / pi, 'go')
incplt.plot(traj_hd_opt[:, 0], traj_hd_opt[:, 1] * 180 / pi, 'g.')

plt.show()
