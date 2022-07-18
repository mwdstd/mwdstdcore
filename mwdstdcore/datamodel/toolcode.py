from typing import Optional, Tuple
from enum import Enum
import attr


class ToolcodeDniAccuracy(str, Enum):
    msa2 = 'MSA2'
    msa1 = 'MSA1'
    std = 'STD'
    red = 'RED'
    poor = 'POOR'
    incl_only = 'INCL_ONLY'
    unknown = 'UNKNOWN'


class ToolcodeMisalignment(str, Enum):
    sag = 'SAG'
    sag1 = 'SAG1'
    sag2 = 'SAG2'


class ToolcodeDeclination(str, Enum):
    hd = 'HD'
    hd0 = 'HD0'
    hd1 = 'HD1'
    hd2 = 'HD2'


@attr.s(auto_attribs=True)
class Toolcode:
    base_name: str
    dni: Optional[ToolcodeDniAccuracy] = None
    mis: Optional[ToolcodeMisalignment] = None
    dec: Optional[ToolcodeDeclination] = None

    def __str__(self) -> str:
        res = self.base_name
        if self.dni is not None:
            res = f'{res}_{self.dni}'
        if self.mis is not None:
            res = f'{res}_{self.mis}'
        if self.dec is not None:
            res = f'{res}_{self.dec}'
        return res


@attr.s(auto_attribs=True)
class GeneratedToolcode:
    name: str
    scale: Tuple[float, float, float] = (1., 1., 1.)


@attr.s(auto_attribs=True)
class ProvidedToolcode:
    name: str
    terms: dict


class ToolCodes(str, Enum):
    # mwd = 'ISCWSA MWD Rev0'
    # mwd_fl = 'ISCWSA MWD Rev0_Fl'
    mwd_rev4 = 'ISCWSA MWD REV4'
    blind = 'BLIND'
    incl_only = 'INCL-ONLY'
    gwd_omega = 'OMEGA-X'
    mwd_test = 'MWD_TEST'
    gwd_test = 'GWD_TEST'
    # mwd_rev4_fl = 'ISCWSA MWD Rev4_Fl'
