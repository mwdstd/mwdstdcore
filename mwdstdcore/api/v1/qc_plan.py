from typing import List
from mwdstdcore.datamodel import Correction, Station
from mwdstdcore.auto.act_vs_plan import act2plan


def qc_plan(corrections: List[Correction], plan: List[Station] = None):
    traj = None
    if plan is not None and len(plan) > 0:
        for corr in corrections:
            if corr is not None:
                has_hd_stations = corr.stations_hd is not None and len(corr.stations_hd)> 0
                stations = corr.stations_hd if has_hd_stations else corr.get_std_stations()
                stations: List[Station] = sorted(stations, key=lambda s: s.md)
                if len(stations) == 0:
                    continue
                if traj is None:
                    start = stations[0]
                    traj = [st for st in plan if st.md < start.md]
                traj += stations
                qc_inc, qc_az, corr.plan_dev, corr.deepest = act2plan(traj, plan)
                corr.qa.plan.value = qc_inc and qc_az
