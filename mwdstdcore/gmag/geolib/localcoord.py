class CoordLocal:
    def __init__(self, ns=0., ew=0., tvd=0.):
        self.NS = ns
        self.EW = ew
        self.TVD = tvd

    def clone(self):
        res = CoordLocal()
        res.NS = self.NS
        res.EW = self.EW
        res.TVD = self.TVD
        return res
