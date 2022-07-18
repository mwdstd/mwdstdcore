from typing import Tuple
from math import radians as deg2rad, degrees as rad2deg, pi, sin, cos, atan2, sqrt, exp, atanh, acos, atan, fabs
from .geoidcoord import CoordGeodetic
from .sphcoord import CoordSpherical
from .ellipsoid import Ellipsoid


UTM_MIN_LAT_DEGREE = -80.5
UTM_MAX_LAT_DEGREE = 84.5

PS_MAX_LAT_DEGREE = 55.0
PS_MIN_LAT_DEGREE = -55.0


class UTMParameters:
    def __init__(self):
        self.Easting = 0.
        self.Northing = 0.
        self.Zone = 0
        self.HemiSphere = ''
        self.CentralMeridian = 0.
        self.ConvergenceOfMeridians = 0.
        self.PointScale = 0.

    def get_transverse_mercator(self, geodetic_coords: CoordGeodetic):
        Lambda = deg2rad(geodetic_coords.Lambda)
        Phi = deg2rad(geodetic_coords.Phi)

        [Zone, Hemisphere, Lam0] = UTMParameters.get_utm_parameters(Phi, Lambda)
        K0 = 0.9996
        if Hemisphere == 'n' or Hemisphere == 'N':
            falseN = 0
        else:
            falseN = 10000000
        if Hemisphere == 's' or Hemisphere == 'S':
            falseN = 10000000
        else:
            falseN = 0
        falseE = 500000

        Eps = 0.081819190842621494335
        Epssq = 0.0066943799901413169961
        K0R4 = 6367449.1458234153093 * K0
        K0R4oa = K0R4 / 6378137

        Acoeff = [8.37731820624469723600E-04, 7.60852777357248641400E-07, 1.19764550324249124400E-09,
                  2.42917068039708917100E-12, 5.71181837042801392800E-15, 1.47999793137966169400E-17,
                  4.10762410937071532000E-20, 1.21078503892257704200E-22]

        XYonly = 0

        [X, Y, pscale, CoM] = UTMParameters.tm_fwd4(Eps, Epssq, K0R4, K0R4oa, Acoeff, Lam0, K0, falseE, falseN,  XYonly,
                                                    Lambda, Phi)

        self.Easting = X
        self.Northing = Y
        self.Zone = Zone
        self.HemiSphere = Hemisphere
        self.CentralMeridian = rad2deg(Lam0)
        self.ConvergenceOfMeridians = rad2deg(CoM)
        self.PointScale = pscale

    @staticmethod
    def get_utm_parameters(latitude: float, longitude: float) -> Tuple[int, str, float]:
        if latitude < deg2rad(UTM_MIN_LAT_DEGREE) or latitude > deg2rad(UTM_MAX_LAT_DEGREE):
            raise Exception('Class UTMParameters method get_utm_parameters: latitude out of range')

        if longitude < -pi or longitude > 2 * pi:
            raise Exception('Class UTMParameters method get_utm_parameters: longitude out of range')

        if longitude < 0:
            longitude += 2 * pi + 1.0e-10
        Lat_Degrees = int(rad2deg(latitude))
        Long_Degrees = int(rad2deg(longitude))

        if longitude < pi:
            temp_zone = int(31 + (rad2deg(longitude) / 6.0))
        else:
            temp_zone = int((rad2deg(longitude) / 6.0) - 29)

        if temp_zone > 60:
            temp_zone = 1

        if 55 < Lat_Degrees < 64 and -1 < Long_Degrees < 3:
            temp_zone = 31
        if 55 < Lat_Degrees < 64 and 2 < Long_Degrees < 12:
            temp_zone = 32
        if Lat_Degrees > 71 and -1 < Long_Degrees < 9:
            temp_zone = 31
        if Lat_Degrees > 71 and 8 < Long_Degrees < 21:
            temp_zone = 33
        if Lat_Degrees > 71 and 20 < Long_Degrees < 33:
            temp_zone = 35
        if Lat_Degrees > 71 and 32 < Long_Degrees < 42:
            temp_zone = 37

        if temp_zone >= 31:
            CentralMeridian = deg2rad(6 * temp_zone - 183)
        else:
            CentralMeridian = deg2rad(6 * temp_zone + 177)
        Zone = temp_zone
        if latitude < 0:
            Hemisphere = 'S'
        else:
            Hemisphere = 'N'

        return [Zone, Hemisphere, CentralMeridian]

    @staticmethod
    def tm_fwd4(Eps: float, Epssq: float, K0R4: float, K0R4oa: float, Acoeff: list, Lam0: float, K0: float,
                falseE: float, falseN: float, XYonly: int, Lambda: float, Phi: float) -> Tuple[float, float, float, float]:
        Lam = Lambda - Lam0
        CLam = cos(Lam)
        SLam = sin(Lam)

        # Latitude
        CPhi = cos(Phi)
        SPhi = sin(Phi)

        P = exp(Eps * atanh(Eps * SPhi))
        part1 = (1 + SPhi) / P
        part2 = (1 - SPhi) * P
        denom = 1 / (part1 + part2)
        CChi = 2 * CPhi * denom
        SChi = (part1 - part2) * denom

        T = CChi * SLam
        U = atanh(T)
        V = atan2(SChi, CChi * CLam)

        Tsq = T * T
        denom2 = 1 / (1 - Tsq)
        c2u = (1 + Tsq) * denom2
        s2u = 2 * T * denom2
        c2v = (-1 + CChi * CChi * (1 + CLam * CLam)) * denom2
        s2v = 2 * CLam * CChi * SChi * denom2

        c4u = 1 + 2 * s2u * s2u
        s4u = 2 * c2u * s2u
        c4v = 1 - 2 * s2v * s2v
        s4v = 2 * c2v * s2v

        c6u = c4u * c2u + s4u * s2u
        s6u = s4u * c2u + c4u * s2u
        c6v = c4v * c2v - s4v * s2v
        s6v = s4v * c2v + c4v * s2v

        c8u = 1 + 2 * s4u * s4u
        s8u = 2 * c4u * s4u
        c8v = 1 - 2 * s4v * s4v
        s8v = 2 * c4v * s4v

        Xstar = Acoeff[3] * s8u * c8v
        Xstar = Xstar + Acoeff[2] * s6u * c6v
        Xstar = Xstar + Acoeff[1] * s4u * c4v
        Xstar = Xstar + Acoeff[0] * s2u * c2v
        Xstar = Xstar + U

        Ystar = Acoeff[3] * c8u * s8v
        Ystar = Ystar + Acoeff[2] * c6u * s6v
        Ystar = Ystar + Acoeff[1] * c4u * s4v
        Ystar = Ystar + Acoeff[0] * c2u * s2v
        Ystar = Ystar + V

        X = K0R4 * Xstar + falseE
        Y = K0R4 * Ystar + falseN

        if XYonly == 1:
            pscale = K0
            CoM = 0
        else:
            sig1 = 8 * Acoeff[3] * c8u * c8v
            sig1 = sig1 + 6 * Acoeff[2] * c6u * c6v
            sig1 = sig1 + 4 * Acoeff[1] * c4u * c4v
            sig1 = sig1 + 2 * Acoeff[0] * c2u * c2v
            sig1 = sig1 + 1

            sig2 = 8 * Acoeff[3] * s8u * s8v
            sig2 = sig2 + 6 * Acoeff[2] * s6u * s6v
            sig2 = sig2 + 4 * Acoeff[1] * s4u * s4v
            sig2 = sig2 + 2 * Acoeff[0] * s2u * s2v

            comroo = sqrt((1 - Epssq * SPhi * SPhi) * denom2 * (sig1 * sig1 + sig2 * sig2))

            pscale = K0R4oa * 2 * denom * comroo
            CoM = atan2(SChi * SLam, CLam) + atan2(sig2, sig1)
        return [X, Y, pscale, CoM]

    @staticmethod
    def cartesian2geodetic(x: float, y: float, z: float) -> CoordGeodetic:
        if z < 0.0:
            modified_b = -Ellipsoid.b
        else:
            modified_b = Ellipsoid.b

        r = sqrt(x * x + y * y)
        e = (modified_b * z - (Ellipsoid.a ** 2 - modified_b * modified_b)) / (Ellipsoid.a * r)
        f = (modified_b * z + (Ellipsoid.a ** 2 - modified_b * modified_b)) / (Ellipsoid.a * r)

        p = (4.0 / 3.0) * (e * f + 1.0)
        q = 2.0 * (e * e - f * f)
        d = p ** 3 + q ** 2

        if d >= 0.0:
            v = pow((sqrt(d) - q), 1. / 3.) - pow((sqrt(d) + q), 1. / 3.)
        else:
            v = 2.0 * sqrt(-p) * cos(acos(q / (p * sqrt(-p))) / 3.)

        if v * v < fabs(p):
            v = -(v ** 3 + 2. * q) / (3. * p)

        g = (sqrt(e ** 2 + v) + e) / 2.
        t = sqrt(g ** 2 + (f - v * g) / (2. * g - e)) - g

        rlat = atan((Ellipsoid.a * (1.0 - t ** 2)) / (2. * modified_b * t))
        latitude = rad2deg(rlat)

        height_above_ellipsoid = (r - Ellipsoid.a * t) * cos(rlat) + (z - modified_b) * sin(rlat)

        zlong = atan2(y, x)
        if zlong < 0.0:
            zlong = zlong + 2 * pi

        longitude = rad2deg(zlong)
        while longitude > 180:
            longitude -= 360

        geodetic_coords = CoordGeodetic(latitude, longitude, height_above_ellipsoid, altitude_type='WGS-84')
        return geodetic_coords

    @staticmethod
    def spherical2cartesian(spherical_coords: CoordSpherical) -> Tuple[float, float, float]:
        rad_phi = deg2rad(spherical_coords.Phig)
        rad_lambda = deg2rad(spherical_coords.Lambda)
        x = spherical_coords.R * cos(rad_phi) * cos(rad_lambda)
        y = spherical_coords.R * cos(rad_phi) * sin(rad_lambda)
        z = spherical_coords.R * sin(rad_phi)
        return [x, y, z]

    @staticmethod
    def spherical2geodetic(spherical_coords: CoordSpherical) -> CoordGeodetic:
        [x, y, z] = UTMParameters.spherical2cartesian(spherical_coords)
        geodetic_coords = UTMParameters.cartesian2geodetic(x, y, z)
        return geodetic_coords
