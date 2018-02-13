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

ConvertCWSDMDtoHKL('md', UBMatrix=ub, OutputWorkspace='md2')

proj_id = Projection([1,0,0], [0,1,0], [0,0,1])
proj_ws = proj_id.createWorkspace()
SetUB('md',UB=ub)
md3=CutMD(InputWorkspace='md',Projection=proj_ws, PBins=([-10, 0.05,10], [-10,0.05,10],[-10,0.05,10]),InterpretQDimensionUnits= 'Q in A^-1',NoPix=True)


BinMD(InputWorkspace='md1', AlignedDim0='[H,0,0],-0.5,0.5,11', AlignedDim1='[0,K,0],-10,10,101', AlignedDim2='[0,0,L],-10,10,101', OutputWorkspace='mdh1')
BinMD(InputWorkspace='md2', AlignedDim0='H,-0.5,0.5,11', AlignedDim1='K,-10,10,101', AlignedDim2='L,-10,10,101', OutputWorkspace='mdh2')

print(mtd['mdh1'].getSignalArray().sum())
print(mtd['mdh2'].getSignalArray().sum())

