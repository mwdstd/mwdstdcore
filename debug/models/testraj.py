from math import pi
from .testrun import test_run


def test_traj(num: int, dni_model, g=9.81, b=48000, dip=60. * pi / 180, dec=6. * pi / 180, grid=0., mag_noise=2000.,
              acc_noise=0.3):
    if num == 1:
        [run, qc, plan, stations] = test_run(mds=(0., 1000.), incs=(5. * pi / 180, 8. * pi / 180),
                                    azs=(270. * pi / 180, 285. * pi / 180), num=20, g=g, b=b,
                                    dip=dip, dec=dec, grid=grid, dni_mod=dni_model, mag_noise=mag_noise,
                                    acc_noise=acc_noise)
    elif num == 2:
        [run, qc, plan, stations] = test_run(mds=(0., 1000.), incs=(8. * pi / 180, 87. * pi / 180),
                                    azs=(285. * pi / 180, 285. * pi / 180), num=20, g=g, b=b,
                                    dip=dip, dec=dec, grid=grid, dni_mod=dni_model, mag_noise=mag_noise,
                                    acc_noise=acc_noise)
    elif num == 3:
        [run, qc, plan, stations] = test_run(mds=(0., 1000.), incs=(90. * pi / 180, 90. * pi / 180),
                                    azs=(285. * pi / 180, 285. * pi / 180), num=20, g=g, b=b,
                                    dip=dip, dec=dec, grid=grid, dni_mod=dni_model, mag_noise=mag_noise,
                                    acc_noise=acc_noise)
    elif num == 4:
        [run, qc, plan, stations] = test_run(mds=(0., 1000.), incs=(90. * pi / 180, 90. * pi / 180),
                                    azs=(270. * pi / 180, 270. * pi / 180), num=1, g=g, b=b,
                                    dip=dip, dec=0., grid=0., dni_mod=dni_model, mag_noise=mag_noise,
                                    acc_noise=acc_noise)
    else:
        [run, qc, plan, stations] = test_run(mds=(0., 1000.), incs=(5. * pi / 180, 8. * pi / 180),
                                    azs=(270. * pi / 180, 290. * pi / 180), num=20, g=g, b=b,
                                    dip=dip, dec=dec, grid=grid, dni_mod=dni_model, mag_noise=mag_noise,
                                    acc_noise=acc_noise)
    return [run, qc, plan, stations]
