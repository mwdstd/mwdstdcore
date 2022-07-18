from typing import List, Dict
from math import pi
import numpy as np
from numpy import ndarray
from numpy.linalg import inv
from mwdstdcore.core.analysis.jacobian import jcbn4run
from mwdstdcore.core.analysis.covmat import covmat_run
from mwdstdcore.core.analysis.emanalysis import em_analysis
from mwdstdcore.core.wfunc import wfunc
from mwdstdcore.errormods.codes import faxis, def_pattern
from mwdstdcore.core.common.srvmath import iat, gbd


def run_apst(dni_xyz: ndarray, apr_unc: Dict[str, float], dni_err_mod: str, ref_mod: Dict[str, float],
             sigma_inc: float=0., sigma_az: float=0.):
    num = dni_xyz.shape[0]
    if num == 0:
        raise NameError('method apstan: No corrected surveys')

    # reference errors
    [inc_err_ref, az_err_ref] = srv_ref_err(dni_xyz, dni_err_mod, sigma_inc, sigma_az)

    # actual errors calculation
    apst_cov_mat = covmat_apst(dni_xyz, apr_unc, ref_mod)

    [_, jcbn_inc, jcbn_az] = jdia(dni_xyz, -np.ones(num), def_pattern)
    cov_mat_inc = jcbn_inc @ apst_cov_mat[:-3, :-3] @ jcbn_inc.T
    cov_mat_az = jcbn_az @ apst_cov_mat[:-3, :-3] @ jcbn_az.T

    az_err_apost = np.sqrt(np.diag(cov_mat_az))
    az_err_apost = (az_err_apost <= pi) * az_err_apost + (az_err_apost > pi) * pi

    inc_err_apost = np.sqrt(np.diag(cov_mat_inc))
    inc_err_apost = (inc_err_apost <= pi) * inc_err_apost + (inc_err_apost > pi) * pi

    inc_err_status = (inc_err_apost <= inc_err_ref)
    az_err_status = (az_err_apost <= az_err_ref)
    inc_unc = np.zeros((num, 2))
    az_unc = np.zeros((num, 2))
    inc_unc[:, 0] = inc_err_apost
    inc_unc[:, 1] = inc_err_ref
    az_unc[:, 0] = az_err_apost
    az_unc[:, 1] = az_err_ref
    return [inc_err_status, inc_unc, az_err_status, az_unc]


# calculate a posteriori covariance matrix for sole run
def covmat_apst(dni_xyz: ndarray, apr_unc: Dict[str, float], refmod: Dict[str, float]):
    srv_num = dni_xyz.shape[0]
    jcbn_msa = jcbn4run(dni_xyz)
    covmat_apriori = covmat_run(srv_num, apr_unc, refmod)
    apst_cov_mat = inv(jcbn_msa.T @ inv(covmat_apriori) @ jcbn_msa)
    return apst_cov_mat


# jacobians for depth, inclination and azimuth
def jdia(dni_xyz: ndarray, axis_status: ndarray, correct_pattern: List[str]):
    [inc, az_m, tf] = iat(dni_xyz)
    [g, b, d] = gbd(dni_xyz)

    fail_indexes = np.argwhere(axis_status != -1)[:, 0]
    failed_survey_num = fail_indexes.shape[0]
    if failed_survey_num == 0:
        fail_axis_code = 'none'
    else:
        fail_axis_code = faxis[axis_status[fail_indexes[0]]]

    basic_pattern = correct_pattern
    basic_error_num = len(basic_pattern)
    total_error_num = basic_error_num + failed_survey_num
    survey_num = dni_xyz.shape[0]
    full_pattern = correct_pattern + failed_survey_num * [fail_axis_code]
    jcbn_md = np.zeros((survey_num, total_error_num))
    jcbn_inc = np.zeros((survey_num, total_error_num))
    jcbn_az = np.zeros((survey_num, total_error_num))
    i = 0
    fail_survey_index = 0
    while i < survey_num:
        j = 0
        fax_stat = axis_status[i]
        fail_axis = faxis[fax_stat]
        for error_code in full_pattern:
            if fax_stat != -1:
                if j >= basic_error_num and j - basic_error_num < fail_survey_index:
                    j += 1
                    continue
                elif j >= basic_error_num and j - basic_error_num > fail_survey_index:
                    fail_survey_index += 1
                    break
            else:
                if j >= basic_error_num:
                    break
            dpdr = wfunc(error_code, inc=inc[i], az=az_m[i], tf=tf[i], g=g[i], b=b[i], d=d[i])
            if fail_axis == 'AFX':
                if error_code == 'ABX' or error_code == 'ASX':
                    dpdr *= 0.
            elif fail_axis == 'AFY':
                if error_code == 'ABY' or error_code == 'ASY':
                    dpdr *= 0.
            elif fail_axis == 'AFZ':
                if error_code == 'ABZ' or error_code == 'ASZ':
                    dpdr *= 0.
            elif fail_axis == 'MFX':
                if error_code == 'MBX' or error_code == 'MSX':
                    dpdr *= 0.
            elif fail_axis == 'MFY':
                if error_code == 'MBY' or error_code == 'MSY':
                    dpdr *= 0.
            elif fail_axis == 'MFY':
                if error_code == 'MBZ' or error_code == 'MSZ':
                    dpdr *= 0.
            jcbn_md[i, j] = dpdr[0]
            jcbn_inc[i, j] = dpdr[1]
            jcbn_az[i, j] = dpdr[2]
            j += 1
        i += 1

    return [jcbn_md, jcbn_inc, jcbn_az]


# survey model reference error calculation
def srv_ref_err(dni_xyz: ndarray, dni_err_mod: str, err_inc_thrd: float, err_az_thrd: float):
    [inc, az_m, tf] = iat(dni_xyz)
    [g, b, d] = gbd(dni_xyz)
    [cov_mat_inc, cov_mat_az] = em_analysis(inc, az_m, tf, g, b, d, dni_err_mod, sigma_inc=err_inc_thrd,
                                            sigma_az=err_az_thrd)

    az_err_ref = np.sqrt(np.diag(cov_mat_az))
    az_err_ref = (az_err_ref <= pi) * az_err_ref + (az_err_ref > pi) * pi
    inc_err_ref = np.sqrt(np.diag(cov_mat_inc))
    inc_err_ref = (inc_err_ref <= pi) * inc_err_ref + (inc_err_ref > pi) * pi
    return [inc_err_ref, az_err_ref]
