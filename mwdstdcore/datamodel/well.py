from datetime import datetime
from typing import List, Optional
import attr
from .station import Station, TfStation
from .run import Run
from .correction import Correction
from .ref import Reference
from .link import Links
from .toolcode import GeneratedToolcode, ProvidedToolcode


@attr.s(auto_attribs=True)
class Well:
    runs: List[Run]
    plan: List[Station]
    north_type: int
    latitude: float
    longitude: float
    altitude: float
    date: datetime

    gmag_mod_name: str = 'EMM2017'
    gmag_use_crustfield: bool = True


@attr.s(auto_attribs=True)
class WellShort:
    north_type: int
    latitude: float
    longitude: float
    altitude: float
    date: datetime
    plan: List[Station] = None
    gmag_mod_name: str = 'EMM2017'
    gmag_use_crustfield: bool = True


@attr.s(auto_attribs=True)
class SurveyLeg:
    stations: List[TfStation]
    toolcode: ProvidedToolcode


@attr.s(auto_attribs=True)
class FusedSurveyLeg:
    stations: List[TfStation]
    toolcode: GeneratedToolcode


@attr.s(auto_attribs=True)
class MwdRun:
    stations: List[TfStation]
    toolcode: Optional[ProvidedToolcode] = None
    correction: Optional[Correction] = None


@attr.s(auto_attribs=True, kw_only=True)
class WellPosUnc:
    plan: List[SurveyLeg]
    runs_mwd: List[MwdRun]

    head_reference: Reference
    lat: float
    gmag_mod_name: str
    float_rig: bool
    declination_unc_estimation: bool = False

    links: Links = None
    slot_unc: float = 0.3  # m


@attr.s(auto_attribs=True, kw_only=True)
class WellFusion(WellPosUnc):
    runs_gwd: List[SurveyLeg]
