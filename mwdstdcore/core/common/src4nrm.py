from typing import Tuple
import numpy as np
from .mincurv import mincurv_int


# find the nearest point of the object well from the latest point of the subject well
def src4nrm(traj_sbj: np.ndarray, traj_obj: np.ndarray, tie_in_sbj: Tuple[float, float, float] = (0., 0., 0.),
            tie_in_obj: Tuple[float, float, float] = (0., 0., 0.)):
    [_, nev_sbj] = mincurv_int(traj_sbj[-1, 0:1], traj_sbj, tie_in_sbj)
    nev_sbj = np.resize(nev_sbj, (1, 3))
    md_step = 1.
    mdi_obj = np.arange(traj_obj[0, 0], traj_obj[-1, 0], md_step)
    ind4td = np.argwhere(mdi_obj == traj_obj[-1, 0])
    if ind4td.shape[0] == 0:
        mdi_obj = np.block([mdi_obj, traj_obj[-1, 0:1]])

    [_, nev_obj_int] = mincurv_int(mdi_obj, traj_obj, tie_in_obj)

    dnev = nev_obj_int - nev_sbj
    dr2 = np.sum(dnev ** 2, 1)
    ind_dr2_min = np.argmin(dr2)
    md_obj_min = mdi_obj[ind_dr2_min]

    return md_obj_min
