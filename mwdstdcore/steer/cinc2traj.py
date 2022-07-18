from typing import List, Optional, Tuple
import numpy as np
from numpy import pi
from mwdstdcore.datamodel import BHA, SlideInterval, TfStation, CIStation
from mwdstdcore.core.common.mincurv import mincurv_int


CI_MIN = 2. * pi / 180  # minimum inclination for continuous measurement
CI_TRN = 3. * pi / 180  # transition zone for continuous inclination
INC_ERR_THR = 0.25 * pi / 180
DELTA_MD_MIN = 1.5  # m
DELTA_MD_VAL = 3.  # m
GT_ERR = 1e-3  # relative to G
DMD_QC = 10.  # m, minimum distance between surveys
INT_STEP = 3.  # m


# calculate HD surveys from stationary and continuous inclination surveys
def cinc2traj(cinc: List[CIStation], stations: List[TfStation], bha: Optional[BHA] = None,
              steering: Optional[List[SlideInterval]] = None) -> Tuple[List[TfStation], bool, bool]:
    # find DLS capacity
    # dls = dlsest(stations, bha, steering)
    dls = 7. * np.pi / 180 / 30

    # smooth stations
    # stn_smooth = preflt(stations, dls)
    stn_smooth = stations
    stn_num = len(stations)

    # interpolate azimuth and tf for continuous inclination surveys
    traj_smooth = np.asarray([[s.md, s.inc, s.az, s.tf] for s in stn_smooth])
    # md_ci = np.asarray([ci.md for ci in cinc])
    # inc_ci = np.asarray([ci.inc for ci in cinc])
    [md_ci, inc_ci] = md2flt(cinc)
    [table_int, _] = mincurv_int(md_ci, traj_smooth)

    # fuse stationary and continuous surveys at low inclinations
    table_ci = table_int.copy()
    inc_int = table_int[:, 1]
    ci_weights = ((inc_int >= CI_MIN) * (inc_int < CI_MIN + CI_TRN) * (inc_int - CI_MIN) / CI_TRN +
                  (inc_int > CI_MIN + CI_TRN))
    table_ci[:, 1] = (1 - ci_weights) * inc_int + ci_weights * inc_ci

    # search for minimum MD distance from cinc survey to 6-axis survey
    ind = np.searchsorted(traj_smooth[:, 0], md_ci)
    dmd1 = np.abs(traj_smooth[(ind - 1 >= 0) * (ind - 1), 0] - md_ci)
    dmd2 = np.abs(traj_smooth[(ind < stn_num) * ind + (ind >= stn_num) * (stn_num - 1), 0] - md_ci)
    dmd_min = (dmd1 <= dmd2) * dmd1 + (dmd2 < dmd1) * dmd2
    dmd_min = (dmd_min < DELTA_MD_MIN) * DELTA_MD_MIN + (dmd_min >= DELTA_MD_MIN) * dmd_min

    # calculate an error from G_total
    inc_min = 1. * pi / 180  # minimum inclination for error propagation
    inc4jcbn = (table_ci[:, 1] < inc_min) * inc_min + (table_ci[:, 1] >= inc_min) * table_ci[:, 1]

    # filter cont inc surveys with regard to 6-axis surveys
    dinc_thr = np.sqrt((dmd_min * dls) ** 2 + INC_ERR_THR ** 2 + (GT_ERR / np.sin(inc4jcbn)) ** 2)
    dinc = np.abs(table_ci[:, 1] - table_int[:, 1])
    table_ci = table_ci[(dinc <= dinc_thr), :]

    # verification continuous inclination data vs stations
    ci_vrf_qc = qc4match(traj_smooth[:, 0], table_ci[:, 0])

    # add additional interpolated points at 6-axis survey MDs
    [table2add, _] = mincurv_int(traj_smooth[:, 0], table_ci)
    for i in range(0, table2add.shape[0]):
        ind = np.argwhere(table_ci[:, 0] == table2add[i, 0])
        if ind.shape[0] == 0:
            row2add = np.resize(table2add[i, :], (1, table2add.shape[1]))
            table_ci = np.r_[table_ci, row2add]

    # sort by MD
    sort_ind = np.argsort(table_ci[:, 0])
    table_ci = table_ci[sort_ind, :]
    stn2ci_ind = np.zeros(traj_smooth.shape[0]).astype(int)
    for i in range(0, traj_smooth.shape[0]):
        ind = np.argwhere(table_ci[:, 0] == traj_smooth[i, 0]).flatten()
        stn2ci_ind[i] = int(ind)

    # smooth
    stn_ci = [TfStation(md=table_ci[i, 0], inc=table_ci[i, 1], az=table_ci[i, 2], tf=table_ci[i, 3])
              for i in range(0, table_ci.shape[0])]

    # calculate build-rate table
    dmd = np.array([(stn_ci[i + 1].md - stn_ci[i].md) for i in range(0, len(stn_ci) - 1)])
    br = np.array([(stn_ci[i + 1].inc - stn_ci[i].inc) / dmd[i] for i in range(0, len(stn_ci) - 1)])
    md_hd = np.array([traj_smooth[0, 0]])
    inc_hd = np.array([traj_smooth[0, 1]])
    for i in range(0, traj_smooth.shape[0] - 1):
        md1 = traj_smooth[i, 0]
        inc1 = traj_smooth[i, 1]
        inc2 = traj_smooth[i + 1, 1]
        sort_ind1 = stn2ci_ind[i]
        sort_ind2 = stn2ci_ind[i + 1]
        dinc_ci = np.sum(br[sort_ind1:sort_ind2] * dmd[sort_ind1:sort_ind2])
        dinc_srv = inc2 - inc1
        br_offset = (dinc_srv - dinc_ci) / np.sum(dmd[sort_ind1:sort_ind2])
        dinc_acc = np.cumsum((br[sort_ind1:sort_ind2] + br_offset) * dmd[sort_ind1:sort_ind2])
        inc_hd = np.r_[inc_hd, dinc_acc + inc1]

        dmd_acc = np.cumsum(dmd[sort_ind1:sort_ind2])
        md_hd = np.r_[md_hd, dmd_acc + md1]

    # interpolate azimuth and toolface for HD surveys
    [traj_hd, _] = mincurv_int(md_hd, traj_smooth)
    traj_hd[:, 1] = inc_hd

    stn_hd = [TfStation(md=traj_hd[i, 0], inc=traj_hd[i, 1], az=traj_hd[i, 2], tf=traj_hd[i, 3])
              for i in range(0, traj_hd.shape[0])]
    srv_freq_qc = qc4frq(md_hd)
    return stn_hd, srv_freq_qc, ci_vrf_qc


# quality check for survey frequency
def qc4frq(md_hd: np.ndarray):
    dmd_max = md_hd[-1] - md_hd[0]
    dmd = md_hd[1:] - md_hd[:-1]
    dmd_qc = np.sum((dmd <= DMD_QC) * dmd)
    dmd_qc = dmd_qc / dmd_max if dmd_max != 0. else 1.
    return dmd_qc >= 0.8


# quality cross-check between static and continuous surveys
def qc4match(md_stn: np.ndarray, md_ci: np.ndarray):
    if md_ci.shape[0] > 0:
        ind = np.searchsorted(md_ci, md_stn)
        ind1 = (ind - 1 >= 0) * (ind - 1)
        ind2 = (ind < md_ci.shape[0]) * ind + (ind >= md_ci.shape[0]) * (md_ci.shape[0] - 1)
        qc1 = np.abs(md_stn - md_ci[ind1]) <= DELTA_MD_VAL
        qc2 = np.abs(md_stn - md_ci[ind2]) <= DELTA_MD_VAL
        qc = np.sum(np.logical_or(qc1, qc2)) / md_stn.shape[0]
    else:
        qc = 0.
    return qc >= 0.5


# average repeating depth continuous surveys
def md2flt(cinc: List[CIStation]):
    md_ci_flt: List[float] = []
    inc_ci_flt: List[float] = []
    for ci in cinc:
        md_ci_flt += [] if ci.md in md_ci_flt else [ci.md]
    md_ci_flt: np.ndarray = np.asarray(md_ci_flt)
    md_ci = np.asarray([ci.md for ci in cinc])
    inc_ci = np.asarray([ci.inc for ci in cinc])
    for md in md_ci_flt:
        ind = np.argwhere(md_ci == md).flatten()
        inc_ci_flt += [np.mean(inc_ci[ind])]
    inc_ci_flt: np.ndarray = np.asarray(inc_ci_flt)
    return md_ci_flt, inc_ci_flt
