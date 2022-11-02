from typing import List
from math import cos, sin, atan, pi, sqrt
import attr
import numpy as np
from numpy import ndarray
from mwdstdcore.datamodel import BHA, Station
from .bha2input import bha2input
from .cdesc import coord_descent


@attr.s(auto_attribs=True)
class SagResult:
    sag: float
    grid: List[float]
    opt: List[float]
    low: List[float]
    top: List[float]
    mid: List[float]
    od: List[float]
    id: List[float]
    valid: bool


def sagcor(bha: BHA, md_bit: float, trajectory: List[Station], steer_gtf: float, mud_weight: float, 
           borehole_design: List[List[float]] = None) -> SagResult:
    traj = np.asarray([[st.md, st.inc] for st in trajectory])
    if borehole_design is not None:
        bh_design = np.asarray(borehole_design)
    else:
        bh_design = None

    inc_dni = trajinc(bha.dni_to_bit, md_bit, traj)
    if inc_dni < 10. * pi / 180:
        delta = [1.5]
        eps = [1.e-7]
    else:
        delta = [.75]
        eps = [1.e-7]

    [z_cur, x_opt, x_low, x_top, bha_od, bha_id, valid] = optimize_x(bha, steer_gtf, mud_weight, md_bit, traj, delta,
                                                                     eps, bh_design=bh_design)
    sag = x2sag(delta[-1], x_opt, bha.dni_to_bit)
    x_mid = (x_low + x_top) / 2
    return SagResult(sag=sag, grid=z_cur, opt=x_opt, low=x_low, top=x_top, od=bha_od, id=bha_id, mid=x_mid, valid=valid)


def optimize_x(bha: BHA, gtf: float, mud_weight: float, md_bit: float, traj: ndarray, delta: List[float],
               eps: List[float], dbh: float = 0., x0: ndarray = None, bh_design: ndarray = None):
    ro_steel = 7850.
    if dbh > 0:
        borehole_enlargement = dbh
    else:
        borehole_enlargement = sqrt((bha.bend_to_bit * sin(bha.bend_angle) / 4) ** 2 +
                                    (0.025 * bha.structure[0].od) ** 2)
    apparent_bend_angle = bha.bend_angle * cos(gtf)

    dz = delta[0]
    [ei, bha_od, bha_id, linear_weight, bend_ind] = bha2input(bha, dz)
    z_cur = np.cumsum(dz * np.ones_like(ei)) - dz
    inc_dni = trajinc(bha.dni_to_bit, md_bit, traj)
    q = linear_weight * (1 - mud_weight / ro_steel) * np.sin(inc_dni)

    if bh_design is None:
        radius = .5 * (bha_od[0] * np.ones_like(ei) + borehole_enlargement)
        x_low = -radius
        x_top = radius
    else:
        bh_size = bh2size(md_bit, z_cur, bh_design)
        x_low = -(bh_size + borehole_enlargement) / 2
        x_top = (bh_size + borehole_enlargement) / 2

    x_opt = (x_low + bha_od / 2.) if inc_dni > 2.5 * pi / 180 else (x_low + x_top) / 2
    if not (x0 is None):
        x_opt = x0.copy()

    e = eps[0]
    x_opt, io = coord_descent(x_opt, ei, q, bha_od, x_low, x_top, dz, bend_ind, apparent_bend_angle, e)

    return [z_cur, x_opt, x_low, x_top, bha_od, bha_id, bool(io)]


def trajinc(md_dni, md_bit, traj):
    md = np.flip(traj[:, 0])
    inc = np.flip(traj[:, 1])
    md = -(md - md_bit)
    inc_dni = np.interp(md_dni, md, inc)
    return inc_dni


def bh2size(md_bit: float, z: ndarray, bh_design: ndarray):
    bh_size = np.zeros_like(z)
    size_num = bh_design.shape[0]
    for i in range(0, size_num):
        bh_size += (bh_design[i, 0] <= (md_bit - z)) * ((md_bit - z) < bh_design[i, 1]) * bh_design[i, 2]
    return bh_size


def x2sag(dz: float, x: np.ndarray, dni2bit: float):
    num = x.shape[0]
    dni_ind = int(round(dni2bit / dz))
    if dni_ind <= 0:
        dni_ind = 1
    elif dni_ind >= num - 1:
        dni_ind = num - 2
    sag = -(atan((x[dni_ind + 1] - x[dni_ind]) / dz) + atan((x[dni_ind] - x[dni_ind - 1]) / dz)) / 2
    return sag
