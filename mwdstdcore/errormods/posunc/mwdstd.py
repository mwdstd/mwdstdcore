from math import pi

mwdstd0 = {
           # depth error terms
           'DRFR': {'wfunc': 'DREF', 'value': 0.35, 'mode': 'R'},  # m, Depth: Depth Reference - Random
           'DSFS': {'wfunc': 'DSF', 'value': 2.4e-4, 'mode': 'S'},  # -, Depth: Depth Scale Factor - Systematic
           'DSTG': {'wfunc': 'DST', 'value': 2.2e-7, 'mode': 'G'},  # 1/m, Depth: Depth Stretch - Global
           # sensors' error terms
           'ABX': {'wfunc': 'ABX', 'value': 0.004, 'mode': 'S'},  # m/s2, X-Accelerometer Bias
           'ABY': {'wfunc': 'ABY', 'value': 0.004, 'mode': 'S'},  # m/s2, Y-Accelerometer Bias
           'ABZ': {'wfunc': 'ABZ', 'value': 0.004, 'mode': 'S'},  # m/s2, Z-Accelerometer Bias
           'ASX': {'wfunc': 'ASX', 'value': 0.0005, 'mode': 'S'},  # -, X-Accelerometer Scale Factor
           'ASY': {'wfunc': 'ASY', 'value': 0.0005, 'mode': 'S'},  # -, Y-Accelerometer Scale Factor
           'ASZ': {'wfunc': 'ASZ', 'value': 0.0005, 'mode': 'S'},  # -, Z-Accelerometer Scale Factor
           'MBX': {'wfunc': 'MBX', 'value': 70., 'mode': 'S'},  # nT, X-Magnetometer Bias
           'MBY': {'wfunc': 'MBY', 'value': 70., 'mode': 'S'},  # nT, Y-Magnetometer Bias
           'MBZ': {'wfunc': 'MBZ', 'value': 70., 'mode': 'S'},  # nT, Z-Magnetometer Bias
           'MSX': {'wfunc': 'MSX', 'value': 0.0016, 'mode': 'S'},  # -, X-Magnetometer Scale Factor
           'MSY': {'wfunc': 'MSY', 'value': 0.0016, 'mode': 'S'},  # -, Y-Magnetometer Scale Factor
           'MSZ': {'wfunc': 'MSZ', 'value': 0.0016, 'mode': 'S'},  # -, Z-Magnetometer Scale Factor
           # declination error terms
           'DECG': {'wfunc': 'AZ', 'value': 0.36*pi/180, 'mode': 'G'},  # rad, Declination Constant Error
           'DBHG': {'wfunc': 'DBH', 'value': 5000.*pi/180, 'mode': 'G'},  # rad, Declination Var Error
           # axial drillstring interference error terms
           'AMIC': {'wfunc': 'AZ', 'value': 0.25*pi/180, 'mode': 'S'},  # rad, Axial DSI Constant Error
           'AMID': {'wfunc': 'AMID', 'value': 0.6*pi/180, 'mode': 'S'},  # rad, Axial DSI Var Error
           # misalignment error terms
           'SAG': {'wfunc': 'SAG', 'value': 0.2*pi/180, 'mode': 'S'},  # rad, BHA Sag
           'MX': {'wfunc': 'MX', 'value': 0.06*pi/180, 'mode': 'S'},  # rad, X-Axis Misalignment
           'MY': {'wfunc': 'MY', 'value': 0.06*pi/180, 'mode': 'S'}   # rad, Y-Axis Misalignment
        }

mwdstd0_poor = {
           # depth error terms
           'DRFR': {'wfunc': 'DREF', 'value': 0.35, 'mode': 'R'},  # m, Depth: Depth Reference - Random
           'DSFS': {'wfunc': 'DSF', 'value': 2.4e-4, 'mode': 'S'},  # -, Depth: Depth Scale Factor - Systematic
           'DSTG': {'wfunc': 'DST', 'value': 2.2e-7, 'mode': 'G'},  # 1/m, Depth: Depth Stretch - Global
           # sensors' error terms
           'ABX': {'wfunc': 'ABX', 'value': 0.004, 'mode': 'S'},  # m/s2, X-Accelerometer Bias
           'ABY': {'wfunc': 'ABY', 'value': 0.004, 'mode': 'S'},  # m/s2, Y-Accelerometer Bias
           'ABZ': {'wfunc': 'ABZ', 'value': 0.004, 'mode': 'S'},  # m/s2, Z-Accelerometer Bias
           'ASX': {'wfunc': 'ASX', 'value': 0.0005, 'mode': 'S'},  # -, X-Accelerometer Scale Factor
           'ASY': {'wfunc': 'ASY', 'value': 0.0005, 'mode': 'S'},  # -, Y-Accelerometer Scale Factor
           'ASZ': {'wfunc': 'ASZ', 'value': 0.0005, 'mode': 'S'},  # -, Z-Accelerometer Scale Factor
           'MBX': {'wfunc': 'MBX', 'value': 70., 'mode': 'S'},  # nT, X-Magnetometer Bias
           'MBY': {'wfunc': 'MBY', 'value': 70., 'mode': 'S'},  # nT, Y-Magnetometer Bias
           'MBZ': {'wfunc': 'MBZ', 'value': 70., 'mode': 'S'},  # nT, Z-Magnetometer Bias
           'MSX': {'wfunc': 'MSX', 'value': 0.0016, 'mode': 'S'},  # -, X-Magnetometer Scale Factor
           'MSY': {'wfunc': 'MSY', 'value': 0.0016, 'mode': 'S'},  # -, Y-Magnetometer Scale Factor
           'MSZ': {'wfunc': 'MSZ', 'value': 0.0016, 'mode': 'S'},  # -, Z-Magnetometer Scale Factor
           # declination error terms
           'DECG': {'wfunc': 'AZ', 'value': 0.36*pi/180, 'mode': 'G'},  # rad, Declination Constant Error
           'DBHG': {'wfunc': 'DBH', 'value': 5000.*pi/180, 'mode': 'G'},  # rad, Declination Var Error
           # axial drillstring interference error terms
           'AMIC': {'wfunc': 'AZ', 'value': 0.25*pi/180, 'mode': 'S'},  # rad, Axial DSI Constant Error
           'AMID': {'wfunc': 'AMID', 'value': 2.5*pi/180, 'mode': 'S'},  # rad, Axial DSI Var Error
           # misalignment error terms
           'SAG': {'wfunc': 'SAG', 'value': 0.2*pi/180, 'mode': 'S'},  # rad, BHA Sag
           'MX': {'wfunc': 'MX', 'value': 0.06*pi/180, 'mode': 'S'},  # rad, X-Axis Misalignment
           'MY': {'wfunc': 'MY', 'value': 0.06*pi/180, 'mode': 'S'}   # rad, Y-Axis Misalignment
        }

mwdaxint = {
           # depth error terms
           'DRFR': {'wfunc': 'DREF', 'value': 0.35, 'mode': 'R'},  # m, Depth: Depth Reference - Random
           'DSFS': {'wfunc': 'DSF', 'value': 2.4e-4, 'mode': 'S'},  # -, Depth: Depth Scale Factor - Systematic
           'DSTG': {'wfunc': 'DST', 'value': 2.2e-7, 'mode': 'G'},  # 1/m, Depth: Depth Stretch - Global
           # sensors' error terms
           'ABX': {'wfunc': 'ABIX', 'value': 0.004, 'mode': 'S'},  # m/s2, X-Accelerometer Bias
           'ABY': {'wfunc': 'ABIY', 'value': 0.004, 'mode': 'S'},  # m/s2, Y-Accelerometer Bias
           'ABZ': {'wfunc': 'ABIZ', 'value': 0.004, 'mode': 'S'},  # m/s2, Z-Accelerometer Bias
           'ASX': {'wfunc': 'ASIX', 'value': 0.0005, 'mode': 'S'},  # -, X-Accelerometer Scale Factor
           'ASY': {'wfunc': 'ASIY', 'value': 0.0005, 'mode': 'S'},  # -, Y-Accelerometer Scale Factor
           'ASZ': {'wfunc': 'ASIZ', 'value': 0.0005, 'mode': 'S'},  # -, Z-Accelerometer Scale Factor
           'MBX': {'wfunc': 'MBIX', 'value': 70., 'mode': 'S'},  # nT, X-Magnetometer Bias
           'MBY': {'wfunc': 'MBIY', 'value': 70., 'mode': 'S'},  # nT, Y-Magnetometer Bias
           'MSX': {'wfunc': 'MSIX', 'value': 0.0016, 'mode': 'S'},  # -, X-Magnetometer Scale Factor
           'MSY': {'wfunc': 'MSIY', 'value': 0.0016, 'mode': 'S'},  # -, Y-Magnetometer Scale Factor
           # declination error terms
           'DECG': {'wfunc': 'AZ', 'value': 0.36*pi/180, 'mode': 'G'},  # rad, Declination Constant Error
           'DBHG': {'wfunc': 'DBH', 'value': 5000.*pi/180, 'mode': 'G'},  # rad, Declination Var Error
           # axial drillstring interference error terms
           'MBI': {'wfunc': 'MBI', 'value': 130., 'mode': 'W'},  # nT, Total B Reference Error
           'MDI': {'wfunc': 'MDI', 'value': 0.2*pi/180, 'mode': 'W'},  # rad, Dip Reference Error
           # misalignment error terms
           'SAG': {'wfunc': 'SAG', 'value': 0.2*pi/180, 'mode': 'S'},  # rad, BHA Sag
           'MX': {'wfunc': 'MX', 'value': 0.06*pi/180, 'mode': 'S'},  # rad, X-Axis Misalignment
           'MY': {'wfunc': 'MY', 'value': 0.06*pi/180, 'mode': 'S'}   # rad, Y-Axis Misalignment
        }

mwdstd_dni = {
               # sensors' error terms
               'ABX': {'wfunc': 'ABX', 'value': 0.004, 'mode': 'S'},  # m/s2, X-Accelerometer Bias
               'ABY': {'wfunc': 'ABY', 'value': 0.004, 'mode': 'S'},  # m/s2, Y-Accelerometer Bias
               'ABZ': {'wfunc': 'ABZ', 'value': 0.004, 'mode': 'S'},  # m/s2, Z-Accelerometer Bias
               'ASX': {'wfunc': 'ASX', 'value': 0.0005, 'mode': 'S'},  # -, X-Accelerometer Scale Factor
               'ASY': {'wfunc': 'ASY', 'value': 0.0005, 'mode': 'S'},  # -, Y-Accelerometer Scale Factor
               'ASZ': {'wfunc': 'ASZ', 'value': 0.0005, 'mode': 'S'},  # -, Z-Accelerometer Scale Factor
               'MBX': {'wfunc': 'MBX', 'value': 70., 'mode': 'S'},  # nT, X-Magnetometer Bias
               'MBY': {'wfunc': 'MBY', 'value': 70., 'mode': 'S'},  # nT, Y-Magnetometer Bias
               'MBZ': {'wfunc': 'MBZ', 'value': 70., 'mode': 'S'},  # nT, Z-Magnetometer Bias
               'MSX': {'wfunc': 'MSX', 'value': 0.0016, 'mode': 'S'},  # -, X-Magnetometer Scale Factor
               'MSY': {'wfunc': 'MSY', 'value': 0.0016, 'mode': 'S'},  # -, Y-Magnetometer Scale Factor
               'MSZ': {'wfunc': 'MSZ', 'value': 0.0016, 'mode': 'S'},  # -, Z-Magnetometer Scale Factor
               'MXY': {'wfunc': 'MXY', 'value': 0.001, 'mode': 'S'},  # rad, Angular Twist Between Accels and Mags
               'MXZ': {'wfunc': 'MXZ', 'value': 0.001, 'mode': 'S'},  # rad, X-Bend Between Accels and Mags
               'MYZ': {'wfunc': 'MYZ', 'value': 0.001, 'mode': 'S'},  # rad, Y-Bend Between Accels and Mags
               # axial drillstring interference error terms
               'AMIL': {'wfunc': 'AMIL', 'value': 220., 'mode': 'S'},  # nT, Axial DSI Constant Error
            }

mwdstd4 = {
           # depth error terms
           'DRFR': {'wfunc': 'DREF', 'value': 0.35, 'mode': 'R'},  # m, Depth: Depth Reference - Random
           'DSFS': {'wfunc': 'DSF', 'value': 0.00056, 'mode': 'S'},  # -, Depth: Depth Scale Factor - Systematic
           'DSTG': {'wfunc': 'DST', 'value': 0.00000022, 'mode': 'G'},  # 1/m, Depth: Depth Stretch - Global
           # sensors' error terms
           'ABXY-TI1S': {'wfunc': 'ABXY-TI1', 'value': 0.004, 'mode': 'S'},  # m/s2, XY-Accelerometer Bias 1
           'ABXY-TI2S': {'wfunc': 'ABXY-TI2', 'value': 0.004, 'mode': 'S'},  # m/s2, XY-Accelerometer Bias 2
           'ABZ': {'wfunc': 'ABZ', 'value': 0.004, 'mode': 'S'},  # m/s2, Z-Accelerometer Bias
           'ASXY-TI1S': {'wfunc': 'ASXY-TI1', 'value': 0.0005, 'mode': 'S'},  # -, XY-Accelerometer Scale Factor 1
           'ASXY-TI2S': {'wfunc': 'ASXY-TI2', 'value': 0.0005, 'mode': 'S'},  # -, XY-Accelerometer Scale Factor 2
           'ASXY-TI3S': {'wfunc': 'ASXY-TI3', 'value': 0.0005, 'mode': 'S'},  # -, XY-Accelerometer Scale Factor 3
           'ASZ': {'wfunc': 'ASZ', 'value': 0.0005, 'mode': 'S'},  # -, Z-Accelerometer Scale Factor
           'MBXY-TI1S': {'wfunc': 'MBXY-TI1', 'value': 70., 'mode': 'S'},  # nT, XY-Magnetometer Bias 1
           'MBXY-TI2S': {'wfunc': 'MBXY-TI2', 'value': 70., 'mode': 'S'},  # nT, XY-Magnetometer Bias 2
           'MBZ': {'wfunc': 'MBZ', 'value': 70., 'mode': 'S'},  # nT, Z-Magnetometer Bias
           'MSXY-TI1S': {'wfunc': 'MSXY-TI1', 'value': 0.0016, 'mode': 'S'},  # -, XY-Magnetometer Scale Factor 1
           'MSXY-TI2S': {'wfunc': 'MSXY-TI2', 'value': 0.0016, 'mode': 'S'},  # -, XY-Magnetometer Scale Factor 2
           'MSXY-TI3S': {'wfunc': 'MSXY-TI3', 'value': 0.0016, 'mode': 'S'},  # -, XY-Magnetometer Scale Factor 3
           'MSZ': {'wfunc': 'MSZ', 'value': 0.0016, 'mode': 'S'},  # -, Z-Magnetometer Scale Factor
           # declination error terms
           'DECG': {'wfunc': 'AZ', 'value': 0.36*pi/180, 'mode': 'G'},  # rad, Global Declination Constant Error
           'DBHG': {'wfunc': 'DBH', 'value': 5000.*pi/180, 'mode': 'G'},  # rad, Global Declination Var Error
           'DECR': {'wfunc': 'AZ', 'value': 0.1*pi/180, 'mode': 'R'},  # rad, Random Declination Constant Error
           'DBHR': {'wfunc': 'DBH', 'value': 3000.*pi/180, 'mode': 'R'},  # rad, Random Declination Var Error
           # axial drillstring interference error terms
           'AMIL': {'wfunc': 'AMIL', 'value': 220., 'mode': 'S'},  # nT, Axial DSI Constant Error
           # misalignment error terms
           'SAG': {'wfunc': 'SAG', 'value': 0.2*pi/180, 'mode': 'S'},  # rad, BHA Sag
           'XYM1': {'wfunc': 'XYM1', 'value': 0.1*pi/180, 'mode': 'S'},  # rad, XY-Axis Misalignment 1
           'XYM2': {'wfunc': 'XYM2', 'value': 0.1*pi/180, 'mode': 'S'},  # rad, XY-Axis Misalignment 2
           'XYM3': {'wfunc': 'XYM3', 'value': 0.1*pi/180, 'mode': 'S'},  # rad, XY-Axis Misalignment 3
           'XYM4': {'wfunc': 'XYM4', 'value': 0.1*pi/180, 'mode': 'S'},  # rad, XY-Axis Misalignment 4
        }

mwdstd4_ms_sag_ifr1 = {
           # depth error terms
           'DRFR': {'wfunc': 'DREF', 'value': 0.35, 'mode': 'R'},  # m, Depth: Depth Reference - Random
           'DSFS': {'wfunc': 'DSF', 'value': 0.00056, 'mode': 'S'},  # -, Depth: Depth Scale Factor - Systematic
           'DSTG': {'wfunc': 'DST', 'value': 0.00000022, 'mode': 'G'},  # 1/m, Depth: Depth Stretch - Global
           # sensors' error terms
           'ABXY-TI1S': {'wfunc': 'ABXY-TI1', 'value': 0.004, 'mode': 'S'},  # m/s2, XY-Accelerometer Bias 1
           'ABXY-TI2S': {'wfunc': 'ABXY-TI2', 'value': 0.004, 'mode': 'S'},  # m/s2, XY-Accelerometer Bias 2
           'ABZ': {'wfunc': 'ABZ', 'value': 0.004, 'mode': 'S'},  # m/s2, Z-Accelerometer Bias
           'ASXY-TI1S': {'wfunc': 'ASXY-TI1', 'value': 0.0005, 'mode': 'S'},  # -, XY-Accelerometer Scale Factor 1
           'ASXY-TI2S': {'wfunc': 'ASXY-TI2', 'value': 0.0005, 'mode': 'S'},  # -, XY-Accelerometer Scale Factor 2
           'ASXY-TI3S': {'wfunc': 'ASXY-TI3', 'value': 0.0005, 'mode': 'S'},  # -, XY-Accelerometer Scale Factor 3
           'ASZ': {'wfunc': 'ASZ', 'value': 0.0005, 'mode': 'S'},  # -, Z-Accelerometer Scale Factor
           'MBXY-TI1S': {'wfunc': 'MBXY-TI1', 'value': 35., 'mode': 'S'},  # nT, XY-Magnetometer Bias 1
           'MBXY-TI2S': {'wfunc': 'MBXY-TI2', 'value': 35., 'mode': 'S'},  # nT, XY-Magnetometer Bias 2
           'MBZ': {'wfunc': 'MBZ', 'value': 35., 'mode': 'S'},  # nT, Z-Magnetometer Bias
           'MSXY-TI1S': {'wfunc': 'MSXY-TI1', 'value': 0.0008, 'mode': 'S'},  # -, XY-Magnetometer Scale Factor 1
           'MSXY-TI2S': {'wfunc': 'MSXY-TI2', 'value': 0.0008, 'mode': 'S'},  # -, XY-Magnetometer Scale Factor 2
           'MSXY-TI3S': {'wfunc': 'MSXY-TI3', 'value': 0.0008, 'mode': 'S'},  # -, XY-Magnetometer Scale Factor 3
           'MSZ': {'wfunc': 'MSZ', 'value': 0.0008, 'mode': 'S'},  # -, Z-Magnetometer Scale Factor
           # declination error terms
           'DECG': {'wfunc': 'AZ', 'value': 0.15*pi/180, 'mode': 'G'},  # rad, Global Declination Constant Error
           'DBHG': {'wfunc': 'DBH', 'value': 1500.*pi/180, 'mode': 'G'},  # rad, Global Declination Var Error
           'DECR': {'wfunc': 'AZ', 'value': 0.1*pi/180, 'mode': 'R'},  # rad, Random Declination Constant Error
           'DBHR': {'wfunc': 'DBH', 'value': 3000.*pi/180, 'mode': 'R'},  # rad, Random Declination Var Error
           # axial drillstring interference error terms
           'AMIL': {'wfunc': 'AMIL', 'value': 100., 'mode': 'S'},  # nT, Axial DSI Constant Error
           # misalignment error terms
           'SAG': {'wfunc': 'SAG', 'value': 0.08*pi/180, 'mode': 'S'},  # rad, BHA Sag
           'XYM1': {'wfunc': 'XYM1', 'value': 0.1*pi/180, 'mode': 'S'},  # rad, XY-Axis Misalignment 1
           'XYM2': {'wfunc': 'XYM2', 'value': 0.1*pi/180, 'mode': 'S'},  # rad, XY-Axis Misalignment 2
           'XYM3': {'wfunc': 'XYM3', 'value': 0.1*pi/180, 'mode': 'S'},  # rad, XY-Axis Misalignment 3
           'XYM4': {'wfunc': 'XYM4', 'value': 0.1*pi/180, 'mode': 'S'},  # rad, XY-Axis Misalignment 4
        }

mwdstd4_hd = {
           # depth error terms
           'DRFR': {'wfunc': 'DREF', 'value': 0.35, 'mode': 'R'},  # m, Depth: Depth Reference - Random
           'DSFS': {'wfunc': 'DSF', 'value': 0.00056, 'mode': 'S'},  # -, Depth: Depth Scale Factor - Systematic
           'DSTG': {'wfunc': 'DST', 'value': 0.00000022, 'mode': 'G'},  # 1/m, Depth: Depth Stretch - Global
           # sensors' error terms
           'ABXY-TI1S': {'wfunc': 'ABXY-TI1', 'value': 0.004, 'mode': 'S'},  # m/s2, XY-Accelerometer Bias 1
           'ABXY-TI2S': {'wfunc': 'ABXY-TI2', 'value': 0.004, 'mode': 'S'},  # m/s2, XY-Accelerometer Bias 2
           'ABZ': {'wfunc': 'ABZ', 'value': 0.004, 'mode': 'S'},  # m/s2, Z-Accelerometer Bias
           'ASXY-TI1S': {'wfunc': 'ASXY-TI1', 'value': 0.0005, 'mode': 'S'},  # -, XY-Accelerometer Scale Factor 1
           'ASXY-TI2S': {'wfunc': 'ASXY-TI2', 'value': 0.0005, 'mode': 'S'},  # -, XY-Accelerometer Scale Factor 2
           'ASXY-TI3S': {'wfunc': 'ASXY-TI3', 'value': 0.0005, 'mode': 'S'},  # -, XY-Accelerometer Scale Factor 3
           'ASZ': {'wfunc': 'ASZ', 'value': 0.0005, 'mode': 'S'},  # -, Z-Accelerometer Scale Factor
           'MBXY-TI1S': {'wfunc': 'MBXY-TI1', 'value': 70., 'mode': 'S'},  # nT, XY-Magnetometer Bias 1
           'MBXY-TI2S': {'wfunc': 'MBXY-TI2', 'value': 70., 'mode': 'S'},  # nT, XY-Magnetometer Bias 2
           'MBZ': {'wfunc': 'MBZ', 'value': 70., 'mode': 'S'},  # nT, Z-Magnetometer Bias
           'MSXY-TI1S': {'wfunc': 'MSXY-TI1', 'value': 0.0016, 'mode': 'S'},  # -, XY-Magnetometer Scale Factor 1
           'MSXY-TI2S': {'wfunc': 'MSXY-TI2', 'value': 0.0016, 'mode': 'S'},  # -, XY-Magnetometer Scale Factor 2
           'MSXY-TI3S': {'wfunc': 'MSXY-TI3', 'value': 0.0016, 'mode': 'S'},  # -, XY-Magnetometer Scale Factor 3
           'MSZ': {'wfunc': 'MSZ', 'value': 0.0016, 'mode': 'S'},  # -, Z-Magnetometer Scale Factor
           # declination error terms
           'DECG': {'wfunc': 'AZ', 'value': 0.3*pi/180, 'mode': 'G'},  # rad, Global Declination Constant Error
           'DBHG': {'wfunc': 'DBH', 'value': 4118.*pi/180, 'mode': 'G'},  # rad, Global Declination Var Error
           'DECR': {'wfunc': 'AZ', 'value': 0.1*pi/180, 'mode': 'R'},  # rad, Random Declination Constant Error
           'DBHR': {'wfunc': 'DBH', 'value': 3000.*pi/180, 'mode': 'R'},  # rad, Random Declination Var Error
           # axial drillstring interference error terms
           'AMIL': {'wfunc': 'AMIL', 'value': 220., 'mode': 'S'},  # nT, Axial DSI Constant Error
           # misalignment error terms
           'SAG': {'wfunc': 'SAG', 'value': 0.2*pi/180, 'mode': 'S'},  # rad, BHA Sag
           'XYM1': {'wfunc': 'XYM1', 'value': 0.1*pi/180, 'mode': 'S'},  # rad, XY-Axis Misalignment 1
           'XYM2': {'wfunc': 'XYM2', 'value': 0.1*pi/180, 'mode': 'S'},  # rad, XY-Axis Misalignment 2
           'XYM3': {'wfunc': 'XYM3', 'value': 0.1*pi/180, 'mode': 'S'},  # rad, XY-Axis Misalignment 3
           'XYM4': {'wfunc': 'XYM4', 'value': 0.1*pi/180, 'mode': 'S'},  # rad, XY-Axis Misalignment 4
        }

mwdstd4_sag = {
           # depth error terms
           'DRFR': {'wfunc': 'DREF', 'value': 0.35, 'mode': 'R'},  # m, Depth: Depth Reference - Random
           'DSFS': {'wfunc': 'DSF', 'value': 0.00056, 'mode': 'S'},  # -, Depth: Depth Scale Factor - Systematic
           'DSTG': {'wfunc': 'DST', 'value': 0.00000022, 'mode': 'G'},  # 1/m, Depth: Depth Stretch - Global
           # sensors' error terms
           'ABXY-TI1S': {'wfunc': 'ABXY-TI1', 'value': 0.004, 'mode': 'S'},  # m/s2, XY-Accelerometer Bias 1
           'ABXY-TI2S': {'wfunc': 'ABXY-TI2', 'value': 0.004, 'mode': 'S'},  # m/s2, XY-Accelerometer Bias 2
           'ABZ': {'wfunc': 'ABZ', 'value': 0.004, 'mode': 'S'},  # m/s2, Z-Accelerometer Bias
           'ASXY-TI1S': {'wfunc': 'ASXY-TI1', 'value': 0.0005, 'mode': 'S'},  # -, XY-Accelerometer Scale Factor 1
           'ASXY-TI2S': {'wfunc': 'ASXY-TI2', 'value': 0.0005, 'mode': 'S'},  # -, XY-Accelerometer Scale Factor 2
           'ASXY-TI3S': {'wfunc': 'ASXY-TI3', 'value': 0.0005, 'mode': 'S'},  # -, XY-Accelerometer Scale Factor 3
           'ASZ': {'wfunc': 'ASZ', 'value': 0.0005, 'mode': 'S'},  # -, Z-Accelerometer Scale Factor
           'MBXY-TI1S': {'wfunc': 'MBXY-TI1', 'value': 70., 'mode': 'S'},  # nT, XY-Magnetometer Bias 1
           'MBXY-TI2S': {'wfunc': 'MBXY-TI2', 'value': 70., 'mode': 'S'},  # nT, XY-Magnetometer Bias 2
           'MBZ': {'wfunc': 'MBZ', 'value': 70., 'mode': 'S'},  # nT, Z-Magnetometer Bias
           'MSXY-TI1S': {'wfunc': 'MSXY-TI1', 'value': 0.0016, 'mode': 'S'},  # -, XY-Magnetometer Scale Factor 1
           'MSXY-TI2S': {'wfunc': 'MSXY-TI2', 'value': 0.0016, 'mode': 'S'},  # -, XY-Magnetometer Scale Factor 2
           'MSXY-TI3S': {'wfunc': 'MSXY-TI3', 'value': 0.0016, 'mode': 'S'},  # -, XY-Magnetometer Scale Factor 3
           'MSZ': {'wfunc': 'MSZ', 'value': 0.0016, 'mode': 'S'},  # -, Z-Magnetometer Scale Factor
           # declination error terms
           'DECG': {'wfunc': 'AZ', 'value': 0.36*pi/180, 'mode': 'G'},  # rad, Global Declination Constant Error
           'DBHG': {'wfunc': 'DBH', 'value': 5000.*pi/180, 'mode': 'G'},  # rad, Global Declination Var Error
           'DECR': {'wfunc': 'AZ', 'value': 0.1*pi/180, 'mode': 'R'},  # rad, Random Declination Constant Error
           'DBHR': {'wfunc': 'DBH', 'value': 3000.*pi/180, 'mode': 'R'},  # rad, Random Declination Var Error
           # axial drillstring interference error terms
           'AMIL': {'wfunc': 'AMIL', 'value': 220., 'mode': 'S'},  # nT, Axial DSI Constant Error
           # misalignment error terms
           'SAG': {'wfunc': 'SAG', 'value': 0.08*pi/180, 'mode': 'S'},  # rad, BHA Sag
           'XYM1': {'wfunc': 'XYM1', 'value': 0.1*pi/180, 'mode': 'S'},  # rad, XY-Axis Misalignment 1
           'XYM2': {'wfunc': 'XYM2', 'value': 0.1*pi/180, 'mode': 'S'},  # rad, XY-Axis Misalignment 2
           'XYM3': {'wfunc': 'XYM3', 'value': 0.1*pi/180, 'mode': 'S'},  # rad, XY-Axis Misalignment 3
           'XYM4': {'wfunc': 'XYM4', 'value': 0.1*pi/180, 'mode': 'S'},  # rad, XY-Axis Misalignment 4
        }

mwdstd4_sag_mis_hd = {
           # depth error terms
           'DRFR': {'wfunc': 'DREF', 'value': 0.35, 'mode': 'R'},  # m, Depth: Depth Reference - Random
           'DSFS': {'wfunc': 'DSF', 'value': 0.00056, 'mode': 'S'},  # -, Depth: Depth Scale Factor - Systematic
           'DSTG': {'wfunc': 'DST', 'value': 0.00000022, 'mode': 'G'},  # 1/m, Depth: Depth Stretch - Global
           # sensors' error terms
           'ABXY-TI1S': {'wfunc': 'ABXY-TI1', 'value': 0.004, 'mode': 'S'},  # m/s2, XY-Accelerometer Bias 1
           'ABXY-TI2S': {'wfunc': 'ABXY-TI2', 'value': 0.004, 'mode': 'S'},  # m/s2, XY-Accelerometer Bias 2
           'ABZ': {'wfunc': 'ABZ', 'value': 0.004, 'mode': 'S'},  # m/s2, Z-Accelerometer Bias
           'ASXY-TI1S': {'wfunc': 'ASXY-TI1', 'value': 0.0005, 'mode': 'S'},  # -, XY-Accelerometer Scale Factor 1
           'ASXY-TI2S': {'wfunc': 'ASXY-TI2', 'value': 0.0005, 'mode': 'S'},  # -, XY-Accelerometer Scale Factor 2
           'ASXY-TI3S': {'wfunc': 'ASXY-TI3', 'value': 0.0005, 'mode': 'S'},  # -, XY-Accelerometer Scale Factor 3
           'ASZ': {'wfunc': 'ASZ', 'value': 0.0005, 'mode': 'S'},  # -, Z-Accelerometer Scale Factor
           'MBXY-TI1S': {'wfunc': 'MBXY-TI1', 'value': 70., 'mode': 'S'},  # nT, XY-Magnetometer Bias 1
           'MBXY-TI2S': {'wfunc': 'MBXY-TI2', 'value': 70., 'mode': 'S'},  # nT, XY-Magnetometer Bias 2
           'MBZ': {'wfunc': 'MBZ', 'value': 70., 'mode': 'S'},  # nT, Z-Magnetometer Bias
           'MSXY-TI1S': {'wfunc': 'MSXY-TI1', 'value': 0.0016, 'mode': 'S'},  # -, XY-Magnetometer Scale Factor 1
           'MSXY-TI2S': {'wfunc': 'MSXY-TI2', 'value': 0.0016, 'mode': 'S'},  # -, XY-Magnetometer Scale Factor 2
           'MSXY-TI3S': {'wfunc': 'MSXY-TI3', 'value': 0.0016, 'mode': 'S'},  # -, XY-Magnetometer Scale Factor 3
           'MSZ': {'wfunc': 'MSZ', 'value': 0.0016, 'mode': 'S'},  # -, Z-Magnetometer Scale Factor
           # declination error terms
           'DECG': {'wfunc': 'AZ', 'value': 0.15*pi/180, 'mode': 'G'},  # rad, Global Declination Constant Error
           'DBHG': {'wfunc': 'DBH', 'value': 2059.*pi/180, 'mode': 'G'},  # rad, Global Declination Var Error
           'DECR': {'wfunc': 'AZ', 'value': 0.1*pi/180, 'mode': 'R'},  # rad, Random Declination Constant Error
           'DBHR': {'wfunc': 'DBH', 'value': 3000.*pi/180, 'mode': 'R'},  # rad, Random Declination Var Error
           # axial drillstring interference error terms
           'AMIL': {'wfunc': 'AMIL', 'value': 220., 'mode': 'S'},  # nT, Axial DSI Constant Error
           # misalignment error terms
           'SAG': {'wfunc': 'SAG', 'value': 0.06*pi/180, 'mode': 'S'},  # rad, BHA Sag
           'XYM1': {'wfunc': 'XYM1', 'value': 0.04*pi/180, 'mode': 'S'},  # rad, XY-Axis Misalignment 1
           'XYM2': {'wfunc': 'XYM2', 'value': 0.04*pi/180, 'mode': 'S'},  # rad, XY-Axis Misalignment 2
           'XYM3': {'wfunc': 'XYM3', 'value': 0.04*pi/180, 'mode': 'S'},  # rad, XY-Axis Misalignment 3
           'XYM4': {'wfunc': 'XYM4', 'value': 0.04*pi/180, 'mode': 'S'},  # rad, XY-Axis Misalignment 4
        }
