from typing import List, Optional
import jsons
import hashlib
import numpy as np
from math import radians, cos, sin, atan2

from mwdstdcore.datamodel import Station, BHA, Correction
from mwdstdcore.datamodel.calc.station import calc_gtf
from mwdstdcore.sag.sagcor import sagcor
from .models import Run2
from ..logs import DebugTimer

SAG_TOLERANCE = radians(2 * 0.225)


def sag_basic(runs: List[Run2], corrections: List[Optional[Correction]], use_hd: bool = False):
    for ri, run in enumerate(runs):
        corr = corrections[ri]
        if corr is None:
            continue

        # Get indices of STD surveys with good inc/az unc
        idx = corr.get_std_inc_idx()
        idx = sorted(idx, key=lambda i: corr.stations[i].md)

        if len(idx) > 1:
            
            # calculate trajectory for filtered surveys and reference
            traj = [corr.stations[i] for i in idx]

            sag_tag = hashlib.md5(jsons.dumps(traj).encode('utf-8')).hexdigest()
            if run.correction is not None and run.correction.sag_tag == sag_tag:
                corr.sag = run.correction.sag
                corr.qa.sag_conv.value = run.correction.qa.sag_conv.value
                corr.qa.sag_exp.value = run.correction.qa.sag_exp.value
            else:
                # calculate sag on filtered surveys depths
                with DebugTimer(f"Sag{ri}: {{:0.2f}}"):
                    sag_results = [run_sagcor(st, sgtf, run.bha, run.mud_weight, traj) for st, sgtf in
                            [(st, calc_gtf(s)) for s, st in [(corr.surveys[i], corr.stations[i]) for i in idx]]]
                corr.sag = [sag for sag, valid in sag_results]
                corr.qa.sag_conv.value = all(valid for sag, valid in sag_results)
                corr.qa.sag_exp.value = all(abs(sag) < SAG_TOLERANCE for sag, valid in sag_results)
                # interpolate sag for bad surveys
                if len(corr.sag) > 0:
                    corr.sag = np.interp([s.md for s in corr.surveys], [corr.surveys[i].md for i in idx], corr.sag).tolist()
            corr.sag_tag = sag_tag

            # apply sag correction to source trajectory
            for st, sag in zip(corr.stations, corr.sag):
                st.inc -= sag
                st.dinc -= sag


# linear station extrapolation
def extrapolate_station(md: float, st1: Station, st2: Station) -> Station:
    dinc = st1.inc - st2.inc
    cos_x = cos(st1.az) * cos(st2.az) + sin(st1.az) * sin(st2.az)
    sin_x = cos(st2.az) * sin(st1.az) - sin(st2.az) * cos(st1.az)
    daz = atan2(sin_x, cos_x)
    rate = (md - st1.md) / (st1.md - st2.md)
    return Station(
        md=md, 
        inc=st1.inc + dinc * rate, 
        az=st1.az + daz * rate
    )


def run_sagcor(station: Station, survey_gtf: float, bha: BHA, mud_weight:float, base_traj: List[Station]):
    if station.inc < radians(5.):
        return 0., True
    bit_depth = station.md + bha.dni_to_bit
    # traj = [st for st in base_traj if st.md <= bit_depth]
    traj = [st for st in base_traj]
    if len(traj) == 0:
        return 0., True
    # extrapolate trajectory to bit
    if traj[-1].md < bit_depth and len(traj) > 1:
        traj.append(extrapolate_station(bit_depth, traj[-1], traj[-2]))
    res = sagcor(bha, bit_depth, traj, survey_gtf + bha.tf_correction, mud_weight)
    return res.sag, res.valid
