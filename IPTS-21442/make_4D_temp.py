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

    
