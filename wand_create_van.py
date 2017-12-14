import numpy as np
from mantid.simpleapi import *

van = LoadEventNexus(Filename='/HFIR/HB2C/IPTS-7776/nexus/HB2C_1035.nxs.h5')
van = Integration(van)
MaskDetectors(van,DetectorList=range(16384))
van.getAxis(0).setUnit("Wavelength")
w = np.array([1.487,1.489])
for idx in xrange(van.getNumberHistograms()):
    van.setX(idx, w)
van=ConvertToEventWorkspace(van)
SetGoniometer('van', Axis0="HB2C:Mot:s1,0,1,0,1")

SaveNexus('van', '/SNS/users/rwp/wand/HB2C_1035_van.nxs')
