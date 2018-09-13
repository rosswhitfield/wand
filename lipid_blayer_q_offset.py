import numpy as np

DPPC = LoadWANDSCD(IPTS='17751', RunNumbers='64974-65134')
s1 = np.asarray(DPPC.getExperimentInfo(0).run().getProperty('s1').value)

s1_offset = -45
DPPC.getExperimentInfo(0).run().addProperty('s1', list(s1+s1_offset), True)

ConvertWANDSCDtoQ(InputWorkspace='DPPC', OutputWorkspace='q')
