from typing import Dict, List, Optional, Tuple
from collections import OrderedDict
from math import degrees, radians

from mwdstdcore.datamodel import Station, BHA, Correction
from mwdstdcore.datamodel.calc.station import calc_gtf
from mwdstdcore.sag.sagcor import sagcor
from .models import Run2
from ..logs import DebugTimer

SAG_TOLERANCE = radians(2 * 0.225)


def sag_basic(runs: List[Run2], corrections: List[Optional[Correction]]):
    for ri, run in enumerate(runs):
        corr = corrections[ri]
        if corr is None:
            continue

        # Skip if already done
        if run.correction == corr:
            continue

        if len(corr.stations) > 0:

            # calculate DLS
            dlss = calc_dls(corr.stations)
            # calculate sag
            with DebugTimer(f"Sag{ri}: {{:0.2f}}"):
                sag_results = [
                    run_sagcor(st.inc, dls[0], dls[1], run.bha, run.mud_weight) for st, dls in zip(corr.stations, dlss)
                ]
            corr.sag = [sag for sag, valid in sag_results]
            corr.qa.sag_conv.value = all(valid for sag, valid in sag_results)
            corr.qa.sag_exp.value = all(abs(sag) < SAG_TOLERANCE for sag, valid in sag_results)

            # apply sag correction to source trajectory
            for st, sag in zip(corr.stations, corr.sag):
                st.inc -= sag
                st.dinc -= sag


def calc_dls(stations: List[Station]) -> List[Tuple[float, float]]:
    res = [(0, 0)] * len(stations)
    for (i, st) in enumerate(stations):
        srev = reversed(stations)
        sp = next((s for s in srev if s.md < st.md - 10.), None)
        sn = next((s for s in stations if s.md > st.md + 10.), None)
        dlsp = (st.inc - sp.inc) / (st.md - sp.md) if sp is not None else 0.
        dlsn = (sn.inc - st.inc) / (sn.md - st.md) if sn is not None else dlsp / 2.0
        if sp is None:
            dlsp = dlsn / 2.0
        res[i] = (dlsp, dlsn)
    return res


class LRUCache:
    def __init__(self, capacity: int):
        self.cache = OrderedDict()
        self.capacity = capacity
    def get(self, key: Tuple[str, float]) -> Dict[Tuple[float, float, float], Tuple[float, bool]]:
        if key not in self.cache:
            return None
        else:
            self.cache.move_to_end(key)
            return self.cache[key]
    def put(self, key: Tuple[str, float], value: int) -> None:
        self.cache[key] = value
        self.cache.move_to_end(key)
        if len(self.cache) > self.capacity:
            self.cache.popitem(last = False)

bha_cache = LRUCache(10)


def get_cached_sag(inc: float, dls1: float, dls2: float, bha: BHA, mud_weight: float) -> Tuple[float, bool]:
    table = bha_cache.get((repr(bha), mud_weight))
    if table is None:
        return None
    return table.get((inc, dls1, dls2))

def cache_sag(inc: float, dls1: float, dls2: float, bha: BHA, mud_weight: float, sag: float, valid: bool):
    table = bha_cache.get((repr(bha), mud_weight))
    if table is None:
        table = {}
        bha_cache.put((repr(bha), mud_weight), table)
    table[(inc, dls1, dls2)] = (sag, valid)

def run_sagcor(inc: float, dls1: float, dls2: float, bha: BHA, mud_weight: float):
    if inc < radians(5.):
        return 0., True
    inc = radians(round(degrees(inc)))
    dls1 = radians(round(degrees(dls1)*60.)/60.) # round to 0.5 deg/30m (or 1 deg/60m)
    dls2 = radians(round(degrees(dls2)*60.)/60.) # round to 0.5 deg/30m (or 1 deg/60m)
    cached = get_cached_sag(inc, dls1, dls2, bha, mud_weight)
    if cached is not None:
        return cached
    bit_depth = bha.dni_to_bit
    md1 = bit_depth - bha.length - 10
    inc1 = inc + dls1 * md1
    md2 = bit_depth + 10
    inc2 = inc + dls2 * md2
    traj = [Station(md1, inc1, 0), Station(0., inc, 0), Station(md2, inc2, 0.)]
    res = sagcor(bha, bit_depth, traj, radians(90.), mud_weight)
    cache_sag(inc, dls1, dls2, bha, mud_weight, res.sag, res.valid)
    return res.sag, res.valid
