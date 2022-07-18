import numpy as np
from numpy import ndarray
from mwdstdcore.errormods.dnistd import dni_std
from mwdstdcore.errormods.unknown import unknown
from mwdstdcore.core.common.srvmath import iat


# simplified MSA setup of full analysis of apriori covariance matrix for performance maximization
def covan(dni_xyz: ndarray):

    apriori_unc = dni_std.copy()
    apriori_unc['MBZ'] = unknown['MBZ']

    _, _, tf = iat(dni_xyz)
    if tf.shape[0] > 1:
        tf_sorted = np.sort(tf)
        dtf = np.zeros_like(tf)
        dtf[1:] = np.abs(tf_sorted[1:] - tf_sorted[:-1])
        dtf[0] = 2 * np.pi - (tf_sorted[-1] - tf_sorted[0])
        if np.max(dtf) <= 100 * np.pi / 180:
            apriori_unc['MBX'] = unknown['MBX']
            apriori_unc['MBY'] = unknown['MBY']

    return apriori_unc
