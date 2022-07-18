import numpy as np
from math import sin, cos, sqrt, fabs, radians as deg2rad
from mwdstdcore.gmag.geolib.sphcoord import CoordSpherical
from mwdstdcore.gmag.geolib.geoidcoord import CoordGeodetic
from mwdstdcore.gmag.maglib.magmod import MagneticModel
from mwdstdcore.gmag.gmagcalc.sphharm import SphericalHarmonicVariables
from mwdstdcore.gmag.gmagcalc.legfunc import LegendreFunction


class MagneticResults:
    def __init__(self, mag_model: MagneticModel, spherical_coords: CoordSpherical,
                 sph_harmonics: SphericalHarmonicVariables, legendre_func: LegendreFunction, mode: str):
        self.__Phig = spherical_coords.Phig
        self.Bx = 0.
        self.By = 0.
        self.Bz = 0.

        if mode == 'var':
            self.__secular_var_compute(mag_model, spherical_coords, sph_harmonics, legendre_func)
        elif mode == 'geo':
            self.__compute(mag_model, spherical_coords, sph_harmonics, legendre_func)
        elif mode == 'grad_y':
            self.__compute_grad_y(mag_model, spherical_coords, sph_harmonics, legendre_func)
        else:
            raise Exception('Class MagneticResult: wrong mode input variable')

    def rotate(self, geoid_coords: CoordGeodetic):
        psi = deg2rad(self.__Phig - geoid_coords.Phi)

        self.__Phig = geoid_coords.Phi

        self.Bz = self.Bx * sin(psi) + self.Bz * cos(psi)
        self.Bx = self.Bx * cos(psi) - self.Bz * sin(psi)
        self.By = self.By

    def __compute(self, mag_model: MagneticModel, spherical_coords: CoordSpherical,
                  sph_harmonics: SphericalHarmonicVariables, legendre_func: LegendreFunction):
        m = np.cumsum(np.ones(mag_model.nMax + 1)) - 1
        for n in range(1, mag_model.nMax + 1):
            shift = int(n * (n + 1) / 2)
            rrp = sph_harmonics.RelativeRadiusPower[n]
            g_cos = mag_model.Main_Field_Coeff_G[shift:shift+n+1] * sph_harmonics.cos_mlambda[0:n+1]
            g_sin = mag_model.Main_Field_Coeff_G[shift:shift+n+1] * sph_harmonics.sin_mlambda[0:n+1]
            h_cos = mag_model.Main_Field_Coeff_H[shift:shift+n+1] * sph_harmonics.cos_mlambda[0:n+1]
            h_sin = mag_model.Main_Field_Coeff_H[shift:shift+n+1] * sph_harmonics.sin_mlambda[0:n+1]
            self.Bz -= rrp * np.sum((g_cos + h_sin) * (n + 1) * legendre_func.Pcup[shift:shift+n+1])
            self.By += rrp * np.sum((g_sin - h_cos) * m[0:n+1] * legendre_func.Pcup[shift:shift+n+1])
            self.Bx -= rrp * np.sum((g_cos + h_sin) * legendre_func.dPcup[shift:shift+n+1])

        cos_phi = cos(deg2rad(spherical_coords.Phig))
        if fabs(cos_phi) > 1.0e-10:
            self.By = self.By / cos_phi
        else:
            self.__special_compute(mag_model, sph_harmonics, spherical_coords)

    def __special_compute(self, mag_model: MagneticModel, sph_harmonics: SphericalHarmonicVariables,
                          spherical_coords: CoordSpherical):
        PcupS = np.zeros(mag_model.nMax + 1)
        PcupS[0] = 1
        schmidtQuasiNorm1 = 1.0
        self.By = 0.0
        sin_phi = sin(deg2rad(spherical_coords.Phig))

        for n in range(1, mag_model.nMax + 1):
            index = int(n * (n + 1) / 2 + 1)
            schmidtQuasiNorm2 = schmidtQuasiNorm1 * float(2 * n - 1) / float(n)
            schmidtQuasiNorm3 = schmidtQuasiNorm2 * sqrt(float(n * 2) / float(n + 1))
            schmidtQuasiNorm1 = schmidtQuasiNorm2
            if n == 1:
                PcupS[n] = PcupS[n - 1]
            else:
                k = float(((n - 1) * (n - 1)) - 1) / float((2 * n - 1) * (2 * n - 3))
                PcupS[n] = sin_phi * PcupS[n - 1] - k * PcupS[n - 2]

            self.By += sph_harmonics.RelativeRadiusPower[n] * (mag_model.Main_Field_Coeff_G[index] *
                sph_harmonics.sin_mlambda[1] - mag_model.Main_Field_Coeff_H[index] * sph_harmonics.cos_mlambda[1]) * \
                PcupS[n] * schmidtQuasiNorm3

    def __secular_var_compute(self, mag_model: MagneticModel, spherical_coords: CoordSpherical,
                              sph_harmonics: SphericalHarmonicVariables, legendre_func: LegendreFunction):
        mag_model.SecularVariationUsed = 1
        for n in range(1, mag_model.nMaxSecVar + 1):
            for m in range(0, n + 1):
                index = int(n * (n + 1) / 2 + m)
                self.Bz -= \
                    sph_harmonics.RelativeRadiusPower[n] * (mag_model.Secular_Var_Coeff_G[index] *
                    sph_harmonics.cos_mlambda[m] + mag_model.Secular_Var_Coeff_H[index] *
                    sph_harmonics.sin_mlambda[m]) * float(n + 1) * legendre_func.Pcup[index]

                self.By += \
                    sph_harmonics.RelativeRadiusPower[n] * (mag_model.Secular_Var_Coeff_G[index] *
                    sph_harmonics.sin_mlambda[m] - mag_model.Secular_Var_Coeff_H[index] *
                    sph_harmonics.cos_mlambda[m]) * float(m) * legendre_func.Pcup[index]

                self.Bx -= \
                    sph_harmonics.RelativeRadiusPower[n] * (mag_model.Secular_Var_Coeff_G[index] *
                    sph_harmonics.cos_mlambda[m] + mag_model.Secular_Var_Coeff_H[index] *
                    sph_harmonics.sin_mlambda[m]) * legendre_func.dPcup[index]

        cos_phi = cos(deg2rad(spherical_coords.Phig))
        if fabs(cos_phi) > 1.0e-10:
            self.By = self.By / cos_phi
        else:
            self.__special_secular_var_compute(mag_model, sph_harmonics, spherical_coords)

    def __special_secular_var_compute(self, mag_model: MagneticModel, sph_harmonics: SphericalHarmonicVariables,
                                      spherical_coords: CoordSpherical):
        PcupS = np.zeros(mag_model.nMaxSecVar + 1)
        PcupS[0] = 1
        schmidtQuasiNorm1 = 1.0
        self.By = 0.0
        sin_phi = sin(deg2rad(spherical_coords.Phig))

        for n in range(1, mag_model.nMaxSecVar + 1):
            index = int(n * (n + 1) / 2 + 1)
            schmidtQuasiNorm2 = schmidtQuasiNorm1 * float(2 * n - 1) / float(n)
            schmidtQuasiNorm3 = schmidtQuasiNorm2 * sqrt(float(n * 2) / float(n + 1))
            schmidtQuasiNorm1 = schmidtQuasiNorm2
            if n == 1:
                PcupS[n] = PcupS[n - 1]
            else:
                k = float(((n - 1) * (n - 1)) - 1) / float((2 * n - 1) * (2 * n - 3))
                PcupS[n] = sin_phi * PcupS[n - 1] - k * PcupS[n - 2]

            self.By += \
                sph_harmonics.RelativeRadiusPower[n] * (mag_model.Secular_Var_Coeff_G[index] *
                sph_harmonics.sin_mlambda[1] - mag_model.Secular_Var_Coeff_H[index] * sph_harmonics.cos_mlambda[1]) * \
                PcupS[n] * schmidtQuasiNorm3

    def __compute_grad_y(self, mag_model: MagneticModel, spherical_coords: CoordSpherical,
                         sph_harmonics: SphericalHarmonicVariables, legendre_func: LegendreFunction):
        m = np.cumsum(np.ones(mag_model.nMax + 1)) - 1
        for n in range(1, mag_model.nMax + 1):
            shift = int(n * (n + 1) / 2)
            rrp = sph_harmonics.RelativeRadiusPower[n]
            g_cos = mag_model.Main_Field_Coeff_G[shift:shift + n + 1] * sph_harmonics.cos_mlambda[0:n + 1]
            g_sin = mag_model.Main_Field_Coeff_G[shift:shift + n + 1] * sph_harmonics.sin_mlambda[0:n + 1]
            h_cos = mag_model.Main_Field_Coeff_H[shift:shift + n + 1] * sph_harmonics.cos_mlambda[0:n + 1]
            h_sin = mag_model.Main_Field_Coeff_H[shift:shift + n + 1] * sph_harmonics.sin_mlambda[0:n + 1]
            self.Bz -= rrp * np.sum((-1. * g_sin + h_cos) * float(n + 1) * m[0:n + 1] *
                                    legendre_func.Pcup[shift:shift + n + 1]) * (1. / spherical_coords.R)
            self.By += rrp * np.sum((g_cos + h_sin) * m[0:n + 1] * m[0:n + 1] *
                                    legendre_func.Pcup[shift:shift + n + 1]) * (1. / spherical_coords.R)
            self.Bx -= rrp * np.sum((-1. * g_sin + h_cos) * m[0:n + 1] * legendre_func.dPcup[shift:shift + n + 1]) * \
                       (1. / spherical_coords.R)

        cos_phi = cos(deg2rad(spherical_coords.Phig))
        if fabs(cos_phi) > 1.0e-10:
            self.By = self.By / (cos_phi * cos_phi)
            self.Bx = self.Bx / cos_phi
            self.Bz = self.Bz / cos_phi
        else:
            pass
