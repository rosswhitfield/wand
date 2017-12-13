from mantid.simpleapi import *
from mantid.api import NumericAxis

van = LoadEventNexus(Filename='/HFIR/HB2C/IPTS-7776/nexus/HB2C_1035.nxs.h5')
van = Integration(van)
MaskDetectors(van,DetectorList=range(16384))

ws = LoadEventNexus(Filename='/HFIR/HB2C/IPTS-7776/nexus/HB2C_1078.nxs.h5')
ws = Integration(ws)
MaskDetectors(ws,DetectorList=range(16384))


newAxis = NumericAxis.create(ws.getNumberHistograms())
newAxis.setUnit("Label").setLabel("Wavelength", "Angstrom")

for idx in range(ws.getNumberHistograms()):
    newAxis.setValue(idx, 1.488)

ws.replaceAxis(1, newAxis)
