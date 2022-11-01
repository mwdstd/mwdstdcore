from typing import Dict, List, Tuple
import attr
import numpy as np
from mwdstdcore.datamodel import DnIParams, Run, Reference, TfStation, FullStation, Survey
from mwdstdcore.datamodel.calc.survey import calc_survey


@attr.s(auto_attribs=True)
class NoiseSettings:
    magnitude: float = 0.
    frequency: float = 0.

def generate_dni_err(errmod: Dict[str, float]):
    arr = [
        errmod['ASX'], errmod['ASY'], errmod['ASZ'],
        errmod['ABX'], errmod['ABY'], errmod['ABZ'],
        errmod['MSX'], errmod['MSY'], errmod['MSZ'],
        errmod['MBX'], errmod['MBY'], errmod['MBZ'],
        errmod['MXY'], errmod['MXZ'], errmod['MYZ']
    ] * np.random.randn(15)
    return DnIParams.fromarray(arr)

def generate_traj(mds: Tuple[float, float], incs: Tuple[float, float], azs: Tuple[float, float], num: int = 20 ) -> List[TfStation]:
    mda = np.linspace(mds[0], mds[1], num)
    inca = np.linspace(incs[0], incs[1], num)
    aza = np.linspace(azs[0], azs[1], num)
    # tf = (2 * np.random.rand(num) - 1) * pi
    tfa = np.linspace(0, np.deg2rad(540), num)
    return [TfStation(md, inc, az, tf) for md, inc, az, tf in zip(mda, inca, aza, tfa)]

def apply_sensor_error(s: Survey, dni_err: DnIParams) -> Survey:
    identity_mat = np.eye(3)
    g_xyz = np.array([s.gx, s.gy, s.gz])
    b_xyz = np.array([s.bx, s.by, s.bz])
    as_err = np.diag([dni_err.ASX, dni_err.ASY, dni_err.ASZ])
    ab_err = np.array([dni_err.ABX, dni_err.ABY, dni_err.ABZ])
    ms_err = np.diag([dni_err.MSX, dni_err.MSY, dni_err.MSZ])
    mb_err = np.array([dni_err.MBX, dni_err.MBY, dni_err.MBZ])
    mi_err = np.array([[0, dni_err.MXY, dni_err.MXZ], [-dni_err.MXY, 0, dni_err.MYZ], [-dni_err.MXZ, -dni_err.MYZ, 0]])
    g_xyz = (identity_mat + as_err) @ g_xyz + ab_err
    b_xyz = (identity_mat + ms_err + mi_err) @ b_xyz + mb_err
    return Survey(md=s.md, gx=g_xyz[0], gy=g_xyz[1], gz=g_xyz[2], bx=b_xyz[0], by=b_xyz[1], bz=b_xyz[2])

def apply_noise(s: Survey, acc_noise: NoiseSettings, mag_noise: NoiseSettings) -> Survey:
    g_xyz = [s.gx, s.gy, s.gz]
    if np.random.random() < acc_noise.frequency:
        g_xyz += np.random.randn(3) * acc_noise.magnitude
    b_xyz = [s.bx, s.by, s.bz]
    if np.random.random() < mag_noise.frequency:
        b_xyz += np.random.randn(3) * mag_noise.magnitude
    return Survey(md=s.md, gx=g_xyz[0], gy=g_xyz[1], gz=g_xyz[2], bx=b_xyz[0], by=b_xyz[1], bz=b_xyz[2])
    

def simulate_run(traj: List[TfStation], ref: Reference, dni_err: DnIParams, acc_noise: NoiseSettings, mag_noise: NoiseSettings) -> Run:
    full_stations = [FullStation(md=st.md, inc=st.inc, az=st.az, tf=st.tf, tg=ref.g, tb=ref.b, dip=ref.dip) for st in traj]
    true_surveys = [calc_survey(st, ref.dec, ref.grid) for st in full_stations]
    err_surveys = [apply_noise(s, acc_noise, mag_noise) for s in true_surveys]
    err_surveys = [apply_sensor_error(s, dni_err) for s in err_surveys]
    return Run(err_surveys, 0., True, reference=[ref]*len(traj))