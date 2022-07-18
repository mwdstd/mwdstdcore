import numpy as np
from math import fabs, sin, sqrt, radians as deg2rad
from mwdstdcore.gmag.geolib.sphcoord import CoordSpherical
from mwdstdcore.gmag.maglib.magmod import MagneticModel


class LegendreFunction:
    def __init__(self, mag_model: MagneticModel, spherical_coords: CoordSpherical):
        nterms = int((mag_model.nMax + 1) * (mag_model.nMax + 2) / 2)

        self.Pcup = np.zeros(nterms+1)
        self.dPcup = np.zeros(nterms+1)

        self.__compute(spherical_coords, mag_model.nMax)

    def __compute(self, spherical_coords: CoordSpherical, n_max: int):
        sin_phi = sin(deg2rad(spherical_coords.Phig))

        if n_max <= 16 or (1 - fabs(sin_phi)) < 1.0e-10:
            self.__pcup_low(sin_phi, n_max)
        else:
            self.__pcup_high(sin_phi, n_max)

    def __pcup_low(self, x: float, n_max: int):

        self.Pcup[0] = 1.0
        self.dPcup[0] = 0.0
        z = sqrt((1.0 - x) * (1.0 + x))

        nterms = int((n_max + 1) * (n_max + 2) / 2)
        schmidt_quasi_norm = np.zeros(nterms + 1)

        for n in range(1, n_max + 1):
            for m in range(0, n + 1):
                index = int(n * (n + 1) / 2 + m)
                if n == m:
                    index1 = int((n - 1) * n / 2 + m - 1)
                    self.Pcup[index] = z * self.Pcup[index1]
                    self.dPcup[index] = z * self.dPcup[index1] + x * self.Pcup[index1]
                elif n == 1 and m == 0:
                    index1 = int((n - 1) * n / 2 + m)
                    self.Pcup[index] = x * self.Pcup[index1]
                    self.dPcup[index] = x * self.dPcup[index1] - z * self.Pcup[index1]
                elif n > 1 and n != m:
                    index1 = int((n - 2) * (n - 1) / 2 + m)
                    index2 = int((n - 1) * n / 2 + m)
                    if m > n - 2:
                        self.Pcup[index] = x * self.Pcup[index2]
                        self.dPcup[index] = x * self.dPcup[index2] - z * self.Pcup[index2]
                    else:
                        k = float(((n - 1) * (n - 1)) - (m * m)) / float((2 * n - 1) * (2 * n - 3))
                        self.Pcup[index] = x * self.Pcup[index2] - k * self.Pcup[index1]
                        self.dPcup[index] = x * self.dPcup[index2] - z * self.Pcup[index2] - k * self.dPcup[index1]

        schmidt_quasi_norm[0] = 1.0
        for n in range(1, n_max + 1):
            index = int(n * (n + 1) / 2)
            index1 = int((n - 1) * n / 2)
            schmidt_quasi_norm[index] = schmidt_quasi_norm[index1] * float(2 * n - 1) / float(n)
            for m in range(1, n + 1):
                index = int(n * (n + 1) / 2 + m)
                index1 = int(n * (n + 1) / 2 + m - 1)
                schmidt_quasi_norm[index] = schmidt_quasi_norm[index1] * \
                    sqrt(float((n - m + 1) * (2 if m == 1 else 1)) / float(n + m))

        for n in range(1, n_max + 1):
            for m in range(0, n + 1):
                index = int(n * (n + 1) / 2 + m)
                self.Pcup[index] = self.Pcup[index] * schmidt_quasi_norm[index]
                self.dPcup[index] = -self.dPcup[index] * schmidt_quasi_norm[index]

    def __pcup_high(self, x: float, n_max: int):
        m = 0
        nterms = int((n_max + 1) * (n_max + 2) / 2)

        if fabs(x) == 1.0:
            raise Exception("Error in PcupHigh: derivative cannot be calculated at poles")

        f1 = np.zeros(nterms + 1)
        pre_sqr = np.zeros(nterms + 1)
        f2 = np.zeros(nterms + 1)

        scalef = 1.0e-280

        pre_sqr = np.sqrt(np.asarray(range(0, (2 * n_max + 1) + 1)))

        k = 2

        for n in range(2, n_max + 1):
            k = k + 1
            f1[k] = float(2 * n - 1) / float(n)
            f2[k] = float(n - 1) / float(n)

            dlt = n - 2
            f1[(k + 1):(k + dlt + 1)] = float(2 * n - 1) / pre_sqr[(n + 1):(n + dlt + 1)] / \
                pre_sqr[(n - 1):(n - dlt - 1):-1]
            f2[(k + 1):(k + dlt + 1)] = pre_sqr[(n - 2):(n - dlt - 2):-1] * pre_sqr[n:(n + dlt)] / \
                pre_sqr[(n + 1):(n + dlt + 1)] / pre_sqr[(n - 1):(n - dlt - 1):-1]

            k = k + n

        z = sqrt((1.0 - x) * (1.0 + x))
        pm2 = 1.0
        self.Pcup[0] = 1.0
        self.dPcup[0] = 0.0
        if n_max == 0:
            raise Exception("Error in PcupHigh: n_max can not be zero")
        pm1 = x
        self.Pcup[1] = pm1
        self.dPcup[1] = z
        k = 1

        for n in range(2, n_max + 1):
            k = k + n
            plm = f1[k] * x * pm1 - f2[k] * pm2
            self.Pcup[k] = plm
            self.dPcup[k] = float(n) * (pm1 - x * plm) / z
            pm2 = pm1
            pm1 = plm

        pmm = pre_sqr[2] * scalef
        rescalem = 1.0 / scalef
        kstart = 0

        for m in range(1, (n_max - 1) + 1):
            rescalem = rescalem * z

            kstart = kstart + m + 1
            pmm = pmm * pre_sqr[2 * m + 1] / pre_sqr[2 * m]
            self.Pcup[kstart] = pmm * rescalem / pre_sqr[2 * m + 1]
            self.dPcup[kstart] = -(float(m) * x * self.Pcup[kstart] / z)
            pm2 = pmm / pre_sqr[2 * m + 1]
            k = kstart + m + 1
            pm1 = x * pre_sqr[2 * m + 1] * pm2
            self.Pcup[k] = pm1 * rescalem
            self.dPcup[k] = ((pm2 * rescalem) * pre_sqr[2 * m + 1] - x * float(m + 1) * self.Pcup[k]) / z
            for n in range(m + 2, n_max + 1):
                k = k + n
                plm = x * f1[k] * pm1 - f2[k] * pm2
                self.Pcup[k] = plm * rescalem
                self.dPcup[k] = (pre_sqr[n + m] * pre_sqr[n - m] * (pm1 * rescalem) - float(n) * x * self.Pcup[k]) / z
                pm2 = pm1
                pm1 = plm

        rescalem = rescalem * z
        kstart = kstart + m + 1
        pmm = pmm / pre_sqr[2 * n_max]
        self.Pcup[kstart] = pmm * rescalem
        self.dPcup[kstart] = -float(n_max) * x * self.Pcup[kstart] / z
