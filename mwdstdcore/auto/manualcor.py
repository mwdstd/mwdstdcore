import numpy as np
from mwdstdcore.datamodel.cor_survey import ManualCorrectedSurvey
from mwdstdcore.datamodel.ref import get_default_boundaries
import mwdstdcore.datamodel as rs
from mwdstdcore.datamodel.calc.station import calc_station, calc_corrected_station, calc_gbd
from mwdstdcore.core.common.srvmath import dni_correct


def manualcor(run: rs.Run) -> rs.correction.ManualCorrection:
    stations = [calc_station(s, r.dec, r.grid) for s, r in zip(run.surveys, run.reference)]
    mds = [s.md for s in run.surveys]
    dni_xyz = np.array([[s.gx, s.gy, s.gz, s.bx, s.by, s.bz] for s in run.surveys])
    dni_xyz_cor = dni_correct(dni_xyz, run.correction.dni_cs.toarray())
    cor_surveys = ManualCorrectedSurvey.listFromArrays(mds, dni_xyz_cor)
    cor_stations = [calc_corrected_station(s, st, r.dec, r.grid) for s, st, r in
                    zip(cor_surveys, stations, run.reference)]

    bnd = get_default_boundaries()

    for su, r in zip(cor_surveys, run.reference):
        gbd = calc_gbd(su)
        su.min = rs.qc_bond.QcBoundary(g=r.g - bnd.g, b=r.b - bnd.b, dip=r.dip - bnd.dip)
        su.max = rs.qc_bond.QcBoundary(g=r.g + bnd.g, b=r.b + bnd.b, dip=r.dip + bnd.dip)
        su.qc_pass = rs.qc_bond.Qc.fromValBnd(gbd, su.min, su.max)
        su.qc = 0 if su.qc_pass.g and su.qc_pass.b and su.qc_pass.dip else 2

    srv_qc = [s.qc == 0 for s, su in zip(cor_surveys, run.surveys) if su.pre_qc]

    try:
        pre_qc_ratio = sum(srv_qc) / len(srv_qc)
    except ZeroDivisionError:
        pre_qc_ratio = 0.

    qa = rs.qa.QualityAssessment()
    qa.expectation.value = pre_qc_ratio >= .8
    qa.accuracy.value = None
    qa.reference.value = None
    qa.correction_possibility.value = None
    qa.model_comparison.value = None
    qa.number_of_surveys.value = None

    if len(srv_qc) >= 5:
        qa.sq_last.value = sum(srv_qc[-5:]) >= 3
        qa.sq_last.severity = 1 if sum(srv_qc[-5:]) == 0 else 0

    return rs.correction.ManualCorrection(
        dni_cs=run.correction.dni_cs,
        qa=qa,
        surveys=cor_surveys,
        stations=cor_stations
    )
