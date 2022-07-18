from typing import List, Tuple
from math import radians as deg2rad, sin, cos, atan2, pi
import numpy as np
from mwdstdcore.core.common.mincurv import mincurv, mincurv_int
from mwdstdcore.core.common.src4nrm import src4nrm
from mwdstdcore.datamodel import Station, StationPosition


# assumed stations sorted by md & actual and plan non-empty
def act2plan(actual: List[Station], plan: List[Station], inc_thr: float = deg2rad(2.5), az_thr: float = deg2rad(5.)
             ) -> Tuple[bool, bool, StationPosition, StationPosition]:
    traj_plan = np.asarray([[s.md, s.inc, s.az, 0.] for s in plan])
    traj_act = np.asarray([[s.md, s.inc, s.az, 0.] for s in actual])
    md_plan = src4nrm(traj_act, traj_plan)
    [stn_ref, nev_ref] = mincurv_int(np.array([md_plan]), traj_plan)
    inc_ref = stn_ref[0, 1]
    az_ref = stn_ref[0, 2]
    inc_act = actual[-1].inc
    az_act = actual[-1].az

    dinc = inc_act - inc_ref

    cos_x = cos(az_act) * cos(az_ref) + sin(az_act) * sin(az_ref)
    sin_x = cos(az_ref) * sin(az_act) - sin(az_ref) * cos(az_act)
    daz = atan2(sin_x, cos_x)
    az_thr_norm = az_thr / sin(inc_act) if inc_act > deg2rad(0.1) else 2 * pi

    qc_inc = (abs(dinc) <= inc_thr)
    qc_az = (abs(daz) <= az_thr_norm)

    nev_act = mincurv(traj_act)
    nev_act = nev_act[-1, :]

    nev_delta = nev_act - nev_ref[0]

    last = actual[-1]
    deepest = StationPosition(md=last.md, inc=last.inc, az=last.az, ns=nev_act[0], ew=nev_act[1], tvd=nev_act[2])
    plan_dev = StationPosition(md=0., inc=dinc, az=daz, ns=nev_delta[0], ew=nev_delta[1], tvd=nev_delta[2])

    return qc_inc, qc_az, plan_dev, deepest
