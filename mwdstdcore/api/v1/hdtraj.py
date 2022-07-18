from typing import List, Optional
from mwdstdcore.datamodel import Correction
from .models import Run3
from ..logs import DebugTimer
from mwdstdcore.steer.cinc2traj import cinc2traj
from mwdstdcore.steer.opt4hd import opt4hd


def hdtraj(runs: List[Run3], corrections: List[Optional[Correction]], optimize_hd: bool = True):
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

            # calculate interpolated trajectory
            if run.ci is not None and len(run.ci) > 2:
                with DebugTimer(f"CIHD{ri}: {{:0.2f}}"):
                    traj_hd, srv_freq_qc, ci_vrf_qc = cinc2traj(run.ci, traj, run.bha, run.slidesheet)
                    corr.qa.srv_freq.value = srv_freq_qc
                    corr.qa.ci_vrf.value = ci_vrf_qc
                    md_cont_inc = [ci.md for ci in run.ci]
                    md_stations = [stn.md for stn in traj]
                    corr.stations_hd = opt4hd(md_stations, md_cont_inc, traj_hd) if optimize_hd else traj_hd
            elif run.slidesheet is not None and len(run.slidesheet) > 0:
                pass
                # with DebugTimer(f"SSHD{ri}: {{:0.2f}}"):
                #     traj_hd, _, _, _ = int_cor(run.slidesheet, traj, run.bha)
                #     corr.stations_hd = traj_hd

