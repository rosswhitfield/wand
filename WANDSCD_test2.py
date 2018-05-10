LoadWANDSCD(IPTS=7776, RunNumbers=26509, OutputWorkspace='norm')
#LoadWANDSCD(IPTS=7776, RunNumbers=','.join(str(n) for n in range(26640,27944,5)), OutputWorkspace='data')
LoadWANDSCD(IPTS=7776, RunNumbers='26640-27944', OutputWorkspace='data')
ConvertWANDSCDtoQ(InputWorkspace='data', NormalisationWorkspace='norm',OutputWorkspace='q_norm',BinningDim1='-0.81,0.81,81',BinningDim0='-8.01,8.01,801',BinningDim2='-8.01,8.01,801')
#ConvertWANDSCDtoQ(InputWorkspace='data', NormalisationWorkspace='norm',OutputWorkspace='q_norm_cut',BinningDim1='-0.2025,0.2025,81',BinningDim0='-0.025,6.025,121',BinningDim2='-5.025,5.025,201')
#ConvertWANDSCDtoQ(InputWorkspace='data', NormalisationWorkspace='norm',OutputWorkspace='q_norm_1',BinningDim1='-0.8,0.8,1')

FindPeaksMD(InputWorkspace='q_norm', PeakDistanceThreshold=2, MaxPeaks=100, CalculateGoniometerForCW=True, Wavelength=1.488, OutputWorkspace='peaks')
FindUBUsingLatticeParameters(PeaksWorkspace='peaks', a=5.64, b=5.64, c=5.64, alpha=90, beta=90, gamma=90)
ConvertWANDSCDtoQ(InputWorkspace='data', NormalisationWorkspace='norm',UBWorkspace='peaks',Frame='HKL',OutputWorkspace='hkl_norm',BinningDim0='-0.6,0.6,61',BinningDim2='-6.51,6.51,651',BinningDim1='-2.01,7.01,451')
#ConvertWANDSCDtoQ(InputWorkspace='data', NormalisationWorkspace='norm',UBWorkspace='peaks',Frame='HKL',OutputWorkspace='hkl_norm',BinningDim2='-0.6,0.6,61',BinningDim0='-6.51,6.51,651',BinningDim1='-2.01,7.01,451')


LoadWANDSCD(IPTS=7776, RunNumbers=26509, OutputWorkspace='norm')
LoadWANDSCD(IPTS=7776, RunNumbers=','.join(str(n) for n in range(26640,27944,5)), OutputWorkspace='data')
ConvertWANDSCDtoQ(InputWorkspace='data', NormalisationWorkspace='norm',OutputWorkspace='q_norm',KeepTemporaryWorkspaces=True)
ConvertWANDSCDtoQ(InputWorkspace='data',OutputWorkspace='q',KeepTemporaryWorkspaces=True)
ConvertWANDSCDtoQ(InputWorkspace='data',OutputWorkspace='q2',KeepTemporaryWorkspaces=True,NormaliseBy='None')

FindPeaksMD(InputWorkspace='q_norm', PeakDistanceThreshold=2, MaxPeaks=100, CalculateGoniometerForCW=True, Wavelength=1.488, OutputWorkspace='peaks')
FindUBUsingLatticeParameters(PeaksWorkspace='peaks', a=5.64, b=5.64, c=5.64, alpha=90, beta=90, gamma=90)
ConvertWANDSCDtoQ(InputWorkspace='data', NormalisationWorkspace='norm',UBWorkspace='peaks',Frame='HKL',OutputWorkspace='hkl_norm',BinningDim0='-0.6,0.6,61',BinningDim2='-6.51,6.51,651',BinningDim1='-2.01,7.01,451',KeepTemporaryWorkspaces=True)








LoadWANDSCD(IPTS=7776, RunNumbers=26509, OutputWorkspace='norm',Grouping='4x4')
LoadWANDSCD(IPTS=7776, RunNumbers='26640-27944', OutputWorkspace='data',Grouping='4x4')
ConvertWANDSCDtoQ(InputWorkspace='data', NormalisationWorkspace='norm',OutputWorkspace='q_norm',KeepTemporaryWorkspaces=True)
ConvertWANDSCDtoQ(InputWorkspace='data', NormalisationWorkspace='norm',OutputWorkspace='q_norm2',BinningDim1='-0.81,0.81,81',BinningDim0='-8.01,8.01,801',BinningDim2='-8.01,8.01,801')


FindPeaksMD(InputWorkspace='q_norm2', PeakDistanceThreshold=2, MaxPeaks=100, CalculateGoniometerForCW=True, Wavelength=1.488, OutputWorkspace='peaks')
FindUBUsingLatticeParameters(PeaksWorkspace='peaks', a=5.64, b=5.64, c=5.64, alpha=90, beta=90, gamma=90)
ConvertWANDSCDtoQ(InputWorkspace='data',NormalisationWorkspace='norm',UBWorkspace='peaks',Frame='HKL',OutputWorkspace='hkl_norm',BinningDim0='-0.6,0.6,61',BinningDim2='-6.51,6.51,651',BinningDim1='-2.01,7.01,451',KeepTemporaryWorkspaces=True)
