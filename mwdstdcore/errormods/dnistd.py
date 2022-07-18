dni_std = {'ABX': 0.004,  # m/s2, X-Accelerometer Bias
           'ABY': 0.004,  # m/s2, Y-Accelerometer Bias
           'ABZ': 0.004,  # m/s2, Z-Accelerometer Bias
           'ASX': 0.0005,  # -, X-Accelerometer Scale Factor
           'ASY': 0.0005,  # -, Y-Accelerometer Scale Factor
           'ASZ': 0.0005,  # -, Z-Accelerometer Scale Factor
           'MBX': 70.,  # nT, X-Magnetometer Bias + Axial Drillstring Interference
           'MBY': 70.,  # nT, Y-Magnetometer Bias
           'MBZ': 230.,  # nT, Z-Magnetometer Bias
           'MSX': 0.0016,  # -, X-Magnetometer Scale Factor
           'MSY': 0.0016,  # -, Y-Magnetometer Scale Factor
           'MSZ': 0.0016,  # -, Z-Magnetometer Scale Factor
           'MXY': 0.00035,  # rad, XY Accelerometers-Magnetometers Misalignment Angle
           'MXZ': 0.00035,  # rad, XZ Accelerometers-Magnetometers Misalignment Angle
           'MYZ': 0.00035}   # rad, YZ Accelerometers-Magnetometers Misalignment Angle


def_mask = {'ABX': 1, 'ABY': 1, 'ABZ': 1, 'ASX': 1, 'ASY': 1, 'ASZ': 1,
            'MBX': 1, 'MBY': 1, 'MBZ': 1, 'MSX': 1, 'MSY': 1, 'MSZ': 1,
            'MXY': 1, 'MXZ': 1, 'MYZ': 1}
