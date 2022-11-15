from typing import List, Optional
from datetime import datetime
import jsons
import attr

from .core import api
from ..utils import json_call
from ..apierror import RequestMalformed

from .models import NorthType
from .ref import head_reference, plan_reference
from mwdstdcore.datamodel import Station
from mwdstdcore.errormods.gmagmod import gmagmod, bggm


@attr.s(auto_attribs=True)
class Point:
    ns: float
    ew: float
    tvd: float


@attr.s(auto_attribs=True)
class Params:
    latitude: float
    longitude: float
    altitude: float
    date: datetime
    gmag_mod: str
    crustal_field: bool
    plan: Optional[List[Station]] = None
    north_type: NorthType = attr.ib(default=NorthType.true, converter=[attr.converters.default_if_none(default=NorthType.true), NorthType], validator=attr.validators.in_(NorthType))
    altitude_type: str = 'MSL'


@api.route('/refcalc', methods=['POST'])
@json_call
def api_gmag_point(jsn):
    try:
        rq = jsons.load(jsn, Params)
    except:
        raise RequestMalformed

    base_point = head_reference(rq.gmag_mod, rq.crustal_field, rq.latitude, rq.longitude, rq.altitude, rq.date)

    refmod_name = 'HDGM' if rq.gmag_mod == 'EMM2017' else 'WMM'
    refmod = gmagmod.get(refmod_name, bggm)
    
    if rq.plan is None or len(rq.plan) < 2:
        return {
            'err_model': {'name': refmod_name, **refmod},
            'base_point': base_point,
        }

    points = plan_reference(rq.gmag_mod, rq.crustal_field, rq.latitude, rq.longitude, rq.altitude, rq.date, rq.plan, rq.north_type)

    return {
        'err_model': {'name': refmod_name, **refmod},
        'base_point': base_point, 
        'points': [ {'md': rq.plan[i].md, **attr.asdict(p)} for i, p in enumerate(points)]
    }
