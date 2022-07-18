import numpy as np


class DnIModel:
    def __init__(self, AS=[0.,0.,0.], AB=[0.,0.,0.], MS=[0.,0.,0.], MB=[0.,0.,0.],
                 MXY=0., MXZ=0., MYZ=0., failed_axis='none'):
        self.AS = np.diag(AS, 0)  # accels' scale factors
        self.AB = np.array(AB)  # accels' biases
        self.MS = np.diag(MS, 0)  # mags' scale factors
        self.MB = np.array(MB)  # mags' biases
        self.MI = np.array([[0, MXY, MXZ], [-MXY, 0, MYZ], [-MXZ, -MYZ, 0]])  # misalignment matrix
        self.FA = failed_axis  # failed axis mnemonic
