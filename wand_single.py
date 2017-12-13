from mantid.simpleapi import *
from mantid.api import NumericAxis

van = LoadEventNexus(Filename='/HFIR/HB2C/IPTS-7776/nexus/HB2C_1035.nxs.h5')
van = Integration(van)
MaskDetectors(van,DetectorList=range(16384))

ws = LoadEventNexus(Filename='/HFIR/HB2C/IPTS-7776/nexus/HB2C_1078.nxs.h5')
ws = Integration(ws)
MaskDetectors(ws,DetectorList=range(16384))


ws.getAxis(0).setUnit("Wavelength")
w = np.array([1.487,1.489])
for idx in xrange(ws.getNumberHistograms()):
    ws.setX(idx, w)
ws=ConvertToEventWorkspace(ws)
