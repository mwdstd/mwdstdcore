from math import pi, radians as deg2rad
import numpy as np
from .survey import Survey
from .station import Station
from .dnimodel import DnIModel
from .run import Run


# create test run
def test_run(mds=(0, 1000), incs=(deg2rad(0), deg2rad(90)), azs=(deg2rad(90), deg2rad(90)), num=25, g=9.81, b=50000,
             dip=deg2rad(70), dec=deg2rad(0), grid=deg2rad(0), dni_mod=DnIModel(), rel_casing_depth=-1., mag_noise=0.,
             acc_noise=0.):
    md = np.linspace(mds[0], mds[1], num)
    inc = np.linspace(incs[0], incs[1], num)
    az = np.linspace(azs[0], azs[1], num)
    # tf = (2 * np.random.rand(num) - 1) * pi
    tf = np.linspace(0, 540, num) * pi / 180
    return test_run_ext(md, inc, az, tf, g, b, dip, dec, grid, dni_mod, rel_casing_depth, mag_noise, acc_noise)


# create test run based on (md, inc, az) arrays
def test_run_ext(md, inc, az, tf=None, g=9.81, b=50000,
                 dip=deg2rad(70), dec=deg2rad(0), grid=deg2rad(0), dni_mod=DnIModel(), rel_casing_depth=-1.,
                 mag_noise=0.,
                 acc_noise=0., acc_noise_freq=0.25, mag_noise_freq=0.33):
    num = len(md)
    if tf is None:
        tf = np.linspace(0, 540, num) * pi / 180

    run = Run()
    run_md = []
    run_xyz = []
    run_ref = []

    i = 0
    qc = []
    stations = []
    plan = np.zeros((num, 4))
    while i < num:
        # check for casing
        if md[0] != md[-1]:
            casing_factor = (md[i] - md[0]) / (md[-1] - md[0])
        else:
            casing_factor = 0
        # unit is nT
        if casing_factor < rel_casing_depth:
            actual_mag_noise = 5000.  # nT
        else:
            if np.random.random() < mag_noise_freq:  # (i % 3) == 0:
                actual_mag_noise = mag_noise
            else:
                actual_mag_noise = 0.  # nT
        # unit is m/s2
        if np.random.random() < acc_noise_freq:  # (i % 4) == 0:
            actual_acc_noise = acc_noise
        else:
            actual_acc_noise = 0.  # m/s2

        station = Station(md[i], inc[i], az[i], tf[i], g, b, dip, dec, grid, 0, 0, 0,
                          actual_mag_noise, actual_acc_noise, dni_mod)
        stations.append(station)
        # check survey for goodness
        qc.append(station.fields.qc)
        plan[i, :] = np.array([md[i], inc[i], az[i], tf[i]])
        srv = Survey(station)
        run_md.append(md[i])
        run_xyz.append([srv.g_xyz[0], srv.g_xyz[1], srv.g_xyz[2], srv.b_xyz[0], srv.b_xyz[1], srv.b_xyz[2]])
        run_ref.append([srv.g_ref, srv.b_ref, srv.d_ref])

        i += 1

        run.md = np.asarray(run_md)
        run.dni_xyz = np.asarray(run_xyz)
        run.ref = np.asarray(run_ref)
        run.survey_status = np.zeros_like(run.md)
        run.axis_status = -np.ones_like(run.md)
    return run, qc, plan, stations
