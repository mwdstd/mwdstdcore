from math import sqrt, sin, cos, asin, atan2, pi
import numpy as np
from mwdstdcore.errormods.gmagmod import bggm


class ExtFields:
    init_flag = False
    ref_error_g = 0.
    ref_error_b = 0.
    ref_error_d = 0.
    g = 0.
    b = 0.
    d = 0.
    geomod = bggm
    num_of_sigma = 0.

    @staticmethod
    def init(g_ref, b_ref, d_ref, ref_err='zero', geomod=bggm, num_of_sigma=3.,
             egbd=(bggm['MGI'], bggm['MBI'], bggm['MDI'])):
        ExtFields.init_flag = True
        if ref_err == 'rnd':
            ExtFields.ref_error_g = geomod['MGI'] * np.random.randn(1)  # mG
            ExtFields.ref_error_b = geomod['MBI'] * np.random.randn(1)  # nT
            ExtFields.ref_error_d = geomod['MDI'] * np.random.randn(1)  # rad
        elif ref_err == 'def':
            ExtFields.ref_error_g = egbd[0]  # mG
            ExtFields.ref_error_b = egbd[1]  # nT
            ExtFields.ref_error_d = egbd[2]  # rad
        else:
            ExtFields.ref_error_g = 0
            ExtFields.ref_error_b = 0
            ExtFields.ref_error_d = 0
        ExtFields.g = g_ref + ExtFields.ref_error_g
        ExtFields.b = b_ref + ExtFields.ref_error_b
        ExtFields.d = d_ref + ExtFields.ref_error_d
        ExtFields.geomod = geomod
        ExtFields.num_of_sigma = num_of_sigma

    # EMI - external magnetic interference
    def __init__(self, emi=0., egi=0.):
        self.emi = emi * np.random.randn(3)
        self.egi = egi * np.random.randn(3)
        self.gravity_vector = ExtFields.g * np.array([0, 0, 1]) + self.egi
        self.magnetic_vector = ExtFields.b * np.array([cos(ExtFields.d), 0, sin(ExtFields.d)]) + self.emi

        # quality check
        g_tot = np.linalg.norm(self.gravity_vector)
        b_tot = np.linalg.norm(self.magnetic_vector)
        self.error_g = g_tot - ExtFields.g
        self.error_b = b_tot - ExtFields.b
        self.error_d = asin(self.magnetic_vector[2] / b_tot) - ExtFields.d
        self.error_dec = atan2(self.magnetic_vector[1], self.magnetic_vector[0])
        if abs(self.error_g) > ExtFields.num_of_sigma * ExtFields.geomod['MGI']:
            self.qc = 2  # BAD survey
        elif (abs(self.error_b) > ExtFields.num_of_sigma * ExtFields.geomod['MBI'] or
              abs(self.error_d) > ExtFields.num_of_sigma * ExtFields.geomod['MDI'] or
              abs(self.error_dec) > ExtFields.num_of_sigma *
              sqrt(ExtFields.geomod['DEC']**2 + (ExtFields.geomod['DBH'] / self.b / cos(self.d))**2)):
            self.qc = 1  # INC only survey
        else:
            self.qc = 0  # STD survey
