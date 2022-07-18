import attr


@attr.s(auto_attribs=True)
class CIStation:
    md: float
    inc: float


@attr.s(auto_attribs=True)
class Station:
    md: float
    inc: float
    az: float


@attr.s(auto_attribs=True)
class TfStation(Station):
    tf: float = attr.ib(default=0., converter=attr.converters.default_if_none(0.))


@attr.s(auto_attribs=True, kw_only=True)
class FullStation(TfStation):
    tg: float
    tb: float
    dip: float


@attr.s(auto_attribs=True, kw_only=True)
class CorrectedStation(FullStation):
    dmd: float
    dinc: float
    daz: float


@attr.s(auto_attribs=True)
class Position:
    ns: float
    ew: float
    tvd: float


@attr.s(auto_attribs=True)
class StationPosition(Station, Position):
    pass
