from math import sin, cos, tan, acos, pi
from .ext_fields import ExtFields
from .dnimodel import DnIModel


class Station:
    def __init__(self, md=0., inc=0., az=0., tf=0., g_ref=9.81, b_ref=50000., d_ref=70.*pi/180, dec=0., grid=0.,
                 tvd=0., ns=0., ew=0., emi=0., egi=0., dni_model=DnIModel()):
        self.md = md
        self.inc = inc
        self.az = az
        self.tf = tf
        self.g_ref = g_ref
        self.b_ref = b_ref
        self.d_ref = d_ref
        self.dec = dec
        self.grid = grid
        self.tvd = tvd
        self.ns = ns
        self.ew = ew
        self.dls = 0.
        self.lat = 0.
        self.sag = 0.
        if not ExtFields.init_flag:
            ExtFields.init(g_ref=g_ref, b_ref=b_ref, d_ref=d_ref, ref_err='zero')
        self.fields = ExtFields(emi, egi)
        self.error = dni_model

    def calc_station(self, so):
        # so - previous station
        md1 = self.md
        md0 = so.md
        inc1 = self.inc
        inc0 = so.inc
        az1 = self.az
        az0 = so.az
        dmd = md1 - md0
        if dmd == 0:
            self.tvd = so.tvd
            self.ns = so.ns
            self.ew = so.ew
            self.dls = so.dls
            return

        if az0 == az1 and inc0 == inc1:
            self.ns = so.ns + dmd * sin(inc0) * cos(az0)
            self.ew = so.ew + dmd * sin(inc0) * sin(az0)
            self.tvd = so.tvd + dmd * cos(inc0)
            self.dls = 0
        else:
            dl = acos(cos(inc1 - inc0) - sin(inc0) * sin(inc1) * (1 - cos(az1 - az0)))
            rf = tan(dl / 2) / dl
            self.ns = so.ns + dmd * rf * (sin(inc0) * cos(az0) + sin(inc1) * cos(az1))
            self.ew = so.ew + dmd * rf * (sin(inc0) * sin(az0) + sin(inc1) * sin(az1))
            self.tvd = so.tvd + dmd * rf * (cos(inc0) + cos(inc1))
            self.dls = dl / dmd
        return

    def copy(self):
        s = Station(md=self.md, inc=self.inc, az=self.az, tf=self.tf, g_ref=self.g_ref, b_ref=self.b_ref,
                    d_ref=self.d_ref, dec=self.dec, grid=self.grid, tvd=self.tvd, ns=self.ns, ew=self.ew)
        return s
