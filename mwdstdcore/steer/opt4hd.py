from typing import List
import numpy as np
from mwdstdcore.core.common.mincurv import mincurv_int, mincurv
from mwdstdcore.datamodel import TfStation


LOCAL_TVD_THR = 0.05  # m
GLOBAL_TVD_THR = 0.30  # m


# thin HD surveys to minimize survey count with keeping NEV accuracy
def opt4hd(md_stations: List[float], md_cont_inc: List[float], stations_hd: List[TfStation]) -> List[TfStation]:
    md_ci = np.array(md_cont_inc)
    md_stat = np.array(md_stations)
    traj_hd = np.asarray([[s.md, s.inc, s.az, s.tf] for s in stations_hd])

    stat_srv_cnt = md_stat.shape[0]
    if stat_srv_cnt < 2:
        return stations_hd

    nev = mincurv(traj_hd)
    tvd0 = nev[-1, 2] - nev[0, 2]

    md_hd: List[float] = list(md_stat)
    while True:
        i_opt = []
        previous_hd_cnt = len(md_hd)
        for ind_stat in range(0, stat_srv_cnt - 1):
            md1 = md_hd[ind_stat]
            md2 = md_hd[ind_stat + 1]

            ind_ci = np.argwhere((md_ci > md1) * (md_ci < md2)).flatten()

            [stn_stat, nev] = mincurv_int(np.array([md1, md2]), traj_hd)
            tvd_full = nev[-1, 2] - nev[0, 2]

            nev = mincurv(stn_stat)
            tvd_hd = nev[-1, 2] - nev[0, 2]
            tvd_error = abs(tvd_full - tvd_hd)
            if tvd_error <= LOCAL_TVD_THR or len(ind_ci) == 0:
                continue
            else:
                i_opt += [None]
                md_avg = (md2 + md1) / 2
                i_avg = ind_ci[0]
                dmd = abs(md_avg - md_ci[i_avg])
                for i in ind_ci:
                    [stn_stat, _] = mincurv_int(np.array([md1, md_ci[i], md2]), traj_hd)
                    nev = mincurv(stn_stat)
                    tvd_ci = nev[-1, 2] - nev[0, 2]
                    tvd_error_cur = abs(tvd_full - tvd_ci)
                    if tvd_error > tvd_error_cur:
                        tvd_error = tvd_error_cur
                        i_opt[-1] = i
                    # looking for middle nearest CI in case of no i_opt found
                    if abs(md_avg - md_ci[i]) < dmd:
                        dmd = abs(md_avg - md_ci[i_avg])
                        i_avg = i

                if i_opt[-1] is None:
                    i_opt[-1] = i_avg

        for i in i_opt:
            if i is not None:
                md_hd += [md_ci[i]]
        md_tmp = np.sort(np.array(md_hd))
        md_hd = list(md_tmp)
        current_hd_cnt = len(md_hd)
        [stn_stat, _] = mincurv_int(md_tmp, traj_hd)
        nev = mincurv(stn_stat)
        tvd1 = nev[-1, 2] - nev[0, 2]
        tvd_error_full = abs(tvd1 - tvd0)
        if tvd_error_full <= GLOBAL_TVD_THR or current_hd_cnt == traj_hd.shape[0] or current_hd_cnt == previous_hd_cnt:
            break

    stn_opt = [TfStation(md=stn_stat[i, 0], inc=stn_stat[i, 1], az=stn_stat[i, 2], tf=stn_stat[i, 3])
               for i in range(0, stn_stat.shape[0])]
    return stn_opt
