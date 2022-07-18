import attr
import numpy as np


@attr.s(auto_attribs=True)
class DnIParams:
    ABX: float
    ABY: float
    ABZ: float
    ASX: float
    ASY: float
    ASZ: float
    MBX: float
    MBY: float
    MBZ: float
    MSX: float
    MSY: float
    MSZ: float
    MXY: float
    MXZ: float
    MYZ: float

    def toarray(self):
        return np.array([
            self.ABX, self.ABY, self.ABZ, self.ASX, self.ASY, self.ASZ,
            self.MBX, self.MBY, self.MBZ, self.MSX, self.MSY, self.MSZ,
            self.MXY, self.MXZ, self.MYZ])

    @classmethod
    def fromarray(cls, a):
        return cls(ABX=a[0],  ABY=a[1],  ABZ=a[2],
                   ASX=a[3],  ASY=a[4],  ASZ=a[5],
                   MBX=a[6],  MBY=a[7],  MBZ=a[8],
                   MSX=a[9],  MSY=a[10], MSZ=a[11],
                   MXY=a[12], MXZ=a[13], MYZ=a[14])
