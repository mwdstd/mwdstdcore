from typing import Tuple
import numpy as np
from numpy import ndarray
from mwdstdcore.core.diffev.de_correct import de_correct
from mwdstdcore.core.common.srvmath import dni_correct
from .apstan import covmat_apst


# ordinary MSA correction of DnI errors associated with the basic model
def correct(dni_xyz: ndarray, ref: ndarray, survey_status: ndarray, refmod, apr_unc) ->\
        Tuple[np.ndarray, np.ndarray, np.ndarray]:

    [dni_cor, _] = de_correct(dni_xyz, ref, survey_status, apr_unc, refmod=refmod)
    dsi_cor = dni_cor[:15].flatten()
    ref_cor = dni_cor[-3:].flatten()

    dni_xyz_cor = dni_correct(dni_xyz, dni_cor)
    apst_cov_mat = covmat_apst(dni_xyz_cor, apr_unc, refmod)
    return [dsi_cor, ref_cor, apst_cov_mat]
