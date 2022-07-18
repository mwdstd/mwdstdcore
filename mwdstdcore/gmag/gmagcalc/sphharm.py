import numpy as np
from mwdstdcore.gmag.geolib.ellipsoid import Ellipsoid
from mwdstdcore.gmag.geolib.sphcoord import CoordSpherical
from mwdstdcore.gmag.maglib.magmod import MagneticModel
from math import sin, cos, radians as deg2rad


class SphericalHarmonicVariables:
    def __init__(self, mag_model: MagneticModel, spherical_coords: CoordSpherical):
        self.__n_max = mag_model.nMax
        self.RelativeRadiusPower = np.zeros(self.__n_max + 1)
        self.cos_mlambda = np.zeros(self.__n_max + 1)
        self.sin_mlambda = np.zeros(self.__n_max + 1)
        self.__compute(spherical_coords)

    def __compute(self, spherical_coords: CoordSpherical):
        n_max = self.__n_max
        cos_lambda = cos(deg2rad(spherical_coords.Lambda))
        sin_lambda = sin(deg2rad(spherical_coords.Lambda))
        self.RelativeRadiusPower[0] = (Ellipsoid.re / spherical_coords.R) * (Ellipsoid.re / spherical_coords.R)
        n = 1
        while n <= n_max:
            self.RelativeRadiusPower[n] = self.RelativeRadiusPower[n - 1] * (Ellipsoid.re / spherical_coords.R)
            n += 1

        self.cos_mlambda[0] = 1.0
        self.sin_mlambda[0] = 0.0

        self.cos_mlambda[1] = cos_lambda
        self.sin_mlambda[1] = sin_lambda
        m = 2
        while m <= n_max:
            self.cos_mlambda[m] = self.cos_mlambda[m - 1] * cos_lambda - self.sin_mlambda[m - 1] * sin_lambda
            self.sin_mlambda[m] = self.cos_mlambda[m - 1] * sin_lambda + self.sin_mlambda[m - 1] * cos_lambda
            m += 1
