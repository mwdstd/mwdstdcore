from enum import Enum
import attr


class SlideMode(str, Enum):
    tangent = 'tangent'
    curve = 'curve'


class TfMode(str, Enum):
    gtf = 'gtf'
    mtf = 'mtf'


@attr.s(auto_attribs=True)
class SlideInterval:
    md_start: float
    md_stop: float
    mode: SlideMode
    tf_mode: TfMode = attr.ib(default=TfMode.gtf, converter=attr.converters.default_if_none(TfMode.gtf))
    tf_value: float = attr.ib(default=0., converter=attr.converters.default_if_none(0.))
    steer_ratio: float = attr.ib(default=1., converter=attr.converters.default_if_none(1.))
