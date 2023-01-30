import argparse
import sys
from math import degrees, radians
from typing import List

import attr
import jsons

from mwdstdcore.datamodel import CIStation, TfStation
from mwdstdcore.datamodel.calc.station import bound_az
from mwdstdcore.steer.cinc2traj import cinc2traj
from mwdstdcore.steer.opt4hd import opt4hd


def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)


@attr.s(auto_attribs=True)
class Params:
    stations: List[TfStation]
    ci: List[CIStation]

@attr.s(auto_attribs=True)
class Result:
    stations: List[TfStation]
    qc_ci_vld: bool
    qc_ci_denst: bool
    

def main():
    parser = argparse.ArgumentParser(description='HD trajectory calculation')
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

    for s in rq.stations:
        s.inc = radians(s.inc)
        s.az = radians(s.az)
        s.tf = radians(s.tf)
    for s in rq.ci:
        s.inc = radians(s.inc)

    traj_hd, srv_freq_qc, ci_vrf_qc = cinc2traj(rq.ci, rq.stations)
    md_cont_inc = [ci.md for ci in rq.ci]
    md_stations = [stn.md for stn in rq.stations]
    stations_hd = opt4hd(md_stations, md_cont_inc, traj_hd)
    
    for s in stations_hd:
        s.inc = degrees(s.inc)
        s.az = degrees(bound_az(s.az))
        s.tf = degrees(s.tf)

    res = Result(stations=stations_hd, qc_ci_vld=ci_vrf_qc, qc_ci_denst=srv_freq_qc)
    args.output.write(jsons.dumps(res))