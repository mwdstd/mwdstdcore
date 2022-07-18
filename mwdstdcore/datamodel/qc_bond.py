from math import acos, cos
from typing import Optional
import attr
from .ref import RefParams


@attr.s(auto_attribs=True, kw_only=True)
class QcBoundary(RefParams):
    inc: Optional[float] = None
    az: Optional[float] = None


@attr.s(auto_attribs=True, kw_only=True)
class Qc:
    g: bool
    b: bool
    dip: bool
    inc: Optional[bool] = None
    az: Optional[bool] = None

    def setIncAz(self, val, min, max):
        self.inc = min.inc <= val.inc <= max.inc
        paz = 0.5 * (min.az + max.az)
        uaz = 0.5 * (max.az - min.az)
        self.az = acos(cos(val.az - paz)) <= 2. * uaz

    @classmethod
    def fromValBnd(cls, val: RefParams, min: QcBoundary, max: QcBoundary):
        return cls(
            g=min.g <= val.g <= max.g,
            b=min.b <= val.b <= max.b,
            dip=min.dip <= val.dip <= max.dip,
        )

