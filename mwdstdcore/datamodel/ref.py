import attr
import numpy as np


@attr.s(auto_attribs=True)
class Reference:
    g: float
    b: float
    dip: float
    dec: float = 0.
    grid: float = 0.


@attr.s(auto_attribs=True)
class RefParams:
    g: float
    b: float
    dip: float

    def toarray(self):
        return np.array([self.g, self.b, self.dip])

    @classmethod
    def fromarray(cls, a):
        return cls(g=a[0], b=a[1], dip=a[2])


def get_default_boundaries():
    return RefParams(g = 2.5e-3 * 9.80665, b = 300, dip = 0.00785)