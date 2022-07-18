import numpy as np
from mwdstdcore.errormods.unknown import unknown
from mwdstdcore.errormods.dnistd import dni_std
from .dnimodel import DnIModel


# create test dni errors
def test_dni(mode='rnd', faxis='none'):
    if mode == 'zero':
        dni_mod = DnIModel()
    elif mode == 'rnd':
        [AS, AB, MS, MB, MXY, MXZ, MYZ] = gen_err(unknown)
        dni_mod = DnIModel(AS, AB, MS, MB, MXY, MXZ, MYZ, 'none')
    elif mode == 'rnd_std':
        [AS, AB, MS, MB, MXY, MXZ, MYZ] = gen_err(dni_std)
        dni_mod = DnIModel(AS, AB, MS, MB, MXY, MXZ, MYZ, 'none')
    elif mode == 'fax':
        [AS, AB, MS, MB, MXY, MXZ, MYZ] = gen_err(dni_std)
        # MB = np.array([3000., -1000., 3000.])
        # MB = np.array([0., 0., 0.])
        dni_mod = DnIModel(AS, AB, MS, MB, MXY, MXZ, MYZ, faxis)
    elif mode == 'dsi':
        AS = np.array([500., -500., 500.]) * 10. ** -6
        AB = np.array([.5, -.5, 0.]) * 10. ** -2
        MS = np.array([1600., -2000., -2200.]) * 10. ** -6
        MB = np.array([-300., 300., 700.])
        MXY = 0.
        MXZ = 0.
        MYZ = 0.
        dni_mod = DnIModel(AS, AB, MS, MB, MXY, MXZ, MYZ, 'none')
    elif mode == 'one':
        AS = np.array([0., 0., 0.])
        AB = np.array([0., 0., 0.])
        MS = np.array([0., 0., 0.])
        MB = np.array([0., 0., 0.])
        MXY = 0.
        MXZ = 0.01
        MYZ = 0.
        dni_mod = DnIModel(AS, AB, MS, MB, MXY, MXZ, MYZ, 'none')
    else:
        AS = np.array([500., 500., 500.]) * 10.**-6
        AB = np.array([1., .5, 0.]) * 10.**-1
        MS = np.array([5., -5., 0.]) * 10.**-2
        MB = np.array([-3000., 3000., 7000.])
        MXY = 0.0001
        MXZ = 0.01
        MYZ = 0.0001
        dni_mod = DnIModel(AS, AB, MS, MB, MXY, MXZ, MYZ, 'none')
    return dni_mod


def gen_err(errmod):
    AS = np.array([errmod['ASX'], errmod['ASY'], errmod['ASZ']]) * np.random.randn(3)
    AB = np.array([errmod['ABX'], errmod['ABY'], errmod['ABZ']]) * np.random.randn(3)
    MS = np.array([errmod['MSX'], errmod['MSY'], errmod['MSZ']]) * np.random.randn(3)
    MB = np.array([errmod['MBX'], errmod['MBY'], errmod['MBZ']]) * np.random.randn(3)
    MXY = errmod['MXY'] * np.random.randn(1)[0]
    MXZ = errmod['MXZ'] * np.random.randn(1)[0]
    MYZ = errmod['MYZ'] * np.random.randn(1)[0]
    return [AS, AB, MS, MB, MXY, MXZ, MYZ]
