from mantid.simpleapi import *
from mantid.api import Projection

nexus_file='/SNS/users/rwp/HB2C_3000.nxs.h5'
output_directory='/tmp'
output_file=os.path.split(nexus_file)[-1].replace('.nxs.h5','')
ipts = nexus_file.split('/')[3]

ws = LoadEventNexus(Filename=nexus_file)
print(ws.getNumberEvents())
ws = Integration(ws)
MaskDetectors(ws,DetectorList=range(16384))
ws.getAxis(0).setUnit("Wavelength")
w = np.array([1.487,1.489])
tt0=time.time()
for idx in range(ws.getNumberHistograms()):
    ws.setX(idx, w)
tt1=time.time()
print(tt1-tt0)
SetGoniometer('ws', Axis0="HB2C:Mot:s1,0,1,0,1")
RemoveLogs('ws', KeepLogs="HB2C:Mot:s1")

ConvertToMD('ws', QDimensions='Q3D', dEAnalysisMode='Elastic', Q3DFrames='Q_sample', OutputWorkspace='md')

LoadIsawUB('ws','/SNS/users/rwp/wand/single4/nacl.mat')
ub=mtd['ws'].sample().getOrientedLattice().getUB().copy()

ConvertToMD('ws', QDimensions='Q3D', dEAnalysisMode='Elastic', Q3DFrames='HKL', OutputWorkspace='md1')

ol=ws.sample().getOrientedLattice()
q1=ol.qFromHKL([1,0,0])
q2=ol.qFromHKL([0,1,0])
q3=ol.qFromHKL([0,0,1])

BinMD(InputWorkspace='md1', AlignedDim0='[H,0,0],-0.5,0.5,11', AlignedDim1='[0,K,0],-10,10,101', AlignedDim2='[0,0,L],-10,10,101', OutputWorkspace='mdh1')
BinMD(InputWorkspace='md',AxisAligned=False,
BasisVector0='[H,0,0],A^-1,{},{},{}'.format(q1.X(),q1.Y(),q1.Z()),
BasisVector1='[0,K,0],A^-1,{},{},{}'.format(q2.X(),q2.Y(),q2.Z()),
BasisVector2='[0,0,L],A^-1,{},{},{}'.format(q3.X(),q3.Y(),q3.Z()),
OutputExtents=[-0.5,0.5,-10,10,-10,10], OutputBins=[11, 101, 101],
OutputWorkspace='mdh3')

ol2 = OrientedLattice()
ol2.setUB(ub)
q21 = ol2.qFromHKL([1, 0, 0])
q22 = ol2.qFromHKL([0, 1, 0])
q23 = ol2.qFromHKL([0, 0, 1])

print(q1, q21)
print(q2, q22)
print(q3, q23)

