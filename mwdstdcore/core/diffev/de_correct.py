from typing import List, Dict
import numpy as np
from numpy import ndarray
from mwdstdcore.core.common.vcorrect import vect_dni_cor, vect_ref_cor
from mwdstdcore.core.common.vdelta import set_delta_func
from mwdstdcore.errormods.gmagmod import hdgm, bggm
from mwdstdcore.core.analysis.covmat import covmat_run
from mwdstdcore.errormods.codes import def_pattern
from .difev import de
from .search_space import space_box


# msa for DSI correction for an optimization algorithm
def de_correct(dni_xyz: ndarray, ref: ndarray, survey_status: ndarray, apr_unc: Dict[str, float],
               pattern: List[str] = def_pattern, refmod: Dict[str, float] = hdgm, particle_num: int = 250):
    total_survey_num = dni_xyz.shape[0]
    if total_survey_num == 0 or ref.shape[0] != total_survey_num or survey_status.shape[0] != total_survey_num:
        raise Exception('Method de_correct(): incorrect dimensions of input arrays(dni_xyz, ref, survey_status)')

    [qfunc, box_func] = qfunc_setup(dni_xyz, ref, survey_status, pattern, apr_unc, refmod, particle_num)
    [min_pos, max_pos] = box_func()

    [dni_cor, qf] = de(qfunc, min_pos, max_pos, particle_num, boxed=True)

    return [dni_cor, qf]


# MLE quality(target) function for an optimization algorithm
def qfunc_setup(dni_xyz: ndarray, ref: ndarray, survey_status: ndarray, pattern: List[str], apr_unc: Dict[str, float],
                refmod: Dict[str, float], particle_num: int):
    # setup covariance matrix
    cov_mat = covmat_run(dni_xyz.shape[0], apr_unc, refmod)
    cov_size = cov_mat.shape[0]
    weights = np.zeros((cov_size, 1))
    weights[:, 0] = np.diag(cov_mat) ** -1

    # setup data set
    survey_num = dni_xyz.shape[0]
    multi_dni_xyz = dni_xyz * np.ones((particle_num, survey_num, 6))
    multi_ref = ref * np.ones((particle_num, survey_num, 3))
    qf = np.zeros((1, particle_num))
    # setup correction and delta functions
    ps_delta = set_delta_func(particle_num, survey_num, len(def_pattern) + 3)   # +3 is reference corrections

    def qfunc(cor_sets: np.ndarray):
        multi_dni_xyz_cor = vect_dni_cor(multi_dni_xyz, cor_sets[:-3, :])
        multi_ref_cor = vect_ref_cor(multi_ref, cor_sets[-3:, :])
        dvector = ps_delta(multi_dni_xyz_cor, multi_ref_cor, cor_sets)

        # MLE criteria: (X - Xa)' * Capr^-1 * (X - Xa)
        qf[0, :] = np.sum(weights * dvector ** 2, 0)
        return qf

    # borders of MLE: setup the pso optimized vector
    def pso_box():
        # DE correction converting to DnI correction vector
        convect = np.zeros((18, 1))
        i = 0
        for mnemonic in def_pattern:
            convect[i, 0] = space_box[mnemonic]
            i += 1
        convect[-3, 0] = 6 * bggm['MGI']
        convect[-2, 0] = 6 * bggm['MBI']
        convect[-1, 0] = 6 * bggm['MDI']
        min_pos = -1 * convect
        max_pos = 1 * convect
        return [min_pos, max_pos]

    return [qfunc, pso_box]
