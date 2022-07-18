from math import sin, cos, atan2, asin, sqrt, pi
import numpy as np
from .station import Station


class Survey:
    def __init__(self, station: Station):
        self.md = station.md
        [self.g_xyz, self.b_xyz] = self.axis_calc(station)
        self.g_ref = station.g_ref
        self.b_ref = station.b_ref
        self.d_ref = station.d_ref
        self.dec = station.dec
        self.grid = station.grid
        self.sag = station.sag
        [self.inc, self.az, self.tf, self.g, self.b, self.d] = \
            self.survey_calc(self.g_xyz, self.b_xyz, self.dec, self.grid, self.sag)
        self.failed_axis = station.error.FA
        # [STD, INC, BAD]
        self.stat = 'STD'

    @staticmethod
    def axis_calc(station: Station):
        inc = station.inc + station.sag
        az = station.az - (station.dec - station.grid)
        tf = station.tf
        gravity_vector = station.fields.gravity_vector
        magnetic_vector = station.fields.magnetic_vector
        # calculate survey
        rot_mat_az = np.array([[0, 0, 1], [cos(az), sin(az), 0], [-sin(az), cos(az), 0]])
        rot_mat_inc = np.array([[cos(inc), sin(inc), 0], [-sin(inc), cos(inc), 0], [0, 0, 1]])
        rot_mat_tf = np.array([[1, 0, 0], [0, cos(tf), sin(tf)], [0, -sin(tf), cos(tf)]])
        xyz_to_zyx = np.array([[0, 0, 1], [0, 1, 0], [1, 0, 0]])
        rot_mat = xyz_to_zyx @ rot_mat_tf @ rot_mat_inc @ rot_mat_az

        g_xyz = rot_mat @ gravity_vector
        b_xyz = rot_mat @ magnetic_vector
        # apply scale factors, biases, and misalignment
        identity_mat = np.eye(3)
        g_xyz = (identity_mat + station.error.AS) @ g_xyz + station.error.AB
        b_xyz = (identity_mat + station.error.MS + station.error.MI) @ b_xyz + station.error.MB
        # fail axis if applicable
        [acc_failure_mat, mag_failure_mat] = Survey.axis_decod(station.error.FA)
        g_xyz = (identity_mat - acc_failure_mat) @ g_xyz + station.g_ref * acc_failure_mat @ np.random.randn(3)
        b_xyz = (identity_mat - mag_failure_mat) @ b_xyz + station.b_ref * mag_failure_mat @ np.random.randn(3)
        return [g_xyz, b_xyz]

    @staticmethod
    def survey_calc(g_xyz_, b_xyz_, dec, grid, sag):
        zyx_to_xyz = np.array([[0, 0, 1], [0, 1, 0], [1, 0, 0]]).T
        g_xyz = zyx_to_xyz @ g_xyz_
        b_xyz = zyx_to_xyz @ b_xyz_

        [g, b, d] = Survey.total_calc(g_xyz, b_xyz)
        a1 = b_xyz[0] / b - g_xyz[0] / g * sin(d)
        a2 = (g_xyz[1] * b_xyz[2] - g_xyz[2] * b_xyz[1]) / g / b
        az = atan2(a2, a1) + (dec - grid)
        if az < 0:
            az = az + 2 * pi

        inc = atan2(sqrt(g_xyz[1] ** 2 + g_xyz[2] ** 2), g_xyz[0]) - sag
        tf = atan2(g_xyz[2], -g_xyz[1])
        return [inc, az, tf, g, b, d]

    @staticmethod
    def total_calc(g_xyz, b_xyz):
        g = sqrt(g_xyz[0] ** 2 + g_xyz[1] ** 2 + g_xyz[2] ** 2)
        b = sqrt(b_xyz[0] ** 2 + b_xyz[1] ** 2 + b_xyz[2] ** 2)
        d = asin((g_xyz[0] * b_xyz[0] + g_xyz[1] * b_xyz[1] + g_xyz[2] * b_xyz[2]) / g / b)
        return [g, b, d]

    @staticmethod
    def axis_decod(failed_axis: str):
        acc_failure_mat = np.zeros((3, 3))
        mag_failure_mat = np.zeros((3, 3))
        if failed_axis == 'AFX':
            acc_failure_mat[0, 0] = 1
        elif failed_axis == 'AFY':
            acc_failure_mat[1, 1] = 1
        elif failed_axis == 'AFZ':
            acc_failure_mat[2, 2] = 1
        elif failed_axis == 'MFX':
            mag_failure_mat[0, 0] = 1
        elif failed_axis == 'MFY':
            mag_failure_mat[1, 1] = 1
        elif failed_axis == 'MFZ':
            mag_failure_mat[2, 2] = 1
        return [acc_failure_mat, mag_failure_mat]
