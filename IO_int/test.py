from mantid.simpleapi import *
import numpy as np

van=LoadNexus('/HFIR/HB2C/IPTS-7776/shared/autoreduce/HB2C_{}.nxs'.format(6558))

y=van.extractY()
e=van.extractY()
s2=van.run().getLogData('HB2C:Mot:s2.RBV').timeAverageValue()
detz=van.run().getLogData('HB2C:Mot:detz.RBV').timeAverageValue()
s1=van.run().getLogData('HB2C:Mot:s1').timeAverageValue()
w=1.488

CreateWorkspace(OutputWorkspace='new', DataX=w, DataY=y, DataE=e, NSpec=y.size, UnitX='Wavelength')
SetGoniometer('new', Axis0="{},0,1,0,1".format(s2))
AddSampleLog('new', LogName='HB2C:Mot:s2.RBV', LogText=str(s2), LogType='Number Series')
AddSampleLog('new', LogName='HB2C:Mot:detz.RBV', LogText=str(detz), LogType='Number Series')
LoadInstrument('new', InstrumentName='WAND',RewriteSpectraMap=True)
# Masking
# Monitor count?




SetGoniometer('ws', Axis0="HB2C:Mot:s1,0,1,0,1")            
ws = Integration(ws)
MaskDetectors(ws,DetectorList=range(16384))
ws.getAxis(0).setUnit("Wavelength")
w = np.array([1.487,1.489])
for idx in xrange(ws.getNumberHistograms()):
    ws.setX(idx, w)
ConvertToMD('ws', QDimensions='Q3D', dEAnalysisMode='Elastic', Q3DFrames='HKL', QConversionScales='HKL', OutputWorkspace='md',MinValues='-10,-10,-10',MaxValues='10,10,10')
