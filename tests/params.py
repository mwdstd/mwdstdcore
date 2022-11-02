import jsons
from numpy import deg2rad
from mwdstdcore.datamodel import DnIParams, Reference, BHA
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

bha_rss = {
    "structure": [
        {"type": "bit", "od": 0.1556, "id": 0.0254, "weight": 30,
            "length": 0.15, "material": "steel", "description": "", "sn": ""},
        {"type": "rss", "od": 0.133, "id": 0.0254, "weight": 310,
            "length": 2.93, "material": "nmsteel", "description": "", "sn": ""},
        {"type": "mwd", "od": 0.1308, "id": 0.034, "weight": 600,
            "length": 6.11, "material": "nmsteel", "description": "", "sn": ""},
        {"type": "string_stabilizer", "od": 0.127, "id": 0.04, "weight": 100,
            "length": 1.00, "material": "nmsteel", "description": "", "sn": ""},
        {"type": "lwd", "od": 0.1308, "id": 0.035, "weight": 330,
            "length": 3.37, "material": "nmsteel", "description": "", "sn": ""},
        {"type": "sub", "od": 0.1207, "id": 0.0683, "weight": 122,
            "length": 1.99, "material": "nmsteel", "description": "", "sn": ""},
        {"type": "string_stabilizer", "od": 0.127, "id": 0.04, "weight": 100,
            "length": 0.88, "material": "nmsteel", "description": "", "sn": ""},
        {"type": "lwd", "od": 0.1347, "id": 0.0476, "weight": 430,
            "length": 4.39, "material": "nmsteel", "description": "", "sn": ""},
        {"type": "string_stabilizer", "od": 0.1347, "id": 0.03, "weight": 170,
            "length": 1.59, "material": "nmsteel", "description": "", "sn": ""},
        {"type": "sub", "od": 0.1355, "id": 0.03, "weight": 560,
            "length": 5.2, "material": "nmsteel", "description": "", "sn": ""},
        {"type": "string_stabilizer", "od": 0.1347, "id": 0.03, "weight": 170,
            "length": 1.58, "material": "nmsteel", "description": "", "sn": ""},
        {"type": "sub", "od": 0.127, "id": 0.035, "weight": 70,
            "length": 0.77, "material": "nmsteel", "description": "", "sn": ""},
        {"type": "nmdc", "od": 0.1238, "id": 0.0685, "weight": 120,
            "length": 1.82, "material": "nmsteel", "description": "", "sn": ""},
        {"type": "sub", "od": 0.127, "id": 0.035, "weight": 70,
            "length": 0.61, "material": "nmsteel", "description": "", "sn": ""},
        {"type": "nmdc", "od": 0.127, "id": 0.054, "weight": 770, 
            "length": 9.45, "material": "nmsteel", "description": "", "sn": ""}
    ],
    "blades": [
        {"od":  0.1524, "center_to_bit":  1.0, "length":  0.36},
        {"od":  0.1492, "center_to_bit":  9.79, "length":  0.36},
        {"od":  0.1492, "center_to_bit":  16.0, "length":  0.36},
        {"od":  0.1461, "center_to_bit":  18.6, "length":  0.36},
        {"od":  0.152, "center_to_bit":  21.6, "length":  0.36},
        {"od":  0.1461, "center_to_bit":  29.0, "length":  0.36}
    ],
    "bend_angle": 0.0,
    "bend_to_bit": 0.0,
    "dni_to_bit": 7.85
}
bha_rss = jsons.load(bha_rss, BHA)

bha_xcd = {
    "structure": [
        {"type": "bit", "od": 0.311, "id": 0.076, "weight": 100,
            "length": 0.40, "material": "steel", "description": "", "sn": ""},
        {"type": "rss", "od": 0.232, "id": 0.171, "weight": 2000,
            "length": 8.65, "material": "nmsteel", "description": "", "sn": ""},
        {"type": "lwd", "od": 0.203, "id": 0.108, "weight": 1400,
            "length": 5.80, "material": "nmsteel", "description": "", "sn": ""},
        {"type": "mwd", "od": 0.213, "id": 0.150, "weight": 1600,
            "length": 8.50, "material": "nmsteel", "description": "", "sn": ""},
        {"type": "string_stabilizer", "od": 0.203, "id": 0.071, "weight": 500,
            "length": 2.30, "material": "nmsteel", "description": "", "sn": ""},
        {"type": "sub", "od": 0.203, "id": 0.073, "weight": 300,
            "length": 1.20, "material": "nmsteel", "description": "", "sn": ""},
        {"type": "nmdc", "od": 0.210, "id": 0.073, "weight": 2200,
            "length": 9.40, "material": "nmsteel", "description": "", "sn": ""},
        {"type": "nmdc", "od": 0.195, "id": 0.070, "weight": 1800,
            "length": 8.80, "material": "nmsteel", "description": "", "sn": ""},
        {"type": "sub", "od": 0.203, "id": 0.089, "weight": 500,
            "length": 2.40, "material": "steel", "description": "", "sn": ""},
        {"type": "sub", "od": 0.216, "id": 0.076, "weight": 300,
            "length": 1.10, "material": "steel", "description": "", "sn": ""},
        {"type": "hwdp", "od": 0.168, "id": 0.114, "weight": 1000,
            "length": 9.40, "material": "steel", "description": "", "sn": ""},
        {"type": "collar", "od": 0.216, "id": 0.076, "weight": 2000,
            "length": 10.00, "material": "steel", "description": "", "sn": ""}
    ],
    "blades": [
        {"od":  0.303, "center_to_bit":  0.77, "length":  0.32},
        {"od":  0.303, "center_to_bit":  4.23, "length":  0.32},
        {"od":  0.235, "center_to_bit":  9.9, "length":  0.2},
        {"od":  0.235, "center_to_bit":  11.2, "length":  0.2},
        {"od":  0.235, "center_to_bit":  11.9, "length":  0.2},
        {"od":  0.235, "center_to_bit":  13.5, "length":  0.2},
        {"od":  0.308, "center_to_bit":  24.5, "length":  0.5}
    ],
    "bend_angle": 0.00,
    "bend_to_bit": 0.0,
    "dni_to_bit": 5.5
}
bha_xcd = jsons.load(bha_xcd, BHA)