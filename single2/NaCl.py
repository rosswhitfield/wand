import numpy as np
from mantid.simpleapi import *

van = LoadEventNexus(Filename='/HFIR/HB2C/IPTS-7776/nexus/HB2C_2933.nxs.h5')
van = Integration(van)
MaskDetectors(van,DetectorList=range(16384))
van.getAxis(0).setUnit("Wavelength")
w = np.array([1.487,1.489])
for idx in xrange(van.getNumberHistograms()):
    van.setX(idx, w)
SetGoniometer('van', Axis0="HB2C:Mot:s1,0,1,0,1")
SaveNexus('van','/SNS/users/rwp/wand/HB2C_2933_Van_processed.nxs')

#NaCl 2952 - 4753

ws = LoadEventNexus(Filename='/HFIR/HB2C/IPTS-7776/nexus/HB2C_2952.nxs.h5')
ws = Integration(ws)
MaskDetectors(ws,DetectorList=range(16384))

ws.getAxis(0).setUnit("Wavelength")
w = np.array([1.487,1.489])
for idx in xrange(ws.getNumberHistograms()):
    ws.setX(idx, w)
SetGoniometer(ws, Axis0="HB2C:Mot:s1,0,1,0,1")

ConvertToMD(ws, QDimensions='Q3D', dEAnalysisMode='Elastic', Q3DFrames='Q_sample', OutputWorkspace='md')

# Do multiple

if 'md' in mtd:
    mtd.remove('md')
    
if 'van_md' in mtd:
    mtd.remove('van_md')

for run in range(2952,4755,100):
    ws = LoadEventNexus(Filename='/HFIR/HB2C/IPTS-7776/nexus/HB2C_{}.nxs.h5'.format(run))
    ws = Integration(ws)
    MaskDetectors(ws,DetectorList=range(16384))
    ws.getAxis(0).setUnit("Wavelength")
    for idx in xrange(ws.getNumberHistograms()):
        ws.setX(idx, w)
    SetGoniometer('ws', Axis0="HB2C:Mot:s1,0,1,0,1")
    ConvertToMD('ws', QDimensions='Q3D', dEAnalysisMode='Elastic', Q3DFrames='Q_sample', OutputWorkspace='md',OverwriteExisting=False,MinValues='-10,-10,-10',MaxValues='10,10,10')
    # Van, copy goniometer
    mtd['van'].run().getGoniometer().setR(mtd['ws'].run().getGoniometer().getR())
    ConvertToMD('van', QDimensions='Q3D', dEAnalysisMode='Elastic', Q3DFrames='Q_sample', OutputWorkspace='van_md',OverwriteExisting=False,MinValues='-10,-10,-10',MaxValues='10,10,10')

SaveMD('md', '/SNS/users/rwp/wand/NaCl_data_MDE.nxs')
SaveMD('van_md', '/SNS/users/rwp/wand/NaCl_van_MDE.nxs')
mdh = BinMD(InputWorkspace='md', AlignedDim0='Q_sample_x,-10,10,401', AlignedDim1='Q_sample_y,-1,1,41', AlignedDim2='Q_sample_z,-10,10,401')
van_mdh = BinMD(InputWorkspace='van_md', AlignedDim0='Q_sample_x,-10,10,401', AlignedDim1='Q_sample_y,-1,1,41', AlignedDim2='Q_sample_z,-10,10,401')
norm = mdh/van_mdh
SaveMD('mdh', '/SNS/users/rwp/wand/NaCl_data_MDH.nxs')
SaveMD('van_mdh', '/SNS/users/rwp/wand/NaCl_van_MDH.nxs')
SaveMD('norm', '/SNS/users/rwp/wand/NaCl_norm_MDH.nxs')


# md=LoadMD('/SNS/users/rwp/wand/NaCl_data_MDE.nxs', LoadHistory=False)
# van_md=LoadMD('/SNS/users/rwp/wand/NaCl_van_MDE.nxs', LoadHistory=False)
# mdh=LoadMD('/SNS/users/rwp/wand/NaCl_data_MDH.nxs', LoadHistory=False)
# van_mdh=LoadMD('/SNS/users/rwp/wand/NaCl_van_MDH.nxs', LoadHistory=False)
# norm=LoadMD('/SNS/users/rwp/wand/NaCl_norm_MDH.nxs', LoadHistory=False)
