import numpy as np
from debug.models.testdni import test_dni
from debug.models.testraj import test_traj
from mwdstdcore.msa.correct import correct
from mwdstdcore.msa.covan import covan
from mwdstdcore.msa.qc import qc
from mwdstdcore.core.common.srvmath import dni_correct
from mwdstdcore.errormods.gmagmod import bggm


def correct_test():
    trial(1)
    trial(2)


def trial(traj_num: int):
    dni_model = test_dni(mode='dsi')
    [run, _, _, _] = test_traj(traj_num, dni_model, mag_noise=0., acc_noise=0.)
    run.dni_rigid = False
    apr_unc = covan(run.dni_xyz)
    res = correct(run.dni_xyz, run.ref, run.survey_status, refmod=bggm, apr_unc=apr_unc)
    dni_cor = res[0]
    ref_cor = res[1]
    dni_xyz_cor = dni_correct(run.dni_xyz, dni_cor)
    [_, gbd_norm] = qc(dni_xyz_cor, run.ref, ref_cor,)
    srv_quality = quality(gbd_norm)
    if srv_quality:
        status = 'passed'
    else:
        status = 'failed'
    print(f'quality check test for traj#{traj_num}: {status}')


def quality(gbd_norm):
    mask = (gbd_norm < 2.)
    srv_quality = np.prod(np.logical_and(np.logical_and(mask[:, 0], mask[:, 1]), mask[:, 2]), 0)
    return srv_quality


correct_test()
