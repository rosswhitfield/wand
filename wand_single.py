from mantid.simpleapi import *

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
SetGoniometer(ws, Axis0="HB2C:Mot:s1,0,1,0,1")
ConvertToMD(ws, QDimensions='Q3D', dEAnalysisMode='Elastic', Q3DFrames='Q_sample', OutputWorkspace='md')


# Do multiple

if 'md' in mtd:
    mtd.remove('md')

for run in range(1059,1833,100):
    ws = LoadEventNexus(Filename='/HFIR/HB2C/IPTS-7776/nexus/HB2C_{}.nxs.h5'.format(run))
    ws = Integration(ws)
    MaskDetectors(ws,DetectorList=range(16384))
    ws.getAxis(0).setUnit("Wavelength")
    w = np.array([1.487,1.489])
    for idx in xrange(ws.getNumberHistograms()):
        ws.setX(idx, w)
    ws=ConvertToEventWorkspace(ws)
    SetGoniometer(ws, Axis0="HB2C:Mot:s1,0,1,0,1")
    ConvertToMD(ws, QDimensions='Q3D', dEAnalysisMode='Elastic', Q3DFrames='Q_sample', OutputWorkspace='md',OverwriteExisting=False,MinValues='-10,-10,-10',MaxValues='10,10,10')
