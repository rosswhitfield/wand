from mantid.simpleapi import *

nexus_file='/SNS/users/rwp/HB2C_3000.nxs.h5'
output_directory='/tmp'
output_file=os.path.split(nexus_file)[-1].replace('.nxs.h5','')
ipts = nexus_file.split('/')[3]


ws=LoadNexus(os.path.join(output_directory,output_file+".nxs"))
md=LoadMD(os.path.join(output_directory,output_file+"_MDE.nxs"))

LoadIsawUB('ws','/SNS/users/rwp/wand/single4/nacl.mat')
ub=mtd['ws'].sample().getOrientedLattice().getUB().copy()

ConvertToMD('ws', QDimensions='Q3D', dEAnalysisMode='Elastic', Q3DFrames='HKL', OutputWorkspace='md1')

ConvertCWSDMDtoHKL('md', UBMatrix=ub, OutputWorkspace='md2')


BinMD(InputWorkspace='md1', AlignedDim0='[H,0,0],-0.5,0.5,11', AlignedDim1='[0,K,0],-10,10,101', AlignedDim2='[0,0,L],-10,10,101', OutputWorkspace='mdh1')
BinMD(InputWorkspace='md2', AlignedDim0='H,-0.5,0.5,11', AlignedDim1='K,-10,10,101', AlignedDim2='L,-10,10,101', OutputWorkspace='mdh2')

print(mtd['mdh1'].getSignalArray().sum())
print(mtd['mdh2'].getSignalArray().sum())

