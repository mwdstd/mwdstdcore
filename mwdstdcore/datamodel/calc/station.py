from mwdstdcore.datamodel.ref import RefParams
import math
from ..survey import Survey
from ..station import Station, FullStation, CorrectedStation


def _calc(s: Survey):
    g = math.sqrt(s.gx * s.gx + s.gy * s.gy + s.gz * s.gz)
    b = math.sqrt(s.bx * s.bx + s.by * s.by + s.bz * s.bz)
    dip = math.asin((s.gx * s.bx + s.gy * s.by + s.gz * s.bz) / (g * b))
    a1 = s.bz / b - s.gz / g * math.sin(dip)
    a2 = (s.gy * s.bx - s.gx * s.by) / (g * b)
    return g, b, dip, a1, a2

def calc_gbd(s: Survey):
    return RefParams.fromarray(_calc(s))

def calc_gtf(s: Survey) -> float:
    return math.atan2(s.gx, -s.gy)


def calc_station(s: Survey, dec: float = 0., grid: float = 0., sag=0.) -> Station:
    g, _, _, a1, a2 = _calc(s)
    return Station(
        md=s.md,
        inc=math.acos(s.gz / g) - sag,
        az=(math.atan2(a2, a1) + (dec - grid) + 2 * math.pi) % (2 * math.pi)
    )


def calc_full_station(s: Survey, dec: float = 0., grid: float = 0., sag=0.) -> FullStation:
    g, b, dip, a1, a2 = _calc(s)
    return FullStation(
        md=s.md,
        inc=math.acos(s.gz / g) - sag,
        az=(math.atan2(a2, a1) + (dec - grid) + 2 * math.pi) % (2 * math.pi),
        tf=calc_gtf(s),
        tg=g, tb=b, dip=dip
    )


def calc_corrected_station(s: Survey, st: Station, dec: float = 0., grid: float = 0., sag=0.) -> CorrectedStation:
    g, b, dip, a1, a2 = _calc(s)
    inc=math.acos(s.gz / g) - sag
    az=(math.atan2(a2, a1) + (dec - grid) + 2 * math.pi) % (2 * math.pi)
    cos_x = math.cos(az) * math.cos(st.az) + math.sin(az) * math.sin(st.az)
    sin_x = math.cos(st.az) * math.sin(az) - math.sin(st.az) * math.cos(az)
    daz = math.atan2(sin_x, cos_x)
    return CorrectedStation(
        md=s.md,
        inc=inc,
        az=az,
        tf=calc_gtf(s),
        tg=g, tb=b, dip=dip,
        dmd=s.md - st.md,
        dinc=inc - st.inc,
        daz=daz
    )
