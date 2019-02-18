import numpy as np

for t in range(5,30):
    runNumbers='{}-{}'.format(95409+122*(t-5),95530+122*(t-5))
    print(t,runNumbers)
    LoadWANDSCD(IPTS=21442, RunNumbers=runNumbers, Grouping='4x4', OutputWorkspace='data_{}K'.format(t))
    ConvertWANDSCDtoQ(InputWorkspace='data_{}K'.format(t),
                      NormaliseBy='None', Frame='HKL',
                      BinningDim0='-0.1525,0.1525,61',
                      BinningDim1='0.8475,1.1525,61',
                      BinningDim2='-0.025,1.025,21',
                      OutputWorkspace='{}K'.format(t))
    DeleteWorkspace('data_{}K'.format(t))

output=CreateMDHistoWorkspace(4, SignalInput=[0]*61*61*21*25, ErrorInput=[0]*61*61*21*25,
                              Extents=[-0.1525,0.1525,0.8475,1.1525,-0.025,1.025,4.5,29.5],
                              NumberOfBins=[61, 61, 21, 25], Names=['[H,0,0]','[0,K,0]','[0,0,L]','temperature'], Units='A^-1,A^-1,A^-1,C')

signal=np.empty((61,61,21,25))
for n, t in enumerate(range(5,30)):
    signal[:,:,:,n]=mtd['{}K'.format(t)].getSignalArray()

output.setSignalArray(signal)

SaveMD(output,'/SNS/users/rwp/wand/IPTS-21442/skyrmion_4D.nxs')
#output=LoadMD('/SNS/users/rwp/wand/IPTS-21442/skyrmion_4D.nxs')
#SaveMDWorkspaceToVTK('output','/SNS/users/rwp/wand/IPTS-21442/skyrmion_4D.vts')
for n in range(output.getDimension(3).getNBins()):
    T=(output.getDimension(3).getX(n)+output.getDimension(3).getX(n+1))/2
    #SliceMDHisto(InputWorkspace='output', Start='10,10,0,{}'.format(n), End='51,51,21,{}'.format(n+1), OutputWorkspace='slice')
    IntegrateMDHistoWorkspace('output', P1Bin='-0.1,0,0.1',P2Bin='0.9,0,1.1',P4Bin='{},{}'.format(T-0.5,T+0.5), OutputWorkspace='slice')
    SaveMD('slice','/SNS/users/rwp/wand/IPTS-21442/skyrmion_{}K.nxs'.format(int(T)))
    SaveMDWorkspaceToVTK('slice','/SNS/users/rwp/wand/IPTS-21442/skyrmion_{}K.vts'.format(int(T)))

# 3D - 2D+T
#SliceMDHisto(InputWorkspace='output', Start='10,10,10,0', End='51,51,11,25', OutputWorkspace='slice')
IntegrateMDHistoWorkspace('output', P1Bin='-0.1,0,0.1',P2Bin='0.9,0,1.1',P3Bin='0.35,0.65', OutputWorkspace='slice')
SaveMD('slice','/SNS/users/rwp/wand/IPTS-21442/skyrmion_3D_T.nxs')
SaveMDWorkspaceToVTK('slice','/SNS/users/rwp/wand/IPTS-21442/skyrmion_3D_T.vts')
