import numpy as np
from mwdstdcore.datamodel.correction import set2cor
from mwdstdcore.datamodel import Run
from mwdstdcore.errormods.gmagmod import gmagmod
from mwdstdcore.errormods.codes import srv_stat_inv
from mwdstdcore.core.common.srvmath import dni_correct
from mwdstdcore.msa.covan import covan
from mwdstdcore.msa.correct import correct
from mwdstdcore.msa.qc import qc
from mwdstdcore.msa.apstan import run_apst
from mwdstdcore.auto.valid import validation


CASING_OFFSET = 20.  # m


# REST wrapper for autocor
def autocor(run: Run, refmod_name: str = 'bggm'):
    if len(run.surveys) == 0:
        return None
    [apr_unc, dni_xyz_cor, dni_cor, ref_cor, apst_vect, ref_cov_mat, inc_st, inc_unc, az_st, az_unc, gbd_boundaries,
     survey_status, axis_status, validity] = autocore(run, refmod_name)

    return set2cor(apr_unc, dni_xyz_cor, dni_cor, ref_cor, apst_vect, ref_cov_mat, inc_st, inc_unc, az_st, az_unc,
                   gbd_boundaries, survey_status, axis_status, validity, run)


# automatic analysis of survey set for different issues
def autocore(run: Run, refmod_name: str):
    ref_mod = gmagmod[refmod_name.upper()]
    survey_status = np.zeros(run.dni_xyz.shape[0])

    # filtering stage
    # MSA setup
    apr_unc = covan(run.dni_xyz)

    # sole run correction
    [dni_cor, ref_cor, apst_cov_mat] = correct(run.dni_xyz, run.ref, survey_status, ref_mod, apr_unc)
    apst_vect = np.sqrt(np.diag(apst_cov_mat[:-3, :-3]))
    ref_cov_mat = apst_cov_mat[-3:, -3:]
    dni_xyz_cor = dni_correct(run.dni_xyz, dni_cor)

    # qc filtering
    [gbd_boundaries, gbd_norm] = qc(dni_xyz_cor, run.ref, ref_cor=ref_cor, ref_mod=ref_mod)
    survey_status = remap(run.md, gbd_norm, run.casing_depth, run.exti_interval)

    [inc_stat, inc_unc, az_stat, az_unc] = run_apst(dni_xyz_cor, apr_unc, 'mwdstd_dni', ref_mod)

    validity = validation(run.pre_qc, run.mag_qc, apr_unc, dni_cor, ref_cor, ref_mod, survey_status, inc_stat, az_stat)

    return [apr_unc, dni_xyz_cor, dni_cor, ref_cor, apst_vect, ref_cov_mat, inc_stat, inc_unc,
            az_stat, az_unc, gbd_boundaries, survey_status, -np.ones_like(survey_status), validity]


def remap(md: np.ndarray, gbd_norm: np.ndarray, casing_depth=-100., exti_int=(-100., -100.), num_of_sigma=2.):
    num = gbd_norm.shape[0]
    dg = np.abs(gbd_norm[:, 0])
    db = np.abs(gbd_norm[:, 1])
    dd = np.abs(gbd_norm[:, 2])
    survey_status = np.zeros_like(dg)
    i = 0
    while i < num:
        if dg[i] > num_of_sigma:
            survey_status[i] = srv_stat_inv['BAD']
        else:
            if (db[i] <= num_of_sigma and dd[i] <= num_of_sigma and md[i] >= casing_depth + CASING_OFFSET and
                    not (exti_int[0] <= md[i] <= exti_int[1])):
                survey_status[i] = srv_stat_inv['STD']
            else:
                survey_status[i] = srv_stat_inv['INC']
        i += 1

    return survey_status
