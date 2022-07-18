from typing import Tuple
import numpy as np
from numpy import sqrt, sin, cos, arcsin, arctan2, pi, ndarray


def iat(dni_xyz: ndarray, dec: ndarray = np.zeros(0), grid: ndarray = np.zeros(0), sag: ndarray = np.zeros(0)) \
        -> Tuple[ndarray, ndarray, ndarray]:
    srv_num = dni_xyz.shape[0]
    if dec.shape[0] == 0:
        dec = np.zeros(srv_num)
    if grid.shape[0] == 0:
        grid = np.zeros(srv_num)
    if sag.shape[0] == 0:
        sag = np.zeros(srv_num)

    if dec.shape[0] != srv_num or grid.shape[0] != srv_num or sag.shape[0] != srv_num:
        raise Exception('Method iat(): wrong dimensions of input arrays: dni_xyz, dec, grid, sag')

    gx = dni_xyz[:, 2]
    gy = dni_xyz[:, 1]
    gz = dni_xyz[:, 0]
    bx = dni_xyz[:, 5]
    by = dni_xyz[:, 4]
    bz = dni_xyz[:, 3]

    [g, b, d] = gbd(dni_xyz)

    inc = arctan2(sqrt(gy ** 2 + gz ** 2), gx) - sag

    a1 = bx / b - gx / g * sin(d)
    a2 = (gy * bz - gz * by) / g / b
    az = arctan2(a2, a1) + (dec - grid)
    az = az + (az < 0.) * 2 * pi * np.ones(srv_num)
    az[inc == 0.] = 0.

    tf = arctan2(gz, -gy)
    return [inc, az, tf]


def iat2xyz(inc: ndarray, az: ndarray, tf: ndarray, g: ndarray, b: ndarray, d: ndarray, dec: ndarray, grid: ndarray):
    az_m = az - (dec - grid)
    xyz = np.zeros((inc.shape[0], 6))

    xyz[:, 0] = -g * sin(inc) * sin(tf)
    xyz[:, 1] = -g * sin(inc) * cos(tf)
    xyz[:, 2] = g * cos(inc)
    xyz[:, 3] = b * (cos(d) * (cos(inc) * cos(az_m) * sin(tf) + sin(az_m) * cos(tf)) - sin(d) * sin(inc) * sin(tf))
    xyz[:, 4] = b * (cos(d) * (cos(inc) * cos(az_m) * cos(tf) - sin(az_m) * sin(tf)) - sin(d) * sin(inc) * cos(tf))
    xyz[:, 5] = b * (cos(d) * sin(inc) * cos(az_m) + sin(d) * cos(inc))

    return xyz


def gbd(dni_xyz: ndarray) -> Tuple[ndarray, ndarray, ndarray]:
    g = sqrt(dni_xyz[:, 0] ** 2 + dni_xyz[:, 1] ** 2 + dni_xyz[:, 2] ** 2)
    b = sqrt(dni_xyz[:, 3] ** 2 + dni_xyz[:, 4] ** 2 + dni_xyz[:, 5] ** 2)
    d = arcsin((dni_xyz[:, 0] * dni_xyz[:, 3] + dni_xyz[:, 1] * dni_xyz[:, 4] + dni_xyz[:, 2] * dni_xyz[:, 5]) / g / b)
    return [g, b, d]


def dgbd(dni_xyz: ndarray, ref: ndarray) -> Tuple[ndarray, ndarray, ndarray]:
    [g, b, d] = gbd(dni_xyz)
    dg = ref[:, 0] - g
    db = ref[:, 1] - b
    dd = ref[:, 2] - d
    return [dg, db, dd]


def dni_correct(dni_xyz: ndarray, dni_cor: ndarray, faxis: int = -1, failed_axis: ndarray = np.zeros(0),
                failed_index: ndarray = np.zeros(0)) -> ndarray:
    dni_cor_ = dni_cor.copy()
    dni_xyz_ = dni_xyz.copy()

    # accels' correction for sf and biases
    abx = dni_cor_[0]
    aby = dni_cor_[1]
    abz = dni_cor_[2]
    asx = dni_cor_[3] + 1.
    asy = dni_cor_[4] + 1.
    asz = dni_cor_[5] + 1.

    dni_xyz_[:, 0] = dni_xyz_[:, 0] / asx - abx
    dni_xyz_[:, 1] = dni_xyz_[:, 1] / asy - aby
    dni_xyz_[:, 2] = dni_xyz_[:, 2] / asz - abz

    # mags' correction for sf and biases
    mbx = dni_cor_[6]
    mby = dni_cor_[7]
    mbz = dni_cor_[8]
    msx = dni_cor_[9] + 1.
    msy = dni_cor_[10] + 1.
    msz = dni_cor_[11] + 1.

    dni_xyz_[:, 3] = dni_xyz_[:, 3] / msx - mbx
    dni_xyz_[:, 4] = dni_xyz_[:, 4] / msy - mby
    dni_xyz_[:, 5] = dni_xyz_[:, 5] / msz - mbz

    # failed axis correction if applicable
    if faxis != -1:
        dni_xyz_[failed_index, faxis] = failed_axis
    dni_xyz_cor = dni_xyz_.copy()

    # misalignment correction
    mxy = dni_cor_[12]
    mxz = dni_cor_[13]
    myz = dni_cor_[14]
    dni_xyz_cor[:, 3] = dni_xyz_[:, 3] - mxy * dni_xyz_[:, 4] - mxz * dni_xyz_[:, 5]
    dni_xyz_cor[:, 4] = dni_xyz_[:, 4] + mxy * dni_xyz_[:, 3] - myz * dni_xyz_[:, 5]
    dni_xyz_cor[:, 5] = dni_xyz_[:, 5] + mxz * dni_xyz_[:, 3] + myz * dni_xyz_[:, 4]

    # re-write failed axis
    if faxis != -1:
        dni_xyz_cor[failed_index, faxis] = failed_axis
    return dni_xyz_cor
