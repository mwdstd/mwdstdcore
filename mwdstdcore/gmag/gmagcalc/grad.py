from mwdstdcore.gmag.gmagcalc.magelement import GeoMagneticElement


class Gradient:
    def __init__(self):
        self.UseGradient = 0
        self.GradPhi = GeoMagneticElement()
        self.GradLambda = GeoMagneticElement()
        self.GradZ = GeoMagneticElement()

    def set_component(self, component: str, gmag_elements: list, dist: float):
        swap: GeoMagneticElement
        if component == 'north':
            swap = self.GradPhi
        elif component == 'east':
            swap = self.GradLambda
        elif component == 'down':
            swap = self.GradZ
        else:
            return
        swap.X = (gmag_elements[0].X - gmag_elements[1].X) / dist
        swap.Y = (gmag_elements[0].Y - gmag_elements[1].Y) / dist
        swap.Z = (gmag_elements[0].Z - gmag_elements[1].Z) / dist

        swap.H = (gmag_elements[0].H - gmag_elements[1].H) / dist
        swap.F = (gmag_elements[0].F - gmag_elements[1].F) / dist
        swap.Decl = (gmag_elements[0].Decl - gmag_elements[1].Decl) / dist
        swap.Incl = (gmag_elements[0].Incl - gmag_elements[1].Incl) / dist

        swap.Xdot = (gmag_elements[0].Xdot - gmag_elements[1].Xdot) / dist
        swap.Ydot = (gmag_elements[0].Ydot - gmag_elements[1].Ydot) / dist
        swap.Zdot = (gmag_elements[0].Zdot - gmag_elements[1].Zdot) / dist

        swap.Hdot = (gmag_elements[0].Hdot - gmag_elements[1].Hdot) / dist
        swap.Fdot = (gmag_elements[0].Fdot - gmag_elements[1].Fdot) / dist
        swap.Decldot = (gmag_elements[0].Decldot - gmag_elements[1].Decldot) / dist
        swap.Incldot = (gmag_elements[0].Incldot - gmag_elements[1].Incldot) / dist

        swap.GV = (gmag_elements[0].GV - gmag_elements[1].GV) / dist
        swap.GVdot = (gmag_elements[0].GVdot - gmag_elements[1].GVdot) / dist
