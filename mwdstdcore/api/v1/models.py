from typing import List, Optional, Union
from enum import Enum
from typing import List
import attr
from mwdstdcore.datamodel import BHA, Correction, ManualCorrection, Reference, SlideInterval, Station, Survey, CIStation, DnIParams


@attr.s(auto_attribs=True, kw_only=True)
class SurveyRef(Survey):
    g: float
    b: float
    dip: float


@attr.s(auto_attribs=True, kw_only=True)
class QcBase:
    qc: int
    fa: bool


@attr.s(auto_attribs=True, kw_only=True)
class SurveyQc(Survey, QcBase):
    pass


@attr.s(auto_attribs=True, kw_only=True)
class SurveyRefQc(SurveyRef, QcBase):
    pass


class NorthType(str, Enum):
    true = 'true'
    grid = 'grid'


@attr.s(auto_attribs=True)
class Interval:
    start: float = -100.
    stop: float = -100.

    def __getitem__(self, item):
        if item == 0:
            return self.start
        if item == 1:
            return self.stop
        return None


@attr.s(auto_attribs=True)
class ManualCorrectionIn:
    dni_cs: DnIParams
    sag_tag: str = ''


@attr.s(auto_attribs=True, kw_only=True)
class Run0:
    surveys: List[Survey]
    reference: List[Reference]
    interference_intervals: List[Interval] = attr.ib(factory=list)
    casing_depth: float = attr.ib(default=-100., converter=attr.converters.default_if_none(-100.))
    dni_rigid: bool
    correction: Optional[Union[Correction, ManualCorrection, ManualCorrectionIn]]
    status_multi: bool = False
    status_auto: bool = True
    status_msa: bool = True


@attr.s(auto_attribs=True, kw_only=True)
class Run2(Run0):
    bha: BHA
    mud_weight: float


@attr.s(auto_attribs=True, kw_only=True)
class Run3(Run2):
    slidesheet: List[SlideInterval] = attr.ib(factory=list)
    ci: Optional[List[CIStation]] = None


@attr.s(auto_attribs=True)
class Result0:
    corrections: List[Optional[Correction]]