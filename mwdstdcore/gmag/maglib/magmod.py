import numpy as np


class MagneticModel:
    def __init__(self, nterms=-1):
        self.EditionDate = 0.
        self.epoch = 0.
        self.ModelName = ''
        z = np.zeros(int(nterms) + 1)
        self.Main_Field_Coeff_G = z.copy()
        self.Main_Field_Coeff_H = z.copy()
        self.Secular_Var_Coeff_G = z.copy()
        self.Secular_Var_Coeff_H = z.copy()
        self.nMax = 0
        self.nMaxSecVar = 0
        self.SecularVariationUsed = 0
        self.CoefficientFileEndDate = 0.
