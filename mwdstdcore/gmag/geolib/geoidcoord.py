from math import cos, sin, asin, sqrt, radians as deg2rad, degrees as rad2deg, floor
from .geoid import Geoid
from .sphcoord import CoordSpherical
from .ellipsoid import Ellipsoid


class CoordGeodetic:
    def __init__(self, lat: float, long: float, alt: float, altitude_type):
        self.Lambda = 0.
        self.Phi = 0.
        self.HeightAboveEllipsoid = 0.
        self.HeightAboveGeoid = 0.
        self.AltitudeType = altitude_type
        if altitude_type == 'MSL':
            self.UseGeoid = 1
        else:
            self.UseGeoid = 0
        self.Geoid = Geoid(altitude_type=altitude_type)

        self.__set_coords(lat, long, alt)

    def clone(self):
        if self.AltitudeType == 'MSL':
            altitude = self.HeightAboveGeoid
        else:
            altitude = self.HeightAboveEllipsoid
        res = CoordGeodetic(lat=self.Phi, long=self.Lambda, alt=altitude, altitude_type=self.AltitudeType)
        return res

    def geodetic_to_spherical(self) -> CoordSpherical:
        cos_lat = cos(deg2rad(self.Phi))
        sin_lat = sin(deg2rad(self.Phi))

        rc = Ellipsoid.a / sqrt(1.0 - Ellipsoid.epssq * sin_lat * sin_lat)

        xp = (rc + self.HeightAboveEllipsoid) * cos_lat
        zp = (rc * (1.0 - Ellipsoid.epssq) + self.HeightAboveEllipsoid) * sin_lat

        spherical_coords = CoordSpherical()
        spherical_coords.R = sqrt(xp * xp + zp * zp)
        spherical_coords.Phig = rad2deg(asin(zp / spherical_coords.R))
        spherical_coords.Lambda = self.Lambda
        return spherical_coords

    def __set_coords(self, lat: float, long: float, alt: float):
        lat_bound = (-90., 90)
        lon_bound = (-180., 180)
        alt_bound = (-10, 10)

        if lat_bound[0] <= lat <= lat_bound[1]:
            self.Phi = lat
        else:
            raise Exception('class CoordGeodetic method set_coords(): Latitude is out or range')

        if lon_bound[0] <= long <= lon_bound[1]:
            self.Lambda = long
        else:
            raise Exception('class CoordGeodetic method set_coords(): Longitude is out or range')

        if alt_bound[0] <= alt <= alt_bound[1]:
            if self.AltitudeType == 'MSL':
                self.HeightAboveGeoid = alt
                delta_height = self.__geoid2ellipsoid()
                self.HeightAboveEllipsoid = self.HeightAboveGeoid + delta_height / 1000
            else:
                self.HeightAboveEllipsoid = alt
                self.HeightAboveGeoid = self.HeightAboveEllipsoid
        else:
            raise Exception('class CoordGeodetic method set_coords(): Altitude is out or range')

        pass

    def __geoid2ellipsoid(self):
        long = self.Lambda
        lat = self.Phi
        if long < 0.0:
            offset_x = (long + 360.0) * self.Geoid.ScaleFactor
        else:
            offset_x = long * self.Geoid.ScaleFactor
        offset_y = (90.0 - lat) * self.Geoid.ScaleFactor

        post_x = int(floor(offset_x))
        if (post_x + 1) == self.Geoid.NumbGeoidCols:
            post_x -= 1
        post_y = int(floor(offset_y))
        if (post_y + 1) == self.Geoid.NumbGeoidRows:
            post_y -= 1

        index = int(post_y * self.Geoid.NumbGeoidCols + post_x)
        elevation_nw = float(self.Geoid.GeoidHeightBuffer[index])
        elevation_ne = float(self.Geoid.GeoidHeightBuffer[index + 1])

        index = int((post_y + 1) * self.Geoid.NumbGeoidCols + post_x)
        elevation_sw = float(self.Geoid.GeoidHeightBuffer[index])
        elevation_se = float(self.Geoid.GeoidHeightBuffer[index + 1])

        delta_x = offset_x - post_x
        delta_y = offset_y - post_y

        upper_y = elevation_nw + delta_x * (elevation_ne - elevation_nw)
        lower_y = elevation_sw + delta_x * (elevation_se - elevation_sw)

        delta_height = upper_y + delta_y * (lower_y - upper_y)
        return delta_height
