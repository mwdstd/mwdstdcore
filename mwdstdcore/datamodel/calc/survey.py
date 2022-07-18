from ..survey import Survey
from ..station import FullStation
from math import sin, cos


def calc_survey(s: FullStation, dec: float = 0., grid: float = 0., sag=0.) -> Survey:
    inc = s.inc + sag
    az = s.az - (dec - grid)
    sini, cosi = sin(inc), cos(inc)
    sina, cosa = sin(az), cos(az)
    sintf, costf = sin(s.tf), cos(s.tf)
    bcosd = s.tb*cos(s.dip)
    bsind = s.tb*cos(s.dip)
    return Survey(
        md = s.md,
        gx = -s.tg*sini*sintf,
        gy = -s.tg*sini*costf,
        gz = s.tg*cosi,
        bx = bcosd * cosi * cosa * sintf - bsind * sini * sintf + bcosd * sina * costf,
        by = bcosd * cosi * cosa * costf - bsind * sini * costf - bcosd * sina * sintf,
        bz = bcosd * sini * cosa + bsind * cosi
    )
