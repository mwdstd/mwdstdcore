from typing import List, Optional
import attr
from .survey import Survey
from .accu import Accuracy
from .qc_bond import QcBoundary, Qc
from .calc.station import calc_gbd
from .ref import RefParams


@attr.s(auto_attribs=True, kw_only=True)
class ManualCorrectedSurvey(Survey):
    min: Optional[QcBoundary] = None
    max: Optional[QcBoundary] = None
    qc_pass: Qc = None
    qc: int = 2  # STD = 0, INC = 1, BAD = 2


@attr.s(auto_attribs=True, kw_only=True)
class CorrectedSurvey(Survey, Accuracy):
    min: QcBoundary
    max: QcBoundary
    qc_pass: Qc
    qc: int  # STD = 0, INC = 1, BAD = 2
    fa: int  # None = -1, AF{XYZ} = {012}, MF{XYZ} = {345}

    @classmethod
    def listFromSets(cls, raw_surveys: List[Survey], reference: List[RefParams], dni_xyz_cor, gbd_boundaries, inc_unc, az_unc, inc_stat, az_stat, srv_stat = None, ax_stat=None):
        mds = [s.md for s in raw_surveys]
        cor_surveys = ManualCorrectedSurvey.listFromArrays(mds, dni_xyz_cor)
        gbds = [calc_gbd(s) for s in cor_surveys]
        qc_mins = [QcBoundary(g=reference[i].g + gbd_boundaries[i, 1], b=reference[i].b + gbd_boundaries[i, 3], dip=reference[i].dip + gbd_boundaries[i, 5]) for i, s in enumerate(raw_surveys)]
        qc_maxs = [QcBoundary(g=reference[i].g + gbd_boundaries[i, 0], b=reference[i].b + gbd_boundaries[i, 2], dip=reference[i].dip + gbd_boundaries[i, 4]) for i, s in enumerate(raw_surveys)]
        qc_passes = [Qc.fromValBnd(val, min, max) for val, min, max in zip(gbds, qc_mins, qc_maxs)]
        return [
            cls(
                md=s.md,
                gx=dni_xyz_cor[i, 0],
                gy=dni_xyz_cor[i, 1],
                gz=dni_xyz_cor[i, 2],
                bx=dni_xyz_cor[i, 3],
                by=dni_xyz_cor[i, 4],
                bz=dni_xyz_cor[i, 5],
                qc=s.qc if srv_stat is None else srv_stat[i],
                fa=s.fa if ax_stat is None else ax_stat[i],
                min=qc_mins[i],
                max=qc_maxs[i],
                qc_pass=qc_passes[i],
                inc_unc=inc_unc[i, 0],
                inc_unc_ref=inc_unc[i, 1],
                az_unc=az_unc[i, 0],
                az_unc_ref=az_unc[i, 1],
                inc_pass=bool(inc_stat[i]),
                az_pass=bool(az_stat[i])
            )
            for i, s in enumerate(raw_surveys)
        ]
