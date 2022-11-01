from numpy import deg2rad
from mwdstdcore.datamodel import DnIParams, Run, Reference
from tests.simulation import NoiseSettings, generate_traj


dni_err_zero = DnIParams(
    0., 0., 0., 
    0., 0., 0.,
    0., 0., 0.,
    0., 0., 0.,
    0., 0., 0.
    )

dni_err_dsi = DnIParams(
    .5e-2, -.5e-2, 0., 
    500e-6, -500e-6, 500e-6,
    -300, 300, 700,
    1600e-6, -2000e-6, -2200e-6,
    0., 0., 0.
    )

noise_zero = NoiseSettings()
noise_default_acc = NoiseSettings(.25, 0.005)
noise_default_mag = NoiseSettings(.33, 30.)

ref1 = Reference(g=9.81, b=48000, dip=deg2rad(60), dec=deg2rad(6.), grid=0.)


traj1 = generate_traj(mds=(0., 1000.), incs=(deg2rad(5.), deg2rad(8.)), azs=(deg2rad(270.), deg2rad(285)))
traj2 = generate_traj(mds=(0., 1000.), incs=(deg2rad(8.), deg2rad(87.)), azs=(deg2rad(285.), deg2rad(285.)))
traj3 = generate_traj(mds=(0., 1000.), incs=(deg2rad(90.), deg2rad(90.)), azs=(deg2rad(285.), deg2rad(285.)))
traj4 = generate_traj(mds=(0., 1000.), incs=(deg2rad(90.), deg2rad(90.)), azs=(deg2rad(270.), deg2rad(270.)))
traj5 = generate_traj(mds=(0., 1000.), incs=(deg2rad(5.), deg2rad(8.)), azs=(deg2rad(270.), deg2rad(290.)))
