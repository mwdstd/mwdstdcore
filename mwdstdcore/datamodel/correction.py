from typing import List, Dict, Optional, Tuple
import attr
import numpy as np

from .cor_survey import CorrectedSurvey, ManualCorrectedSurvey
from .qa import QualityAssessment
from .ref import RefParams
from .dni_params import DnIParams
from .station import CorrectedStation, StationPosition, TfStation, Station
from .calc.station import calc_full_station, calc_corrected_station


@attr.s(auto_attribs=True)
class ManualCorrection:
    dni_cs: DnIParams
    qa: QualityAssessment
    surveys: List[ManualCorrectedSurvey]
    stations: List[CorrectedStation] = attr.ib(factory=list)
    sag: Optional[List[float]] = None
    stations_hd: Optional[List[TfStation]] = None
    deepest: Optional[StationPosition] = None
    plan_dev: Optional[StationPosition] = None

    def get_std_inc_idx(self):
        return self.get_std_idx()

    def get_std_idx(self):
        return [i for i, s in enumerate(self.surveys) if s.qc == 0]

    def get_std_stations(self):
        return [s for i, s in enumerate(self.stations) if self.surveys[i].qc == 0]


@attr.s(auto_attribs=True)
class Correction:
    dni_cs: DnIParams
    ref_cs: RefParams
    apr_unc: Dict[str, float]
    apst_unc: DnIParams
    ref_unc: RefParams
    ref_cov: List[List[float]]
    qa: QualityAssessment
    surveys: List[CorrectedSurvey]
    stations: List[CorrectedStation] = attr.ib(factory=list)
    sag: Optional[List[float]] = None
    stations_hd: Optional[List[TfStation]] = None
    deepest: Optional[StationPosition] = None
    plan_dev: Optional[StationPosition] = None

    def get_std_inc_idx(self):
        return [i for i, s in enumerate(self.surveys) if s.qc == 0 and s.inc_pass]

    def get_std_idx(self):
        return [i for i, s in enumerate(self.surveys) if s.qc == 0]

    def get_std_stations(self):
        return [s for i, s in enumerate(self.stations) if self.surveys[i].qc == 0]


def set2cor(apr_unc, dni_xyz_cor, dni_cor, ref_cor, apst_vect, ref_cov_mat, inc_stat, inc_unc, az_stat, az_unc,
            gbd_boundaries, survey_status, validity, run):
    num = inc_stat.shape[0]
    surveys = CorrectedSurvey.listFromSets(run.surveys, run.reference, dni_xyz_cor, gbd_boundaries, inc_unc, az_unc,
                                           inc_stat, az_stat, survey_status)
    raw_stations = [calc_full_station(s, dec=r.dec, grid=r.grid) for s, r in zip(run.surveys, run.reference)]
    stations = [
        calc_corrected_station(surveys[i], raw_stations[i], dec=run.reference[i].dec, grid=run.reference[i].grid) for i
        in range(0, num)]
    return Correction(
        dni_cs=DnIParams.fromarray(dni_cor),
        ref_cs=RefParams.fromarray(ref_cor),
        apr_unc=apr_unc,
        apst_unc=DnIParams.fromarray(apst_vect),
        ref_unc=RefParams.fromarray(np.sqrt(np.diag(ref_cov_mat))),
        ref_cov=ref_cov_mat.tolist(),
        qa=validity,
        surveys=surveys,
        stations=stations)
