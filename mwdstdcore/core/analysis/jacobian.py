import numpy as np
from numpy import ndarray, arcsin, sqrt, cos, sin
from mwdstdcore.errormods.codes import def_pattern


def jcbn4run(dni_xyz: ndarray, bayes=True, ref=True) -> ndarray:
    srv_num = dni_xyz.shape[0]
    term_num = len(def_pattern)
    bayes_num = term_num if bayes else 0
    ref_num = 3 if ref else 0

    jacob = np.zeros((3 * srv_num + bayes_num + ref_num, term_num + ref_num))
    jcbn_def = jcbn4def(dni_xyz)

    term_ind = list(map(lambda e: def_pattern.index(e), def_pattern))

    jacob[:3 * srv_num, :term_num] = jcbn_def[:, term_ind]

    if bayes:
        jacob[3 * srv_num:3 * srv_num + term_num, :term_num] = np.eye(term_num)

    if ref:
        jacob[-3:, -3:] = np.eye(3)
    return jacob


# analytical default Jacobian
def jcbn4def(dni_xyz: ndarray):
    srv_num = dni_xyz.shape[0]
    eterm_num = 15
    jcbn = np.zeros((3 * srv_num, eterm_num))

    gx = dni_xyz[:, 0]
    gy = dni_xyz[:, 1]
    gz = dni_xyz[:, 2]
    bx = dni_xyz[:, 3]
    by = dni_xyz[:, 4]
    bz = dni_xyz[:, 5]

    g = sqrt(gx ** 2 + gy ** 2 + gz ** 2)
    b = sqrt(bx ** 2 + by ** 2 + bz ** 2)
    d = arcsin((gx * bx + gy * by + gz * bz) / g / b)
    cos_d = cos(d)
    sin_d = sin(d)
    g_b_cos_d = g * b * cos_d
    g2_cos_d = g ** 2 * cos_d
    b2_cos_d = b ** 2 * cos_d
    # ABX
    jcbn[:srv_num, 0] = -gx / g
    jcbn[2 * srv_num:, 0] = -(bx / g_b_cos_d - gx * sin_d / g2_cos_d)
    # ABY
    jcbn[:srv_num, 1] = -gy / g
    jcbn[2 * srv_num:, 1] = -(by / g_b_cos_d - gy * sin_d / g2_cos_d)
    # ABZ
    jcbn[:srv_num, 2] = -gz / g
    jcbn[2 * srv_num:, 2] = -(bz / g_b_cos_d - gz * sin_d / g2_cos_d)
    # ASX
    jcbn[:srv_num, 3] = -gx ** 2 / g
    jcbn[2 * srv_num:, 3] = -(gx * bx / g_b_cos_d - gx ** 2 * sin_d / g2_cos_d)
    # ASY
    jcbn[:srv_num, 4] = -gy ** 2 / g
    jcbn[2 * srv_num:, 4] = -(gy * by / g_b_cos_d - gy ** 2 * sin_d / g2_cos_d)
    # ASZ
    jcbn[:srv_num, 5] = -gz ** 2 / g
    jcbn[2 * srv_num:, 5] = -(gz * bz / g_b_cos_d - gz ** 2 * sin_d / g2_cos_d)

    # MBX
    jcbn[srv_num:2 * srv_num, 6] = -bx / b
    jcbn[2 * srv_num:, 6] = -(gx / g_b_cos_d - bx * sin_d / b2_cos_d)
    # MBY
    jcbn[srv_num:2 * srv_num, 7] = -by / b
    jcbn[2 * srv_num:, 7] = -(gy / g_b_cos_d - by * sin_d / b2_cos_d)
    # MBZ
    jcbn[srv_num:2 * srv_num, 8] = -bz / b
    jcbn[2 * srv_num:, 8] = -(gz / g_b_cos_d - bz * sin_d / b2_cos_d)
    # MSX
    jcbn[srv_num:2 * srv_num, 9] = -bx ** 2 / b
    jcbn[2 * srv_num:, 9] = -(gx * bx / g_b_cos_d - bx ** 2 * sin_d / b2_cos_d)
    # MSY
    jcbn[srv_num:2 * srv_num, 10] = -by ** 2 / b
    jcbn[2 * srv_num:, 10] = -(gy * by / g_b_cos_d - by ** 2 * sin_d / b2_cos_d)
    # MSZ
    jcbn[srv_num:2 * srv_num, 11] = -bz ** 2 / b
    jcbn[2 * srv_num:, 11] = -(gz * bz / g_b_cos_d - bz ** 2 * sin_d / b2_cos_d)

    # MXY
    jcbn[2 * srv_num:, 12] = -(gx * by - gy * bx) / g_b_cos_d
    # MXZ
    jcbn[2 * srv_num:, 13] = -(gx * bz - gz * bx) / g_b_cos_d
    # MYZ
    jcbn[2 * srv_num:, 14] = -(gy * bz - gz * by) / g_b_cos_d

    return jcbn
