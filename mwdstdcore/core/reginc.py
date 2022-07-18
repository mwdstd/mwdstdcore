from math import pi

phi = 1e-4


def reginc(inc: float, az_m: float = 0.):
    if inc == 0. or inc == pi / 2 or inc == -pi / 2:
        inc += phi

    if inc == pi / 2 and (az_m == pi / 2 or az_m == 3 * pi / 2):
        inc += phi
        az_m += phi
    return [inc, az_m]
