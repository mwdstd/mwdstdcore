import numpy as np
from debug.models.testdni import test_dni
from debug.models.testraj import test_traj
from debug.models.dnimodel import DnIModel
from mwdstdcore.datamodel.survey import Survey
from mwdstdcore.datamodel.ref import Reference
from mwdstdcore.datamodel.run import Run
from debug.models.run import Run as _Run
from mwdstdcore.auto.autocor import autocore
from mwdstdcore.errormods.dnistd import dni_std


# convert the obsolete class Run to the actual one
def run2run(run: _Run) -> Run:
    srv_num = run.dni_xyz.shape[0]
    surveys = [Survey(md=run.md[i],
                      gx=run.dni_xyz[i, 0],
                      gy=run.dni_xyz[i, 1],
                      gz=run.dni_xyz[i, 2],
                      bx=run.dni_xyz[i, 3],
                      by=run.dni_xyz[i, 4],
                      bz=run.dni_xyz[i, 5]) for i in range(srv_num)]
    reference = [Reference(g=run.ref[i, 0], b=run.ref[i, 1], dip=run.ref[i, 2]) for i in range(srv_num)]
    run = Run(surveys=surveys, dni_rigid=run.dni_rigid, edi=0., reference=reference, casing_depth=run.casing_depth)
    return run


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

    [run, _, _, _] = test_traj(traj_num, dni_model, mag_noise=30., acc_noise=0.005)
    run = run2run(run)

    [_, _, dsi_cor, _, _, _, _, _, _, _, _, _, _, _] = autocore(run, refmod_name='bggm')

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
