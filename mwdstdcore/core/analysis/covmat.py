from typing import Dict
import numpy as np
from numpy import ndarray
from mwdstdcore.errormods.gmagmod import bggm
from mwdstdcore.errormods.codes import def_pattern


def covmat_run(srv_num: int, errmod: Dict[str, float], refmod: Dict[str, float] = bggm) -> ndarray:
    n = srv_num
    m = len(def_pattern)
    ref_num = 3

    cov_mat = np.zeros((3*n + m + ref_num, 3*n + m + ref_num))
    i = 0
    for j in range(0, n):
        cov_mat[i, i] = refmod['GRE'] ** 2
        cov_mat[n + i, n + i] = refmod['BRE'] ** 2
        cov_mat[2 * n + i, 2 * n + i] = refmod['DRE'] ** 2
        i += 1

    i = 0
    while i < m:
        cov_mat[3 * n + i, 3 * n + i] = errmod[def_pattern[i]] ** 2
        i += 1

    cov_mat[-3, -3] = refmod['MGI'] ** 2
    cov_mat[-2, -2] = refmod['MBI'] ** 2
    cov_mat[-1, -1] = refmod['MDI'] ** 2
    return cov_mat
