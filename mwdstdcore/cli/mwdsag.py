import argparse
import sys
from math import degrees, radians
from typing import Dict, List, Tuple

import attr
import jsons

from mwdstdcore.datamodel import BHA, Station
from mwdstdcore.sag.sagcor import sagcor
from mwdstdcore.api.v1.sag import calc_dls


@attr.s(auto_attribs=True)
class Params:
    bha: BHA
    stations: List[Station]
    mud_weight: float


def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)


def main():
    parser = argparse.ArgumentParser(description='BHA sag correction')
    parser.add_argument('FILE', type=argparse.FileType('r'), help='an input .JSON file')
    parser.add_argument('-o', '--output', type=argparse.FileType('w'), default='-', metavar='OUT', help='an output .JSON file')
    parser.add_argument('-v', '--verbose', action='store_true',)
    args = parser.parse_args()

    if args.verbose:
        eprint(f'FILE: {args.FILE}')
        eprint(f'OUT: {args.output}')

    try:
        rq: Params = jsons.loads(args.FILE.read(), Params)
    except ValueError as e:
        eprint(f"mwdsag: error: can't parse JSON file: {e}")
        exit(2)

    dlss = calc_dls(rq.stations)
    sags = [run_sagcor(s.inc, dls[0], dls[1], rq.bha, rq.mud_weight) for s, dls in zip(rq.stations, dlss)]
    sags = [(degrees(s[0]), s[1]) for s in sags]
    
    args.output.write(jsons.dumps(sags))


table: Dict[Tuple[float,float,float], Tuple[float, bool]] = {}


def get_cached_sag(inc: float, dls1: float, dls2: float, bha: BHA, mud_weight: float) -> Tuple[float, bool]:
    return table.get((inc, dls1, dls2))


def cache_sag(inc: float, dls1: float, dls2: float, bha: BHA, mud_weight: float, sag: float, valid: bool):
    table[(inc, dls1, dls2)] = (sag, valid)
    

def run_sagcor(inc: float, dls1: float, dls2: float, bha: BHA, mud_weight: float) -> Tuple[float, bool]:
    if inc < 5.:
        return 0., True
    inc = radians(round(inc))
    dls1 = radians(round(dls1*60.)/60.) # round to 0.5 deg/30m (or 1 deg/60m)
    dls2 = radians(round(dls2*60.)/60.) # round to 0.5 deg/30m (or 1 deg/60m)
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


# if __name__ == '__main__':
#     sys.argv = ['mwdsag', 'sagrq.json']
#     main()