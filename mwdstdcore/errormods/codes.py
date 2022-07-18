def_pattern = ['ABX', 'ABY', 'ABZ', 'ASX', 'ASY', 'ASZ',
               'MBX', 'MBY', 'MBZ', 'MSX', 'MSY', 'MSZ',
               'MXY', 'MXZ', 'MYZ']
# ['ABX', 'ABY', 'ABZ', 'ASX', 'ASY', 'ASZ',
#  'MBX', 'MBY', 'MBZ', 'MSX', 'MSY', 'MSZ',
#  'MXY', 'MXZ', 'MYZ', 'MGI', 'MBI', 'MDI']


def_srv_stat = 'STD'  # STD, INC, BAD
srv_stat = {0: 'STD', 1: 'INC', 2: 'BAD'}
srv_stat_inv = {'STD': 0, 'INC': 1, 'BAD': 2}
def_fail_axis = 'none'  # none, AFX, AFY, AFZ, MFX, MFY, MFZ
faxis = {-1: 'none', 0: 'AFX', 1: 'AFY', 2: 'AFZ', 3: 'MFX', 4: 'MFY', 5: 'MFZ'}
faxis_inv = {'none': -1, 'AFX': 0, 'AFY': 1, 'AFZ': 2, 'MFX': 3, 'MFY': 4, 'MFZ': 5}