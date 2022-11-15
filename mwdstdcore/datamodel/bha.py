from enum import Enum
from typing import List
from itertools import accumulate
import attr
from .validators import gte, list_non_empty


class BhaElementType(str, Enum):
    bit = 'bit'
    motor = 'motor'
    rss = 'rss'
    bend_sub = 'bend_sub'
    sub = 'sub'
    string_stabilizer = 'string_stabilizer'
    reamer = 'reamer'
    mwd = 'mwd'
    lwd = 'lwd'
    hwdc = 'hwdc'
    hwdp = 'hwdp'
    nmdc = 'nmdc'
    drill_pipe = 'drill_pipe'
    collar = 'collar'
    jar = 'jar'
    other = 'other'


class Material(str, Enum):
    aluminum = "aluminum"
    beryllium_copper = "beryllium_copper"
    chrome_alloy = "chrome_alloy"
    composite = "composite"
    other = "other"
    nm_steel = "nmsteel"
    plastic = "plastic"
    steel = "steel"
    steel_alloy = "steel_alloy"
    titanium = "titanium"


def id_less_than_od(self, attr, val):
    if val >= self.od:
        raise ValueError("Outer diameter is less than inner")


@attr.s(auto_attribs=True)
class BhaElement:
    type: BhaElementType = attr.ib(converter=BhaElementType, validator=attr.validators.in_(BhaElementType))
    od: float = attr.ib(validator=gte(0.))
    id: float = attr.ib(validator=[gte(0.), id_less_than_od])
    weight: float = attr.ib(validator=gte(0.))
    length: float = attr.ib(validator=gte(0.))
    material: Material = attr.ib(converter=Material, validator=attr.validators.in_(Material))
    description: str = None
    sn: str = None


@attr.s(auto_attribs=True)
class Blade:
    od: float = attr.ib(validator=gte(0.))
    center_to_bit: float = attr.ib(validator=gte(0.))
    length: float = attr.ib(validator=gte(0.))


@attr.s(auto_attribs=True)
class BHA:
    structure: List[BhaElement] = attr.ib(validator=list_non_empty)
    blades: List[Blade] = attr.ib()
    dni_to_bit: float = attr.ib(validator=gte(0.))
    bend_angle: float = attr.ib(default=0., validator=gte(0.))  # if no bend elements present
    bend_to_bit: float = attr.ib(default=0., validator=gte(0.))  # if no bend elements present
    tf_correction: float = attr.ib(default=0.)  # SL >= 2 BHA has motor

    @bend_angle.validator
    def bends_check(self, attr, val):
        if val > 0. or self.bend_to_bit > 0.:
            accumulate((el.length for el in self.structure))
        # if bend angle > 0 or bend_to_bit > 0
        # if outside of bend element
        # raise
        pass

    @bend_angle.validator
    def dni_check(self, attr, val):
        pass

    @property
    def length(self) -> float:
        return sum(el.length for el in self.structure)
