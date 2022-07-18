import numpy as np
from mwdstdcore.errormods.gmagmod import bggm
from mwdstdcore.errormods.codes import def_pattern
from mwdstdcore.errormods.dnistd import dni_std
from mwdstdcore.errormods.dnimsa import dni_msa
from mwdstdcore.core.analysis.jacobian import jcbn4run


# quality check of the surveys
def qc(dni_xyz, ref, ref_cor=np.zeros(0), dni_mod='dni_std', ref_mod=bggm, num_of_sigma=2., jcbn=np.zeros(0)):
    if dni_mod == 'dni_msa':
        dni_mod = dni_msa
    else:
        dni_mod = dni_std
    srv_num = dni_xyz.shape[0]
    survey_status = np.zeros(srv_num)
    axis_status = -np.ones(srv_num)
    correct_pattern = def_pattern
    # setup covariance matrix
    num = len(correct_pattern)
    covmat_apr = np.zeros((num, num))
    i = 0
    for e in correct_pattern:
        covmat_apr[i, i] = dni_mod[e] ** 2
        i += 1
    if jcbn.shape[0] == 0:
        jcbn = jcbn4run(dni_xyz, bayes=False, ref=False)
    covmat_gbd_dni = jcbn @ covmat_apr @ jcbn.T
    srv_num = int(covmat_gbd_dni.shape[0] / 3)

    covmat_gbd_noise = np.zeros_like(covmat_gbd_dni)
    covmat_gbd_noise[:srv_num, :srv_num] = ref_mod['GRE'] ** 2 * np.eye(srv_num)
    covmat_gbd_noise[srv_num:2*srv_num, srv_num:2*srv_num] = ref_mod['BRE'] ** 2 * np.eye(srv_num)
    covmat_gbd_noise[2*srv_num:3*srv_num, 2*srv_num:3*srv_num] = ref_mod['DRE'] ** 2 * np.eye(srv_num)

    covmat_gbd_ref = np.zeros_like(covmat_gbd_dni)
    covmat_gbd_ref[:srv_num, :srv_num] = ref_mod['MGI'] ** 2 * np.ones((srv_num, srv_num))
    covmat_gbd_ref[srv_num:2 * srv_num, srv_num:2 * srv_num] = ref_mod['MBI'] ** 2 * np.ones((srv_num, srv_num))
    covmat_gbd_ref[2 * srv_num:3 * srv_num, 2 * srv_num:3 * srv_num] = ref_mod['MDI'] ** 2 * np.ones((srv_num, srv_num))

    # 0:1 Total G boundaries
    # 2:3 Total B boundaries
    # 4:5 Dip boundaries
    gbd_boundaries = np.zeros((srv_num, 6))
    if ref_cor.shape[0] == 3:
        covmat_gbd = covmat_gbd_dni + covmat_gbd_noise
        boundaries_vect = np.sqrt(np.diag(covmat_gbd))
        g_cor = ref_cor[0]
        b_cor = ref_cor[1]
        d_cor = ref_cor[2]
        gbd_boundaries[:, 0] = num_of_sigma * boundaries_vect[0:srv_num] - g_cor
        gbd_boundaries[:, 1] = -num_of_sigma * boundaries_vect[0:srv_num] - g_cor
        gbd_boundaries[:, 2] = num_of_sigma * boundaries_vect[srv_num:2 * srv_num] - b_cor
        gbd_boundaries[:, 3] = -num_of_sigma * boundaries_vect[srv_num:2 * srv_num] - b_cor
        gbd_boundaries[:, 4] = num_of_sigma * boundaries_vect[2 * srv_num:3 * srv_num] - d_cor
        gbd_boundaries[:, 5] = -num_of_sigma * boundaries_vect[2 * srv_num:3 * srv_num] - d_cor
    else:
        covmat_gbd = covmat_gbd_dni + covmat_gbd_noise + covmat_gbd_ref
        boundaries_vect = np.sqrt(np.diag(covmat_gbd))
        gbd_boundaries[:, 0] = num_of_sigma * boundaries_vect[0:srv_num]
        gbd_boundaries[:, 1] = -num_of_sigma * boundaries_vect[0:srv_num]
        gbd_boundaries[:, 2] = num_of_sigma * boundaries_vect[srv_num:2 * srv_num]
        gbd_boundaries[:, 3] = -num_of_sigma * boundaries_vect[srv_num:2 * srv_num]
        gbd_boundaries[:, 4] = num_of_sigma * boundaries_vect[2 * srv_num:3 * srv_num]
        gbd_boundaries[:, 5] = -num_of_sigma * boundaries_vect[2 * srv_num:3 * srv_num]
        g_cor = 0.
        b_cor = 0.
        d_cor = 0.

    g = np.sqrt(dni_xyz[:, 0] ** 2 + dni_xyz[:, 1] ** 2 + dni_xyz[:, 2] ** 2)
    b = np.sqrt(dni_xyz[:, 3] ** 2 + dni_xyz[:, 4] ** 2 + dni_xyz[:, 5] ** 2)
    d = np.arcsin((dni_xyz[:, 0] * dni_xyz[:, 3] + dni_xyz[:, 1] * dni_xyz[:, 4] + dni_xyz[:, 2] * dni_xyz[:, 5])
                  / g / b)
    dg = ((g - (ref[:, 0] - g_cor)) / boundaries_vect[0:srv_num]).reshape((srv_num, 1))
    db = ((b - (ref[:, 1] - b_cor)) / boundaries_vect[srv_num:2 * srv_num]).reshape((srv_num, 1))
    dd = ((d - (ref[:, 2] - d_cor)) / boundaries_vect[2 * srv_num:3 * srv_num]).reshape((srv_num, 1))
    gbd_norm = np.block([dg, db, dd])
    return gbd_boundaries, gbd_norm
