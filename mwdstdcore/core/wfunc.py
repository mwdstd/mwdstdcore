import numpy as np
from math import sqrt, cos, sin, tan, atan, pi, radians as deg2rad
from .reginc import reginc


def wfunc(e: str, md=0., tvd=0., inc=0., az=0., tf=0., dec=0., grid=0., g=9.81, b=50000., d=deg2rad(70.),
          lat=deg2rad(60.), noise_reduction_factor=1.):
    earth_rate = 15.041
    az_t = az + grid
    az_m = az_t - dec
    dpdr = np.zeros((3, 1))

    # regularize inclination and azimuth
    [inc, az_m] = reginc(inc, az_m)

    # depth error terms
    if e == 'DREF':
        dpdr[0, 0] = 1
    elif e == 'DSF':
        dpdr[0, 0] = md
    elif e == 'DST':
        dpdr[0, 0] = md * tvd
    # MWD STD rev 0 sensors' error terms
    elif e == 'ABX' or e == 'AFX':
        dpdr[1, 0] = -cos(inc) * sin(tf) / g
        dpdr[2, 0] = ((cos(inc) * sin(az_m) * sin(tf) - cos(az_m) * cos(tf)) * tan(d) + cos(tf) / tan(inc)) / g
    elif e == 'ABY' or e == 'AFY':
        dpdr[1, 0] = -cos(inc) * cos(tf) / g
        dpdr[2, 0] = ((cos(inc) * sin(az_m) * cos(tf) + cos(az_m) * sin(tf)) * tan(d) - sin(tf) / tan(inc)) / g
    elif e == 'ABZ' or e == 'AFZ':
        dpdr[1, 0] = -sin(inc) / g
        dpdr[2, 0] = tan(d) * sin(inc) * sin(az_m) / g
    elif e == 'ASX':
        dpdr[1, 0] = sin(inc) * cos(inc) * sin(tf) * sin(tf)
        dpdr[2, 0] = -sin(tf) * (tan(d) * sin(inc) * (cos(inc) * sin(az_m) * sin(tf) - cos(az_m) *
                                                      cos(tf)) + cos(inc) * cos(tf))
    elif e == 'ASY':
        dpdr[1, 0] = sin(inc) * cos(inc) * cos(tf) * cos(tf)
        dpdr[2, 0] = -cos(tf) * (tan(d) * sin(inc) * (cos(inc) * sin(az_m) * cos(tf) + cos(az_m) *
                                                      sin(tf)) - cos(inc) * sin(tf))
    elif e == 'ASZ':
        dpdr[1, 0] = -sin(inc) * cos(inc)
        dpdr[2, 0] = tan(d) * sin(inc) * cos(inc) * sin(az_m)
    elif e == 'MBX' or e == 'MFX':
        dpdr[2, 0] = (cos(az_m) * cos(tf) - cos(inc) * sin(az_m) * sin(tf)) / (b * cos(d))
    elif e == 'MBY' or e == 'MFY':
        dpdr[2, 0] = -(cos(az_m) * sin(tf) + cos(inc) * sin(az_m) * cos(tf)) / (b * cos(d))
    elif e == 'MBZ' or e == 'MFZ':
        dpdr[2, 0] = -sin(inc) * sin(az_m) / (b * cos(d))
    elif e == 'MSX':
        dpdr[2, 0] = ((cos(inc) * cos(az_m) * sin(tf) - tan(d) * sin(inc) * sin(tf) + sin(az_m) * cos(tf)) *
                      (cos(az_m) * cos(tf) - cos(inc) * sin(az_m) * sin(tf)))
    elif e == 'MSY':
        dpdr[2, 0] = -((cos(inc) * cos(az_m) * cos(tf) - tan(d) * sin(inc) * cos(tf) - sin(az_m) * sin(tf)) *
                       (cos(az_m) * sin(tf) + cos(inc) * sin(az_m) * cos(tf)))
    elif e == 'MSZ':
        dpdr[2, 0] = -(sin(inc) * cos(az_m) + tan(d) * cos(inc)) * sin(inc) * sin(az_m)
    # axial drillstring interference error terms
    elif e == 'AMIL':
        dpdr[2, 0] = sin(inc) * sin(az_m) / (b * cos(d))
    elif e == 'AMID':
        dpdr[2, 0] = sin(inc) * sin(az_m)
    # misalignment error terms
    elif e == 'SAG':
        dpdr[1, 0] = sin(inc)
    elif e == 'MX':
        dpdr[1, 0] = sin(tf)
        dpdr[2, 0] = -cos(tf) / sin(inc)
    elif e == 'MY':
        dpdr[1, 0] = cos(tf)
        dpdr[2, 0] = sin(tf) / sin(inc)
    # misalignment between magnetometer and accelerometer frames: one twist and two bends
    elif e == 'MXY':
        # twist
        da_dbx = (cos(az_m) * cos(tf) - cos(inc) * sin(az_m) * sin(tf)) / (b * cos(d))
        da_dby = -(cos(az_m) * sin(tf) + cos(inc) * sin(az_m) * cos(tf)) / (b * cos(d))
        by = (b * (cos(d) * cos(inc) * cos(az) * cos(tf) - sin(d) * sin(inc) * cos(tf) - cos(d) * sin(az) * sin(tf)))
        bx = (-b * (cos(d) * cos(inc) * cos(az) * sin(tf) - sin(d) * sin(inc) * sin(tf) + cos(d) * sin(az) * cos(tf)))

        dpdr[2, 0] = da_dbx * by - da_dby * bx
    elif e == 'MXZ':
        # X axis bend
        da_dbx = (cos(az_m) * cos(tf) - cos(inc) * sin(az_m) * sin(tf)) / (b * cos(d))
        da_dbz = -sin(inc) * sin(az_m) / (b * cos(d))
        bx = (-b * (cos(d) * cos(inc) * cos(az) * sin(tf) - sin(d) * sin(inc) * sin(tf) + cos(d) * sin(az) * cos(tf)))
        bz = (b * (cos(d) * sin(inc) * cos(az) + sin(d) * cos(inc)))

        dpdr[2, 0] = da_dbx * bz - da_dbz * bx
    elif e == 'MYZ':
        # Y axis bend
        da_dby = -(cos(az_m) * sin(tf) + cos(inc) * sin(az_m) * cos(tf)) / (b * cos(d))
        da_dbz = -sin(inc) * sin(az_m) / (b * cos(d))
        by = (b * (cos(d) * cos(inc) * cos(az) * cos(tf) - sin(d) * sin(inc) * cos(tf) - cos(d) * sin(az) * sin(tf)))
        bz = (b * (cos(d) * sin(inc) * cos(az) + sin(d) * cos(inc)))

        dpdr[2, 0] = da_dby * bz - da_dbz * by
    # declination error terms
    elif e == 'AZ':
        dpdr[2, 0] = 1.0
    elif e == 'DBH':
        dpdr[2, 0] = 1.0 / (b * cos(d))
    # toolface independent error terms
    # sensors
    elif e == 'ABXY-TI1':
        dpdr[1, 0] = -cos(inc) / g
        dpdr[2, 0] = (tan(d) * cos(inc) * sin(az_m)) / g
    elif e == 'ABXY-TI2':
        dpdr[2, 0] = ((tan((pi / 2.0) - inc)) - tan(d) * cos(az_m)) / g
    elif e == 'ASXY-TI1':
        dpdr[1, 0] = sin(inc) * cos(inc) / sqrt(2.0)
        dpdr[2, 0] = (-tan(d) * sin(inc) * cos(inc) * sin(az_m)) / sqrt(2.0)
    elif e == 'ASXY-TI2':
        dpdr[1, 0] = sin(inc) * cos(inc) / 2.0
        dpdr[2, 0] = (-tan(d) * sin(inc) * cos(inc) * sin(az_m)) / 2.0
    elif e == 'ASXY-TI3':
        dpdr[2, 0] = (tan(d) * sin(inc) * cos(az_m) - cos(inc)) / 2.0
    elif e == 'MBXY-TI1':
        dpdr[2, 0] = -cos(inc) * sin(az_m) / (b * cos(d))
    elif e == 'MBXY-TI2':
        dpdr[2, 0] = cos(az_m) / (b * cos(d))
    elif e == 'MSXY-TI1':
        dpdr[2, 0] = sin(inc) * sin(az_m) * (tan(d) * cos(inc) + sin(inc) * cos(az_m)) / sqrt(2.0)
    elif e == 'MSXY-TI2':
        dpdr[2, 0] = sin(az_m) * (tan(d) * sin(inc) * cos(inc) - cos(inc) * cos(inc) * cos(az_m) - cos(az_m)) / 2.0
    elif e == 'MSXY-TI3':
        dpdr[2, 0] = (cos(inc) * cos(az_m) * cos(az_m) - cos(inc) * sin(az_m) * sin(az_m) -
                      tan(d) * sin(inc) * cos(az_m)) / 2.0
    # misalignment
    elif e == 'XYM1':
        dpdr[1, 0] = abs(sin(inc))
    elif e == 'XYM2':
        dpdr[2, 0] = -1.0
    elif e == 'XYM3':
        dpdr[1, 0] = abs(cos(inc)) * cos(az_m)
        dpdr[2, 0] = -(abs(cos(inc)) * sin(az_m)) / sin(inc)
    elif e == 'XYM4':
        dpdr[1, 0] = abs(cos(inc)) * sin(az_m)
        dpdr[2, 0] = (abs(cos(inc)) * cos(az_m)) / sin(inc)
    # error terms affected by DSI single station correction
    elif e == 'ABIX':
        dpdr[1, 0] = -cos(inc) * sin(tf) / g
        dpdr[2, 0] = ((cos(inc) * cos(inc) * sin(az_m) * sin(tf) * (tan(d) * cos(inc) + sin(inc) * cos(az_m)) - cos(tf) *
                      (tan(d) * cos(az_m) - tan(pi / 2.0 - inc))) /
                      (1.0 - sin(inc) * sin(inc) * sin(az_m) * sin(az_m)) / g)
    elif e == 'ABIY':
        dpdr[1, 0] = -cos(inc) * cos(tf) / g
        dpdr[2, 0] = ((cos(inc) * cos(inc) * sin(az_m) * cos(tf) * (tan(d) * cos(inc) + sin(inc) * cos(az_m)) + sin(tf) *
                      (tan(d) * cos(az_m) - 1.0 / tan(inc))) / (1.0 - sin(inc) * sin(inc) * sin(az_m) * sin(az_m)) / g)
    elif e == 'ABIZ':
        dpdr[1, 0] = -sin(inc) / g
        dpdr[2, 0] = ((sin(inc) * cos(inc) * sin(az_m) * (tan(d) * cos(inc) + sin(inc) * cos(az_m))) /
                      (1.0 - sin(inc) * sin(inc) * sin(az_m) * sin(az_m)) / g)
    elif e == 'ASIX':
        dpdr[1, 0] = sin(inc) * cos(inc) * sin(tf) * sin(tf)
        dpdr[2, 0] = -(sin(tf) * (sin(inc) * cos(inc) * cos(inc) * sin(az_m) * sin(tf) *
                                  (tan(d) * cos(inc) + sin(inc) * cos(az_m)) - cos(tf) *
                                  (tan(d) * sin(inc) * cos(az_m) - cos(inc))) /
                       (1.0 - sin(inc) * sin(inc) * sin(az_m) * sin(az_m)))
    elif e == 'ASIY':
        dpdr[1, 0] = sin(inc) * cos(inc) * cos(tf) * cos(tf)
        dpdr[2, 0] = -cos(tf) * (sin(inc) * cos(inc) * cos(inc) * sin(az_m) * cos(tf) *
                                (tan(d) * cos(inc) + sin(inc) * cos(az_m)) + sin(tf) *
                                (tan(d) * sin(inc) * cos(az_m) - cos(inc))) / \
                     (1.0 - sin(inc) * sin(inc) * sin(az_m) * sin(az_m))
    elif e == 'ASIZ':
        dpdr[1, 0] = -sin(inc) * cos(inc)
        dpdr[2, 0] = sin(inc) * cos(inc) * cos(inc) * sin(az_m) * (tan(d) * cos(inc) + sin(inc) * cos(az_m)) / \
            (1.0 - sin(inc) * sin(inc) * sin(az_m) * sin(az_m))
    elif e == 'MBIX':
        dpdr[2, 0] = -(cos(inc) * sin(az_m) * sin(tf) - cos(az_m) * cos(tf)) / b / cos(d) / \
                  (1.0 - sin(inc) * sin(inc) * sin(az_m) * sin(az_m))
    elif e == 'MBIY':
        dpdr[2, 0] = -(cos(inc) * sin(az_m) * cos(tf) + cos(az_m) * sin(tf)) / b / cos(d) / \
                  (1.0 - sin(inc) * sin(inc) * sin(az_m) * sin(az_m))
    elif e == 'MSIX':
        dpdr[2, 0] = -(cos(inc) * cos(az_m) * sin(tf) - tan(d) * sin(inc) * sin(tf) + sin(az_m) * cos(tf)) * \
                  (cos(inc) * sin(az_m) * sin(tf) - cos(az_m) * cos(tf)) / \
                  (1.0 - sin(inc) * sin(inc) * sin(az_m) * sin(az_m))
    elif e == 'MSIY':
        dpdr[2, 0] = -(cos(inc) * cos(az_m) * cos(tf) - tan(d) * sin(inc) * cos(tf) - sin(az_m) * sin(tf)) * \
                  (cos(inc) * sin(az_m) * cos(tf) + cos(az_m) * sin(tf)) / \
                  (1.0 - sin(inc) * sin(inc) * sin(az_m) * sin(az_m))
    elif e == 'MDI':
        dpdr[2, 0] = -sin(inc) * sin(az_m) * (cos(inc) - tan(d) * sin(inc) * cos(az_m)) / \
                  (1.0 - sin(inc) * sin(inc) * sin(az_m) * sin(az_m))
    elif e == 'MFI' or e == 'MBI':
        dpdr[2, 0] = -sin(inc) * sin(az_m) * (tan(d) * cos(inc) + sin(inc) * cos(az_m)) / \
                  (1.0 - sin(inc) * sin(inc) * sin(az_m) * sin(az_m)) / b
    # toolface independent error terms affected by DSI single station correction
    elif e == 'ABIXY-TI1':
        dpdr[1, 0] = -cos(inc) / g
        dpdr[2, 0] = (cos(inc) * cos(inc) * sin(az_m) * (tan(d) * cos(inc) + sin(inc) * cos(az_m))) / \
                  (g * (1.0 - sin(inc) * sin(inc) * sin(az_m) * sin(az_m)))
    elif e == 'ABIXY-TI2':
        dpdr[1, 0] = 0.0
        dpdr[2, 0] = -(tan(d) * cos(az_m) - tan(pi / 2.0 - inc)) / \
                   (g * (1.0 - sin(inc) * sin(inc) * sin(az_m) * sin(az_m)))
    elif e == 'ASIXY-TI1':
        dpdr[1, 0] = sin(inc) * cos(inc) / sqrt(2.0)
        dpdr[2, 0] = -(sin(inc) * cos(inc) * cos(inc) * sin(az_m) * (tan(d) * cos(inc) + sin(inc) * cos(az_m))) / \
                   (sqrt(2.0) * (1.0 - sin(inc) * sin(inc) * sin(az_m) * sin(az_m)))
    elif e == 'ASIXY-TI2':
        dpdr[1, 0] = sin(inc) * cos(inc) / 2.0
        dpdr[2, 0] = -(sin(inc) * cos(inc) * cos(inc) * sin(az_m) * (tan(d) * cos(inc) + sin(inc) * cos(az_m))) / \
                   (2.0 * (1.0 - sin(inc) * sin(inc) * sin(az_m) * sin(az_m)))
    elif e == 'ASIXY-TI3':
        dpdr[2, 0] = (tan(d) * sin(inc) * cos(az_m) - cos(inc)) / \
                  (2.0 * (1.0 - sin(inc) * sin(inc) * sin(az_m) * sin(az_m)))
    elif e == 'MBIXY-TI1':
        dpdr[2, 0] = -cos(inc) * sin(az_m) / (b * cos(d) * (1.0 - sin(inc) * sin(inc) * sin(az_m) * sin(az_m)))
    elif e == 'MBIXY-TI2':
        dpdr[2, 0] = cos(az_m) / (b * cos(d) * (1.0 - sin(inc) * sin(inc) * sin(az_m) * sin(az_m)))
    elif e == 'MSIXY-TI1':
        dpdr[2, 0] = sin(inc) * sin(az_m) * (tan(d) * cos(inc) + sin(inc) * cos(az_m)) / \
                  (sqrt(2.0) * (1.0 - sin(inc) * sin(inc) * sin(az_m) * sin(az_m)))
    elif e == 'MSIXY-TI2':
        dpdr[2, 0] = sin(az_m) * (tan(d) * sin(inc) * cos(inc) - cos(inc) * cos(inc) * cos(az_m) - cos(az_m)) / \
                  (2.0 * (1.0 - sin(inc) * sin(inc) * sin(az_m) * sin(az_m)))
    elif e == 'MSIXY-TI3':
        dpdr[2, 0] = (cos(inc) * cos(az_m) * cos(az_m) - cos(inc) * sin(az_m) * sin(az_m) - tan(d) * sin(inc) *
                   cos(az_m)) / (2.0 * (1.0 - sin(inc) * sin(inc) * sin(az_m) * sin(az_m)))
    # error terms for unknown error model
    elif e == 'CNI':
        dpdr[1, 0] = 1.0
    elif e == 'CNA':
        dpdr[2, 0] = 1.0 / sin(inc)
    # DMS error terms
    elif e == 'ASXD':
        dpdr[1, 0] = sin(inc) * cos(inc) / 2.0
        dpdr[2, 0] = -sin(inc) * cos(inc) * sin(az_m) * tan(d) / 2.0
    elif e == 'ASYD':
        dpdr[1, 0] = sin(inc) * cos(inc) / 2.0
        dpdr[2, 0] = -sin(inc) * cos(inc) * sin(az_m) * tan(d) / 2.0
    elif e == 'MSXD':
        bxy = b * sqrt(1 - (cos(d) * sin(inc) * cos(az_m) + sin(d) * cos(inc)) ** 2)
        x = atan(sin(az_m) / (sin(inc) * tan(d) - cos(inc) * cos(az_m)))
        dpdr[2, 0] = -bxy * (cos(az_m) * sin(x) + cos(inc) * sin(az_m) * cos(x)) / (2 * b * cos(d))
    elif e == 'MSYD':
        bxy = b * sqrt(1 - (cos(d) * sin(inc) * cos(az_m) + sin(d) * cos(inc)) ** 2)
        x = atan(sin(az_m) / (sin(inc) * tan(d) - cos(inc) * cos(az_m)))
        dpdr[2, 0] = -bxy * (cos(az_m) * sin(x) + cos(inc) * sin(az_m) * cos(x)) / (2 * b * cos(d))
    # frequency response and eddy current effect
    elif e == 'AAXY':
        dpdr[1, 0] = sin(inc) * cos(inc)
        dpdr[2, 0] = -sin(inc) * cos(inc) * sin(az_m) * tan(d)
    elif e == 'AMXY':
        dpdr[2, 0] = (1 - cos(inc) * cos(inc)) * sin(az_m) * cos(az_m) + sin(inc) * cos(inc) * sin(az_m) * tan(d)
    elif e == 'PSD':
        dpdr[2, 0] = (cos(inc) - sin(inc) * cos(az_m) * tan(d)) / sin(inc)
    elif e == 'EDDY':
        dpdr[2, 0] = cos(inc) - sin(inc) * cos(az_m) * tan(d)
    # downhole noise and centripetal acceleration
    elif e == 'AN1':
        dpdr[2, 0] = (1.0 / tan(inc) - cos(az_m) * tan(d)) / g
    elif e == 'AN2':
        dpdr[1, 0] = -cos(inc) / g
        dpdr[2, 0] = cos(inc) * sin(az_m) * tan(d) / g
    elif e == 'ANZ':
        dpdr[1, 0] = -sin(inc) / g
        dpdr[2, 0] = sin(inc) * sin(az_m) * tan(d) / g
    elif e == 'CA1':
        dpdr[2, 0] = (1 / tan(inc) - cos(az_m) * tan(d)) / g
    elif e == 'CA2':
        dpdr[1, 0] = -cos(inc) / g
        dpdr[2, 0] = cos(inc) * sin(az_m) * tan(d) / g
    # signal delay compensation error
    elif e == 'DSC':
        dpdr[1, 0] = 1
        dpdr[2, 0] = 1 / sin(inc)
    # Gyro error terms
    elif e == 'AXYZ-XYB':  # equal to ABZ
        dpdr[1, 0] = cos(inc) / g
    elif e == 'AXYZ-ZB':  # equal to ABZ
        dpdr[1, 0] = sin(inc) / g
    elif e == 'AXYZ-SF':
        dpdr[1, 0] = 1.3 * sin(inc) * cos(inc)
    elif e == 'AXYZ-MIS':
        dpdr[1, 0] = 1
    elif e == 'GXYZ-XYB1':
        dpdr[2, 0] = sin(az_t) * cos(inc) / (earth_rate * cos(lat))
    elif e == 'GXYZ-XYB2':
        dpdr[2, 0] = cos(az_t) / (earth_rate * cos(lat))
    elif e == 'GXYZ-XYRN':
        dpdr[2, 0] = noise_reduction_factor * sqrt(1 - sin(az_t) ** 2 * sin(inc) ** 2) / (earth_rate * cos(lat))
    elif e == 'GXYZ-XYG1':
        dpdr[2, 0] = cos(az_t) * sin(inc) / (earth_rate * cos(lat))
    elif e == 'GXYZ-XYG4':
        dpdr[2, 0] = sin(az_t) * sin(inc) * cos(inc) / (earth_rate * cos(lat))
    elif e == 'GXYZ-ZB':
        dpdr[2, 0] = sin(az_t) * sin(inc) / (earth_rate * cos(lat))
    elif e == 'GXYZ-ZRN':
        dpdr[2, 0] = sin(az_t) * sin(inc) / (earth_rate * cos(lat))
    elif e == 'GXYZ-ZG1':
        dpdr[2, 0] = sin(az_t) * sin(inc) * sin(inc) / (earth_rate * cos(lat))
    elif e == 'GXYZ-ZG2':
        dpdr[2, 0] = sin(az_t) * sin(inc) * cos(inc) / (earth_rate * cos(lat))
    # Legacy gyro (singularity)
    elif e == 'GXY-B1':  # singularity at inclination of 90 deg and poles
        dpdr[2, 0] = sin(az_t) / (earth_rate * cos(lat) * cos(inc))
    elif e == 'GXY-B2':  # singularity at poles
        dpdr[2, 0] = cos(az_t) / (earth_rate * cos(lat))
    elif e == 'GXY-G1':  # singularity at poles
        dpdr[2, 0] = cos(az_t) * sin(inc) / (earth_rate * cos(lat))
    elif e == 'GXY-G4':  # singularity at inclination of 90 def and poles
        dpdr[2, 0] = sin(az_t) * tan(inc) / (earth_rate * cos(lat))
    elif e == 'GXY-RN':  # singularity at inclination of 90 deg and poles
        dpdr[2, 0] = noise_reduction_factor * sqrt(1 - cos(az_t) ** 2 * sin(inc) ** 2) / (earth_rate * cos(lat) * cos(inc))
    # error terms for single station correction of axial interference
    elif e == 'ABIX':
        dpdr[1, 0] = -cos(inc) * sin(tf) / g
        dpdr[2, 0] = (cos(inc) ** 2 * sin(az_m) * sin(tf) * (tan(d) * cos(inc) + sin(inc) * cos(az_m)) -
                   cos(tf) * (tan(d) * cos(az_m) - 1 / tan(inc))) / (1 - sin(inc) ** 2 * sin(az_m) ** 2)
    elif e == 'ABIY':
        dpdr[1, 0] = -cos(inc) * cos(tf) / g
        dpdr[2, 0] = (cos(inc) ** 2 * sin(az_m) * cos(tf) * (tan(d) * cos(inc) + sin(inc) * cos(az_m)) +
                   sin(tf) * (tan(d) * cos(az_m) - 1 / tan(inc))) / (1 - sin(inc) ** 2 * sin(az_m) ** 2)
    elif e == 'ABIZ':
        dpdr[1, 0] = -sin(inc) / g
        dpdr[2, 0] = (sin(inc) * cos(inc) * sin(az_m) * (tan(d) * cos(inc) + sin(inc) * cos(az_m))) / \
                  (1 - sin(inc) ** 2 * sin(az_m) ** 2)
    elif e == 'ASIX':
        dpdr[1, 0] = sin(inc) * cos(inc) * sin(tf) ** 2
        dpdr[2, 0] = -sin(tf) * (sin(inc) * cos(inc) ** 2 * sin(az_m) * sin(tf) *
                              (tan(d) * cos(inc) + sin(inc) * cos(az_m)) - cos(tf) *
                              (tan(d) * sin(inc) * cos(az_m) - cos(inc))) / (1 - sin(inc) ** 2 * sin(az_m) ** 2)
    elif e == 'ASIY':
        dpdr[1, 0] = sin(inc) * cos(inc) * cos(tf) ** 2
        dpdr[2, 0] = -cos(tf) * (sin(inc) * cos(inc) ** 2 * sin(az_m) * cos(tf) *
                              (tan(d) * cos(inc) + sin(inc) * cos(az_m)) + sin(tf) *
                              (tan(d) * sin(inc) * cos(az_m) - cos(inc))) / (1 - sin(inc) ** 2 * sin(az_m) ** 2)
    elif e == 'ASIZ':
        dpdr[1, 0] = -sin(inc) * cos(inc)
        dpdr[2, 0] = sin(inc) * cos(inc) ** 2 * sin(az_m) * (tan(d) * cos(inc) + sin(inc) * cos(az_m)) / \
                  (1 - sin(inc) ** 2 * sin(az_m) ** 2)
    elif e == 'MBIX':
        dpdr[2, 0] = -(cos(inc) * sin(az_m) * sin(tf) - cos(az_m) * cos(tf)) / \
                  ((1 - sin(inc) ** 2 * sin(az_m) ** 2) * b * cos(d))
    elif e == 'MBIY':
        dpdr[2, 0] = -(cos(inc) * sin(az_m) * cos(tf) + cos(az_m) * sin(tf)) / \
                  ((1 - sin(inc) ** 2 * sin(az_m) ** 2) * b * cos(d))
    elif e == 'MSIX':
        dpdr[2, 0] = -(cos(inc) * cos(az_m) * sin(tf) - tan(d) * sin(inc) * sin(tf) + sin(az_m) * cos(tf)) * \
                  (cos(inc) * sin(az_m) * sin(tf) - cos(az_m) * cos(tf)) / (1 - sin(inc) ** 2 * sin(az_m) ** 2)
    elif e == 'MSIY':
        dpdr[2, 0] = -(cos(inc) * cos(az_m) * cos(tf) - tan(d) * sin(inc) * cos(tf) - sin(az_m) * sin(tf)) * \
                  (cos(inc) * sin(az_m) * cos(tf) + cos(az_m) * sin(tf)) / (1 - sin(inc) ** 2 * sin(az_m) ** 2)
    # Axial magnetic interference
    elif e == 'MBI':
        dpdr[2, 0] = -sin(inc) * sin(az_m) * (tan(d) * cos(inc) + sin(inc) * cos(az_m)) / \
                  (b * (1 - sin(inc) ** 2 * sin(az_m) ** 2))
    elif e == 'MDI':
        dpdr[2, 0] = -sin(inc) * sin(az_m) * (cos(inc) - tan(d) * sin(inc) * cos(az_m)) / \
                  (1 - sin(inc) ** 2 * sin(az_m) ** 2)
    return dpdr
