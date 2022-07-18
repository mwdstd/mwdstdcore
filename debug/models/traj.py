from typing import List, Dict
from math import sin, cos, acos, tan, asin, atan, sqrt, atan2, pi
import numpy as np
from .station import Station


# trajectory indexes
class ti:
    num = 0
    md = 1
    inc = 2
    az = 3
    tf = 4
    tvd = 5
    ns = 6
    ew = 7
    dls = 8
    g = 9
    b = 10
    dip = 11
    dec = 12
    grid = 13
    lat = 14
    errmod = 15


class Traj:
    earth_rate = 15.04 * pi / 180

    def __init__(self, stations_list: List[Station] = None, stations_array: np.ndarray = None,
                 stations_list_short: List[List[float]] = None, stations_dict_short: List[Dict[str, float]] = None,
                 tie_in: Station = None):
        self.col_num = 16
        self.traj = np.zeros((0, self.col_num))
        self.append(stations_list=stations_list, stations_array=stations_array, stations_list_short=stations_list_short,
                    stations_dict_short=stations_dict_short, tie_in=tie_in)

    def append(self, stations_list: List[Station] = None, stations_array: np.ndarray = None,
               stations_list_short: List[List[float]] = None, stations_dict_short: List[Dict[str, float]] = None,
               tie_in: Station = None, clear=False):
        if clear:
            self.traj = np.zeros((0, self.col_num))
        num_prev = self.traj.shape[0]
        if not (stations_list is None):
            s: Station
            i = 0
            for s in stations_list:
                row = np.array([[i + num_prev, s.md, s.inc, s.az, s.tf, s.tvd, s.ns, s.ew, 0., s.g_ref, s.b_ref,
                                 s.d_ref, s.dec, s.grid, s.lat, 0.]])
                self.traj = np.block([[self.traj], [row]])
                i += 1
        elif not (stations_list_short is None):
            i = 0
            for stn in stations_list_short:
                md = stn[0]
                inc = stn[1]
                az = stn[2]
                if not (tie_in is None):
                    row = np.array([[i + num_prev, md, inc, az, 0., tie_in.tvd, tie_in.ns, tie_in.ew, 0., tie_in.g_ref,
                                     tie_in.b_ref, tie_in.d_ref, tie_in.dec, tie_in.grid, tie_in.lat, 0.]])
                else:
                    row = np.array([[i + num_prev, md, inc, az, 0., 0., 0., 0., 0., 9.81, 50000, 70. * pi / 180, 0., 0.,
                                     60. * pi / 180, 0.]])
                self.traj = np.block([[self.traj], [row]])
                i += 1
        elif not (stations_dict_short is None):
            i = 0
            for stn in stations_dict_short:
                md = stn['md']
                inc = stn['inc']
                az = stn['az']
                if not (tie_in is None):
                    row = np.array([[i + num_prev, md, inc, az, 0., tie_in.tvd, tie_in.ns, tie_in.ew, 0., tie_in.g_ref,
                                     tie_in.b_ref, tie_in.d_ref, tie_in.dec, tie_in.grid, tie_in.lat, 0.]])
                else:
                    row = np.array([[i + num_prev, md, inc, az, 0., 0., 0., 0., 0., 9.81, 50000, 70. * pi / 180, 0., 0.,
                                     60. * pi / 180, 0.]])
                self.traj = np.block([[self.traj], [row]])
                i += 1
        elif not (stations_array is None):
            if stations_array.shape[0] == 0 or stations_array.shape[1] != self.col_num:
                NameError('class Traj, method append: Incorrect stations_array shape')
            num = stations_array.shape[0]
            for i in range(0, num):
                row = stations_array[i, :]
                row[ti.num] = i + num_prev
                self.traj = np.block([[self.traj], [row]])
        else:
            return
        # sorting on measured depth
        self.traj = self.traj[np.argsort(self.traj[:, ti.md])]
        # recalculating
        num = self.traj.shape[0]
        for i in range(1, num):
            self.traj[i, :] = self.__min_curvature(self.traj[i - 1, :], self.traj[i, :])

    def find_row(self, md: float):
        s = self.traj[0, :]
        num = self.traj.shape[0]
        if num < 2:
            return s
        if md <= self.traj[0, ti.md]:
            s = self.traj[0, :]
            if s[ti.az] < 0:
                s[ti.az] += 2 * pi
            return s
        if md >= self.traj[-1, ti.md]:
            s = self.traj[-1, :]
            if s[ti.az] < 0:
                s[ti.az] += 2 * pi
            return s
        if (md > self.traj[0, ti.md]) and (md < self.traj[-1, ti.md]):
            i = 0
            while i < num:
                if ((md >= self.traj[i, ti.md]) and (md < self.traj[i + 1, ti.md])) or (i == num - 2):
                    break
                i += 1
            s = Traj.__interpolate(md, self.traj[i, :], self.traj[i + 1, :])
        return s

    def find_station(self, md: float, recalc_tf=False):
        row = self.find_row(md)
        s = self.__row_to_station(row)
        if recalc_tf:
            row0 = self.find_row(md - 0.1)
            s0 = self.__row_to_station(row0)
            s.tf = Traj.toolface(s0.inc, s.inc, s0.az, s.az)
        return s

    def __row_to_station(self, row: np.ndarray) -> Station:
        s = Station()
        if row.shape[0] != self.col_num:
            NameError('class Traj, method row_to_station: Incorrect row shape')
        s.md = row[ti.md]
        s.inc = row[ti.inc]
        s.az = row[ti.az]
        s.tf = row[ti.tf]
        s.tvd = row[ti.tvd]
        s.ns = row[ti.ns]
        s.ew = row[ti.ew]
        s.dls = row[ti.dls]
        s.g_ref = row[ti.g]
        s.b_ref = row[ti.b]
        s.d_ref = row[ti.dip]
        s.dec = row[ti.dec]
        s.grid = row[ti.grid]
        s.lat = row[ti.lat]

        return s

    @staticmethod
    def __min_curvature(s0: np.ndarray, s1: np.ndarray):
        dmd = s1[ti.md] - s0[ti.md]
        if dmd == 0:
            s1[:] = s0[:]
            return s1
        inc0 = s0[ti.inc]
        inc1 = s1[ti.inc]
        az0 = s0[ti.az]
        az1 = s1[ti.az]

        dl = acos(cos(inc1 - inc0) - sin(inc0) * sin(inc1) * (1 - cos(az1 - az0)))
        if dl == 0.:
            dns = dmd * sin(inc0) * cos(az0)
            dew = dmd * sin(inc0) * sin(az0)
            dtvd = dmd * cos(inc0)
            s1[ti.dls] = 0.
        else:
            rf = tan(dl / 2) / dl
            dns = dmd * rf * (sin(inc0) * cos(az0) + sin(inc1) * cos(az1))
            dew = dmd * rf * (sin(inc0) * sin(az0) + sin(inc1) * sin(az1))
            dtvd = dmd * rf * (cos(inc0) + cos(inc1))
            s1[ti.dls] = dl / dmd
        s1[ti.ns] = s0[ti.ns] + dns
        s1[ti.ew] = s0[ti.ew] + dew
        s1[ti.tvd] = s0[ti.tvd] + dtvd
        return s1

    @staticmethod
    def __interpolate(mdi: float, s0: np.ndarray, s1: np.ndarray):
        md0 = s0[ti.md]
        md1 = s1[ti.md]
        if not ((mdi >= md0) and (mdi <= md1)):
            raise NameError('class Traj, method interpolate: Incorrect input argument: md')
        dmd = md1 - md0
        dmdi = mdi - md0
        if dmdi == 0:
            s = s0.copy()
            return s
        inc0 = s0[ti.inc]
        inc1 = s1[ti.inc]
        az0 = s0[ti.az]
        az1 = s1[ti.az]
        vect_0 = np.array([sin(inc0) * cos(az0), sin(inc0) * sin(az0), cos(inc0)])
        vect_1 = np.array([sin(inc1) * cos(az1), sin(inc1) * sin(az1), cos(inc1)])
        k = dmdi / dmd
        if not ((inc0 == inc1) and (az0 == az1)) and not ((inc0 == 0.) and (inc1 == 0.)):
            dl_angle = 2 * asin(sqrt(sin((inc1 - inc0) / 2) ** 2 + sin(inc0) * sin(inc1) * sin((az1 - az0) / 2) ** 2))
            vect_i = (sin((1 - k) * dl_angle) * vect_0 + sin(k * dl_angle) * vect_1) / sin(dl_angle)
        else:
            vect_i = vect_0.copy()
        inci = acos(vect_i[2])
        azi = atan2(vect_i[1], vect_i[0])
        if azi < 0:
            azi += 2 * pi
        s = np.zeros_like(s0)
        s[ti.md] = mdi
        s[ti.inc] = inci
        s[ti.az] = azi
        s = Traj.__min_curvature(s0, s)

        if md0 != md1:
            s[ti.tf] = s0[ti.tf] + (s1[ti.tf] - s0[ti.tf]) * k
            s[ti.g] = s0[ti.g] + (s1[ti.g] - s0[ti.g]) * k
            s[ti.b] = s0[ti.b] + (s1[ti.b] - s0[ti.b]) * k
            s[ti.dip] = s0[ti.dip] + (s1[ti.dip] - s0[ti.dip]) * k
            s[ti.dec] = s0[ti.dec] + (s1[ti.dec] - s0[ti.dec]) * k
            s[ti.grid] = s0[ti.grid] + (s1[ti.grid] - s0[ti.grid]) * k
            s[ti.lat] = s0[ti.lat]
            s[ti.errmod] = s0[ti.errmod]
        else:
            s[ti.tf] = s0[ti.tf]
            s[ti.g] = s0[ti.g]
            s[ti.b] = s0[ti.b]
            s[ti.dip] = s0[ti.dip]
            s[ti.dec] = s0[ti.dec]
            s[ti.grid] = s0[ti.grid]
            s[ti.lat] = s0[ti.lat]
            s[ti.errmod] = s0[ti.errmod]
        return s

    @staticmethod
    def toolface(inc1, inc2, az1, az2):
        # calculate wellbore toolface between two surveys
        y = sin(inc2) * cos(inc1) - sin(inc1) * cos(inc2) * cos(az2 - az1)
        x = sin(inc1) * sin(az2 - az1)
        tf = 0
        if y > 0:
            tf = atan(x / y)
        elif y < 0:
            tf = atan(x / y) + pi
        elif y == 0:
            if x < 0:
                tf = -pi / 2
            elif x == 0:
                tf = 0
            elif x > 0:
                tf = pi / 2
        return tf

    @staticmethod
    def nev2hla(inc: float, az: float) -> np.ndarray:
        return np.asarray([[cos(inc) * cos(az), -sin(az), sin(inc) * cos(az)],
                           [cos(inc) * sin(az), cos(az), sin(inc) * sin(az)],
                           [-sin(inc), 0, cos(inc)]])
