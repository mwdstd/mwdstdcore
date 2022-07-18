from typing import Tuple
import numpy as np
from numpy import sin, cos, tan, arccos, arctan2, arcsin, sqrt, pi, ndarray


def mincurv(surveys: ndarray, tie_in: Tuple[float, float, float] = (0., 0., 0.)) -> ndarray:
    nev = np.zeros((surveys.shape[0], 3))
    nev[0, :] = tie_in
    sinI = sin(surveys[:, 1])
    cosI = cos(surveys[:, 1])
    sinA = sin(surveys[:, 2])
    cosA = cos(surveys[:, 2])
    dMD = surveys[1:, 0] - surveys[:-1, 0]
    cosdI = cos(surveys[1:, 1] - surveys[:-1, 1])
    cosdA = cos(surveys[1:, 2] - surveys[:-1, 2])

    DL2 = arccos(cosdI - sinI[:-1] * sinI[1:] * (1-cosdA)) * .5
    DL2[DL2 < 1e-10] = 1e-10
    RF = tan(DL2) / DL2
    # RF[DL2 < 1e-10] = 1
    dMD2RF = dMD * RF * .5
    nev[1:, 0] = dMD2RF * (sinI[:-1] * cosA[:-1] + sinI[1:] * cosA[1:])
    nev[1:, 1] = dMD2RF * (sinI[:-1] * sinA[:-1] + sinI[1:] * sinA[1:])
    nev[1:, 2] = dMD2RF * (cosI[:-1] + cosI[1:])

    nev = np.cumsum(nev, axis=0)
    return nev


def mincurv_int(mdi: ndarray, traj: ndarray, tie_in: Tuple[float, float, float] = (0., 0., 0.)):
    # sorting for depth
    ind_sort = np.argsort(traj[:, 0])
    traj_sorted = traj[ind_sort, :]
    md = traj_sorted[:, 0]
    # search for indexes for mdi
    ind = np.searchsorted(md, mdi)

    s1 = traj_sorted[(ind - 1 >= 0) * (ind - 1), :]
    s2 = traj_sorted[(ind < md.shape[0]) * ind + (ind >= md.shape[0]) * (md.shape[0] - 1), :]

    reg_coef = 1e-10
    dmd = s2[:, 0] - s1[:, 0]
    dmd_reg = (dmd == 0.) * reg_coef + (dmd != 0.) * dmd
    dmdi = mdi - s1[:, 0]
    dmdi_reg = (dmd == 0.) * reg_coef + (dmd != 0.) * dmdi

    inc1 = s1[:, 1]
    inc2 = s2[:, 1]
    az1 = s1[:, 2]
    az2 = s2[:, 2]
    v1 = np.c_[sin(inc1) * cos(az1), sin(inc1) * sin(az1), cos(inc1)]
    v2 = np.c_[sin(inc2) * cos(az2), sin(inc2) * sin(az2), cos(inc2)]

    k = np.resize(dmdi_reg / dmd_reg, (mdi.shape[0], 1))
    dl_angle = 2 * arcsin(sqrt(sin((inc2 - inc1) / 2) ** 2 + sin(inc1) * sin(inc2) * sin((az2 - az1) / 2) ** 2))
    dl_angle = (dl_angle != 0.) * dl_angle + (dl_angle == 0.) * reg_coef
    dl_angle = np.resize(dl_angle, (mdi.shape[0], 1))
    vi = (sin((1 - k) * dl_angle) * v1 + sin(k * dl_angle) * v2) / sin(dl_angle)

    vi /= np.resize(np.linalg.norm(vi, axis=1), (vi.shape[0], 1))

    inci = arccos(vi[:, 2])
    azi = arctan2(vi[:, 1], vi[:, 0]) % (2 * pi)
    tfi = s1[:, 3] if traj.shape[1] == 4 else np.zeros_like(mdi)

    stn_int = np.c_[mdi, inci, azi, tfi]

    # NEV calculation
    traj_merged = np.r_[traj[:, :3], stn_int[:, :3]]
    sort_ind = np.argsort(traj_merged[:, 0])
    traj_merged = traj_merged[sort_ind, :]
    nev_merged = mincurv(traj_merged, tie_in)
    restored_ind = np.argsort(sort_ind)
    nev_int = nev_merged[restored_ind[traj.shape[0]:], :]

    return [stn_int, nev_int]
