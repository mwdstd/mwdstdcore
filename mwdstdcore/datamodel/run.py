from typing import List
import attr
import numpy as np
from mwdstdcore.api.apierror import RequestDataError
from mwdstdcore.errormods.codes import def_pattern
from .interval import Interval
from .ref import Reference
from .slide import SlideInterval
from .survey import Survey
from .correction import Correction
from .bha import BHA


CASING_OFFSET = 20.  # m


@attr.s(auto_attribs=True)
class Run:
    surveys: List[Survey]

    edi: float
    dni_rigid: bool
    bha: BHA = None
    slidesheet: List[SlideInterval] = None
    # dni2bit: float = -100.
    casing_depth: float = -100.
    exti_interval: Interval = attr.ib(factory=Interval)
    mode: str = 'model'
    eterm_sigma: float = 1.
    min_inc_err: float = 0.
    min_az_err: float = 0.

    # controlling flags
    status_auto: bool = True
    status_msa: bool = True
    status_multi: bool = False
    # status_recalc: bool = True #equivalent of correction is not None

    correction: Correction = None
    reference: List[Reference] = None

    __md = None

    @property
    def md(self):
        if self.__md is None:
            self.__md = np.array(list(map(lambda s: s.md, self.surveys)))
        return self.__md

    __dni_xyz = None

    @property
    def dni_xyz(self):
        if self.__dni_xyz is None:
            self.__dni_xyz = np.array(list(map(lambda s: [s.gx, s.gy, s.gz, s.bx, s.by, s.bz], self.surveys)))
        return self.__dni_xyz

    @property
    def dni_xyz_cor(self):
        if self.__dni_xyz is None:
            self.__dni_xyz = np.array(list(map(lambda s: [s.gx, s.gy, s.gz, s.bx, s.by, s.bz], self.surveys)))
        return self.__dni_xyz

    __ref = None

    @property
    def ref(self):
        if self.__ref is None:
            if self.reference is None or len(self.surveys) != len(self.reference):
                raise RequestDataError()  # bad reference data

            self.__ref = np.array(list(map(lambda r: [r.g, r.b, r.dip], self.reference)))
        return self.__ref

    __pre_qc = None

    @property
    def pre_qc(self):
        if self.__pre_qc is None:
            self.__pre_qc = np.array(list(map(lambda s: s.pre_qc, self.surveys)))
        return self.__pre_qc

    __mag_qc = None

    @property
    def mag_qc(self):
        if self.__mag_qc is None:
            self.__mag_qc = np.array([
                not ((s.md < self.casing_depth + CASING_OFFSET) or
                     self.exti_interval.start < s.md < self.exti_interval.stop)
                for s in self.surveys])
        return self.__mag_qc

    __time = None

    @property
    def time(self):
        if self.__time is None:
            self.__time = np.array(list(map(lambda s: s.md, self.surveys)))  # TODO: FAX: add time to Survey class
        return self.__time

    __survey_status = None

    @property
    def survey_status(self):
        if self.__survey_status is None:
            self.__survey_status = np.array(list(map(lambda s: s.qc, self.correction.surveys)))
        return self.__survey_status

    __axis_status = None

    @property
    def axis_status(self):
        if self.__axis_status is None:
            self.__axis_status = np.array(list(map(lambda s: s.fa, self.correction.surveys)))
        return self.__axis_status

    @property
    def dni_cor(self):
        return self.correction.dni_cs.toarray()

    @property
    def ref_cor(self):
        return self.correction.ref_cs.toarray()

    @property
    def faxis(self):
        return max(map(lambda s: s.fa, self.correction.surveys))

    @property
    def fax_cor(self):
        return np.array(list(self.correction.fax_cs.values()))

    @property
    def fax_ind(self):
        return np.array(list(self.correction.fax_cs.keys()))

    @property
    def fax_cs(self):
        return self.correction.fax_cs

    @property
    def correct_pattern(self):
        return def_pattern

    @property
    def apr_unc(self):
        return self.correction.apr_unc

    @property
    def ref_cov_mat(self):
        return np.array(self.correction.ref_cov)

    @property
    def apst_unc(self):
        return self.correction.apst_unc.toarray()
