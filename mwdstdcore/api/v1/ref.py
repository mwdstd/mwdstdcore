from datetime import datetime
from typing import List
import math
import numpy as np
from .models import NorthType
from mwdstdcore.gmag.maglib.date import Date
from mwdstdcore.gmag.gmagcalc.gmag import gmag_point, gmag_traj, grid_conv, gravity
from mwdstdcore.gmag.geolib.localcoord import CoordLocal
from mwdstdcore.datamodel import Survey, Station, Reference
from mwdstdcore.core.common.mincurv import mincurv


def head_reference(gmag_mod_name: str, gmag_use_crustfield: bool, lat: float, lon: float, alt: float, date: datetime):
    lat = math.degrees(lat)
    lon = math.degrees(lon)
    date = Date(day=date.day, month=date.month, year=date.year)    
    
    g = gravity(lat)
    grid = grid_conv(lat, lon)

    pt = gmag_point(lat, lon, alt * 1e-3, date, gmag_mod=gmag_mod_name,
                    crustal_field=False)
    b = math.sqrt(pt.X * pt.X + pt.Y * pt.Y + pt.Z * pt.Z)
    dec = math.atan2(pt.Y, pt.X)
    dip = math.asin(pt.Z / b)

    return Reference(g=g, b=b, dip=dip, dec=dec, grid=grid)


def plan_reference(gmag_mod_name: str, gmag_use_crustfield: bool, lat: float, lon: float, alt: float, date: datetime, plan: List[Station], north_type: NorthType):
    lat = math.degrees(lat)
    lon = math.degrees(lon)
    date = Date(day=date.day, month=date.month, year=date.year)    
    
    g = gravity(lat)
    grid = grid_conv(lat, lon)

    dia = np.array(list(map(lambda st: [st.md, st.inc, st.az], plan)))
    if north_type == NorthType.grid:  # if grid
        dia[:, 2] = dia[:, 2] + grid
    nev = mincurv(dia, [0, 0, 0])
    pts = list(map(lambda pt: CoordLocal(ns=pt[0], ew=pt[1], tvd=pt[2]), nev.tolist()))
    tr = gmag_traj(lat, lon, alt * 1e-3, date, pts, gmag_mod=gmag_mod_name, crustal_field=False)
    bxyz = np.array(list(map(lambda pt: [pt.X, pt.Y, pt.Z], tr)))
    b = np.sqrt(np.sum(bxyz * bxyz, 1))
    dec = np.arctan2(bxyz[:, 1], bxyz[:, 0])
    dip = np.arcsin(bxyz[:, 2] / b)

    return list(map(lambda _b, _dip, _dec: Reference(g=g, b=_b, dip=_dip, dec=_dec, grid=grid), b, dip, dec))


def run_reference(planmd: List[float], plan_ref: List[Reference], surveys: List[Survey]):
    planmd = np.array(planmd)
    md = list(map(lambda s: s.md, surveys))
    b = list(map(lambda s: s.b, plan_ref))
    dec = list(map(lambda s: s.dec, plan_ref))
    dip = list(map(lambda s: s.dip, plan_ref))
    g = plan_ref[0].g
    grid = plan_ref[0].grid
    bs = np.interp(md, planmd, b)            
    decs = np.interp(md, planmd, dec)            
    dips = np.interp(md, planmd, dip)
    return list(map(lambda _b, _dip, _dec: Reference(g=g, b=_b, dip=_dip, dec=_dec, grid=grid), bs, dips, decs))