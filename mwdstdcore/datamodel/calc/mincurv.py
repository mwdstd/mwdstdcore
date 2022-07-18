from typing import List
import math as m
from ..station import Station


def mcint_station(s1: Station, s2: Station, md: float) -> Station:
    sinI1 = m.sin(s1.inc)
    sinI2 = m.sin(s2.inc)
    cosI1 = m.cos(s1.inc)
    cosI2 = m.cos(s2.inc)
    cosA1 = m.cos(s1.az)
    cosA2 = m.cos(s2.az)
    sinA1 = m.sin(s1.az)
    sinA2 = m.sin(s2.az)
    cosdI = m.cos(s2.inc - s1.inc)
    cosdA = m.cos(s2.az - s1.az)

    DL = m.acos(cosdI - sinI1 * sinI2 * (1 - cosdA))

    a1 = cosA1 * sinI1
    a2 = cosA2 * sinI2
    b1 = sinA1 * sinI1
    b2 = sinA2 * sinI2
    c1 = cosI1
    c2 = cosI2

    ksi = b1 * c2 - b2 * c1
    eta = a2 * c1 - a1 * c2
    zeta = a1 * b2 - a2 * b1

    len2 = ksi * ksi + eta * eta + zeta * zeta

    if len2 < 1e-10:
        inc = m.acos(c1)
        az = (m.atan2(b1, a1) + 2 * m.pi) % (2 * m.pi)
        return Station(md, inc, az)

    dMD_ = s2.md - s1.md
    cos1 = m.cos((md - s1.md) * DL / dMD_)
    cos2 = m.cos((s2.md - md) * DL / dMD_)

    d = (a1 * cos2 - a2 * cos1)
    e = (b1 * cos2 - b2 * cos1)
    f = (c1 * cos2 - c2 * cos1)

    x = (eta * f - zeta * e) / len2
    y = (zeta * d - ksi * f) / len2
    z = (ksi * e - eta * d) / len2

    inc = m.acos(z)
    az = (m.atan2(y, x) + 2 * m.pi) % (2 * m.pi)

    return Station(md, inc, az)


def mcint_traj(stations: List[Station], md: float) -> Station:
    exact_matches = [s for s in stations if s.md == md]
    if len(exact_matches) > 0:
        return exact_matches[0]
    intervals = [(s1, s2) for s1, s2 in zip(stations[:-1], stations[1:]) if s1.md <= md <= s2.md]
    if len(intervals) != 1:
        raise ValueError("Interpolation depth not in trajectory range")
    return mcint_station(*intervals[0], md)
