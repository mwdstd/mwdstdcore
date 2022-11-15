from typing import List
import numpy as np
import pytest
from mwdstdcore.errormods.dnistd import dni_std
from mwdstdcore.errormods.gmagmod import bggm
from mwdstdcore.datamodel import TfStation
from mwdstdcore.auto.autocor import autocore
from mwdstdcore.msa.covan import covan
from mwdstdcore.msa.correct import correct, dni_correct
from mwdstdcore.msa.qc import qc
from tests.params import traj1, traj2, ref1, dni_err_dsi, noise_zero, noise_default_acc, noise_default_mag
from tests.simulation import simulate_run


@pytest.mark.parametrize('base_traj', [traj1, traj2])
def test_correct(base_traj: List[TfStation]):
    dni_cor = dni_err_dsi.toarray()
    mask = np.zeros_like(dni_cor)
    unc = np.zeros_like(dni_cor)
    for (i, e) in enumerate(dni_std):
        unc[i] = dni_std[e]
        if abs(dni_cor[i]) > 2 * dni_std[e]:
            mask[i] = 1.

    run = simulate_run(base_traj, ref1, dni_err_dsi, noise_zero, noise_zero)
    apr_unc = covan(run.dni_xyz)
    dsi_cor, _, _ = correct(run.dni_xyz, run.ref, np.zeros(run.dni_xyz.shape[0]), refmod=bggm, apr_unc=apr_unc)
    delta = mask * (dni_cor - dsi_cor) / unc
    assert np.prod(np.abs(delta) < 3)

@pytest.mark.parametrize('base_traj', [traj1, traj2])
def test_qc(base_traj: List[TfStation]):
    run = simulate_run(base_traj, ref1, dni_err_dsi, noise_zero, noise_zero)
    run.dni_rigid = False
    apr_unc = covan(run.dni_xyz)
    dni_cor, ref_cor, _ = correct(run.dni_xyz, run.ref, np.zeros(run.dni_xyz.shape[0]), refmod=bggm, apr_unc=apr_unc)
    dni_xyz_cor = dni_correct(run.dni_xyz, dni_cor)
    _, gbd_norm = qc(dni_xyz_cor, run.ref, ref_cor,)
    mask = (gbd_norm < 2.)
    srv_quality = np.prod(np.logical_and(np.logical_and(mask[:, 0], mask[:, 1]), mask[:, 2]), 0)
    assert srv_quality

@pytest.mark.parametrize('base_traj', [traj1, traj2])
def test_autocor(base_traj: List[TfStation]):
    dni_cor = dni_err_dsi.toarray()
    mask = np.zeros_like(dni_cor)
    unc = np.zeros_like(dni_cor)
    for (i, e) in enumerate(dni_std):
        unc[i] = dni_std[e]
        if abs(dni_cor[i]) > 2 * dni_std[e]:
            mask[i] = 1.

    run = simulate_run(base_traj, ref1, dni_err_dsi, noise_default_acc, noise_default_mag)
    _, _, dsi_cor, _, _, _, _, _, _, _, _, _, _ = autocore(run, refmod_name='bggm')

    delta = mask * (dni_cor - dsi_cor) / unc
    assert np.prod(np.abs(delta) < 3)