import numpy as np
from debug.models.testdni import test_dni
from debug.models.testraj import test_traj
from debug.models.dnimodel import DnIModel
from mwdstdcore.msa.correct import correct
from mwdstdcore.msa.covan import covan
from mwdstdcore.errormods.dnistd import dni_std
from mwdstdcore.errormods.gmagmod import bggm


def correct_test():
    trial(1)
    trial(2)


def trial(traj_num: int):
    dni_model = test_dni(mode='dsi')
    dni_cor = model2vector(dni_model)
    mask = np.zeros_like(dni_cor)
    unc = np.zeros_like(dni_cor)
    i = 0
    for e in dni_std:
        unc[i] = dni_std[e]
        if abs(dni_cor[i]) > 2 * dni_std[e]:
            mask[i] = 1.
        i += 1
    run, _, _, _ = test_traj(traj_num, dni_model, mag_noise=0., acc_noise=0.)
    apr_unc = covan(run.dni_xyz)
    dsi_cor, _, _ = correct(run.dni_xyz, run.ref, run.survey_status, refmod=bggm, apr_unc=apr_unc)
    delta = mask * (dni_cor - dsi_cor) / unc
    if np.prod(np.abs(delta) < 3):
        status = 'passed'
    else:
        status = 'failed'
    print(f'correction test for traj#{traj_num}: {status}')


def model2vector(dni_model: DnIModel) -> np.ndarray:
    dni_cor = np.zeros(15)
    dni_cor[:3] = dni_model.AB
    dni_cor[3:6] = np.diag(dni_model.AS, 0)
    dni_cor[6:9] = dni_model.MB
    dni_cor[9:12] = np.diag(dni_model.MS, 0)
    dni_cor[12] = dni_model.MI[0, 1]
    dni_cor[13] = dni_model.MI[0, 2]
    dni_cor[14] = dni_model.MI[1, 2]
    return dni_cor


correct_test()
