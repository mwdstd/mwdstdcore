from typing import Dict, List, Union
import numpy as np
from numpy import ndarray
from mwdstdcore.errormods.posunc.mwdstd import mwdstd0, mwdstd_dni, mwdstd4
from mwdstdcore.core.wfunc import wfunc


def em_analysis(inc: ndarray, az_m: ndarray, tf: ndarray, g: ndarray, b: ndarray, d: ndarray, em: str, sigma_inc=0.,
                sigma_az=0.):
    # sigma_inc and sigma_az are ground uncertainty levels, zone of unc insensitivity
    if em == 'mwdstd0':
        errmod = mwdstd0
    elif em == 'mwdstd_dni':
        errmod = mwdstd_dni
    elif em == 'mwdstd4':
        errmod = mwdstd4
    else:
        errmod = mwdstd_dni

    cov_mat = cov_mat_dia(errmod)
    err_terms = list(map(lambda e: e, errmod))
    [_, jcbn_inc, jcbn_az] = jdia(inc, az_m, tf, g, b, d, err_terms)
    identity_mat = np.eye(inc.shape[0])
    cov_mat_inc = jcbn_inc @ cov_mat @ jcbn_inc.T + sigma_inc ** 2 * identity_mat
    cov_mat_az = jcbn_az @ cov_mat @ jcbn_az.T + sigma_az ** 2 * identity_mat

    return [cov_mat_inc, cov_mat_az]


# error calculation for existing covariance matrix
def covmat_analysis(inc: ndarray, az_m: ndarray, tf: ndarray, g: ndarray, b: ndarray, d: ndarray, cov_mat: np.ndarray,
                    err_terms: List[str]):
    [_, jcbn_inc, jcbn_az] = jdia(inc, az_m, tf, g, b, d, err_terms)
    cov_mat_inc = jcbn_inc @ cov_mat @ jcbn_inc.T
    cov_mat_az = jcbn_az @ cov_mat @ jcbn_az.T
    return [cov_mat_inc, cov_mat_az]


# jacobians for depth, inclination and azimuth
def jdia(inc: ndarray, az_m: ndarray, tf: ndarray, g: ndarray, b: ndarray, d: ndarray, err_terms: List[str]):
    survey_num = inc.shape[0]
    mnem_num = len(err_terms)
    jcbn_md = np.zeros((survey_num, mnem_num))
    jcbn_inc = np.zeros((survey_num, mnem_num))
    jcbn_az = np.zeros((survey_num, mnem_num))
    i = 0
    while i < survey_num:
        j = 0
        for e in err_terms:
            dpdr = wfunc(e, inc=inc[i], az=az_m[i], tf=tf[i], dec=0., grid=0., g=g[i], b=b[i], d=d[i])
            jcbn_md[i, j] = dpdr[0]
            jcbn_inc[i, j] = dpdr[1]
            jcbn_az[i, j] = dpdr[2]
            j += 1
        i += 1

    return [jcbn_md, jcbn_inc, jcbn_az]


# covariance matrix for depth, inclination and azimuth
def cov_mat_dia(errmod: Dict[str, Dict[str, Union[str, float]]]):
    mnem_num = len(errmod)
    cov_mat = np.zeros((mnem_num, mnem_num))
    i = 0
    for e in errmod:
        cov_mat[i, i] = errmod[e]['value'] ** 2
        i += 1

    return cov_mat
