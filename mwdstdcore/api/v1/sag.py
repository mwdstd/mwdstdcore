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
            # calculate sag
            with DebugTimer(f"Sag{ri}: {{:0.2f}}"):
                sag_results = [
                    run_sagcor(st.inc, run.bha, run.mud_weight) for st in corr.stations
                ]
            corr.sag = [sag for sag, valid in sag_results]
            corr.qa.sag_conv.value = all(valid for sag, valid in sag_results)
            corr.qa.sag_exp.value = all(abs(sag) < SAG_TOLERANCE for sag, valid in sag_results)

            # apply sag correction to source trajectory
            for st, sag in zip(corr.stations, corr.sag):
                st.inc -= sag
                st.dinc -= sag


class LRUCache:
    def __init__(self, capacity: int):
        self.cache = OrderedDict()
        self.capacity = capacity
    def get(self, key: Tuple[str, float]) -> Dict[float, Tuple[float, bool]]:
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

def get_cached_sag(inc: float, bha: BHA, mud_weight: float) -> Tuple[float, bool]:
    table = bha_cache.get((repr(bha), mud_weight))
    if table is None:
        return None
    return table.get(inc)

def cache_sag(inc: float, bha: BHA, mud_weight: float, sag: float, valid: bool):
    table = bha_cache.get((repr(bha), mud_weight))
    if table is None:
        table = {}
        bha_cache.put((repr(bha), mud_weight), table)
    table[inc] = (sag, valid)

def run_sagcor(inc: float, bha: BHA, mud_weight: float):
    if inc < radians(5.):
        return 0., True
    inc = radians(round(degrees(inc)))
    cached = get_cached_sag(inc, bha, mud_weight)
    if cached is not None:
        return cached
    bit_depth = bha.dni_to_bit
    traj = [Station(bit_depth - bha.length - 10, inc, 0), Station(bit_depth + 10, inc, 0.)]
    res = sagcor(bha, bit_depth, traj, radians(90.), mud_weight)
    cache_sag(inc, bha, mud_weight, res.sag, res.valid)
    return res.sag, res.valid
