from .geoid_heights_load import geoid_heiths_buffer


class Geoid:
    def __init__(self, altitude_type='MSL'):
        # Sets EGM - 96 model file parameters
        self.NumbGeoidCols = 1441
        self.NumbGeoidRows = 721
        self.NumbHeaderItems = 6
        self.ScaleFactor = 4
        self.GeoidHeightBuffer = geoid_heiths_buffer
        self.NumbGeoidElevs = self.NumbGeoidCols * self.NumbGeoidRows
        self.Geoid_Initialized = 1
        if altitude_type == 'MLS':
            self.UseGeoid = 1
        else:
            self.UseGeoid = 0
