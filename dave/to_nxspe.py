from mantid.simpleapi import *
import numpy as np
import sys

run=2952

E=36.9384

w = np.array([1.487,1.489])
van=LoadNexus('/SNS/users/rwp/wand/HB2C_2933_Van_processed.nxs')

ws = LoadEventNexus(Filename='/HFIR/HB2C/IPTS-7776/nexus/HB2C_{}.nxs.h5'.format(run))
ws = Integration(ws)
MaskDetectors(ws,DetectorList=range(16384))
ws.getAxis(0).setUnit("Wavelength")
w = np.array([1.487,1.489])
for idx in xrange(ws.getNumberHistograms()):
    ws.setX(idx, w)
ws=ConvertUnits(ws, Target='DeltaE', EMode='Direct', EFixed=E)
ws=Rebin(ws, Params='-0.1,0.2,0.3', PreserveEvents=False)
SaveNXSPE(ws, Filename='/HFIR/HB2C/IPTS-7776/shared/rwp/nxspe/HB2C_{}.nxspe'.format(run), Efixed=E, Psi=ws.getRun().getLogData('HB2C:Mot:s1').value[0])
