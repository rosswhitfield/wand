from mantid.simpleapi import *
import numpy as np
import sys

E=36.9384

w = np.array([1.487,1.489])

for run in range(2952,4754):
    ws = LoadEventNexus(Filename='/HFIR/HB2C/IPTS-7776/nexus/HB2C_{}.nxs.h5'.format(run))
    ws = Integration(ws)
    MaskDetectors(ws,DetectorList=range(16384))
    ws.getAxis(0).setUnit("Wavelength")
    for idx in xrange(ws.getNumberHistograms()):
        ws.setX(idx, w)
    ws=ConvertUnits(ws, Target='DeltaE', EMode='Direct', EFixed=E)
    ws=Rebin(ws, Params='-0.1,0.2,0.3')
    SaveNXSPE(ws, Filename='/HFIR/HB2C/IPTS-7776/shared/rwp/nxspe2/HB2C_{}.nxspe'.format(run), Efixed=E, Psi=ws.getRun().getLogData('HB2C:Mot:s1').value[0])
