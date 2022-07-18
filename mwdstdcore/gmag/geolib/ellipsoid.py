from math import sqrt


class Ellipsoid:
    # Sets WGS - 84 parameters
    a = 6378.137
    b = 6356.7523142
    fla = 1. / 298.257223563
    eps = sqrt(1. - (b * b) / (a * a))
    epssq = eps * eps
    re = 6371.2
