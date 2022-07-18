from math import sqrt, degrees as rad2deg, atan2


class GeoMagneticElement:
    def __init__(self, mag_geo=None, mag_var=None):
        self.Decl = 0.
        self.Incl = 0.
        self.F = 0.
        self.H = 0.
        self.X = 0.
        self.Y = 0.
        self.Z = 0.
        
        if not (mag_geo is None):
            self.X = mag_geo.Bx
            self.Y = mag_geo.By
            self.Z = mag_geo.Bz
            self.H = sqrt(mag_geo.Bx * mag_geo.Bx + mag_geo.By * mag_geo.By)
            self.F = sqrt(self.H * self.H + mag_geo.Bz * mag_geo.Bz)
            self.Decl = rad2deg(atan2(self.Y, self.X))
            self.Incl = rad2deg(atan2(self.Z, self.H))

        self.GV = 0.
        self.Decldot = 0.
        self.Incldot = 0.
        self.Fdot = 0.
        self.Hdot = 0.
        self.Xdot = 0.
        self.Ydot = 0.
        self.Zdot = 0.
        self.GVdot = 0.
        
        if not (mag_var is None):
            self.Xdot = mag_var.Bx
            self.Ydot = mag_var.By
            self.Zdot = mag_var.Bz
            self.Hdot = (self.X * self.Xdot + self.Y * self.Ydot) / self.H
            self.Fdot = (self.X * self.Xdot + self.Y * self.Ydot + self.Z * self.Zdot) / self.F
            self.Decldot = rad2deg((self.X * self.Ydot - self.Y * self.Xdot) / (self.H * self.H))
            self.Incldot = rad2deg((self.H * self.Zdot - self.Z * self.Hdot) / (self.F * self.F))
            self.GVdot = self.Decldot
