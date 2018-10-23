LoadWANDSCD(IPTS='7776', RunNumbers='26613', OutputWorkspace='Vana_26613', Grouping='4x4')
LoadWANDSCD(IPTS='7776', RunNumbers='26640-27944', OutputWorkspace='NaCl', Grouping='4x4')

q=ConvertWANDSCDtoQ(InputWorkspace='NaCl', NormalisationWorkspace='Vana_26613', KeepTemporaryWorkspaces=True)

FindPeaksMD(InputWorkspace='q_data', PeakDistanceThreshold=0.5, MaxPeaks=100, DensityThresholdFactor=250, CalculateGoniometerForCW=True, Wavelength=1.488, OutputWorkspace='peaks')

FindUBUsingLatticeParameters(PeaksWorkspace='peaks', a=5.6418, b=5.6418, c=5.6418, alpha=90, beta=90, gamma=90)
IndexPeaks(PeaksWorkspace='peaks')

IntegratePeaksUsingClusters(InputWorkspace='q', PeaksWorkspace='peaks', Threshold=10000, OutputWorkspace='integrated', OutputWorkspaceMD='labeled')


q2=ConvertWANDSCDtoQ(InputWorkspace='NaCl', NormalisationWorkspace='Vana_26613', KeepTemporaryWorkspaces=True, BinningDim0='-8.01,8.01,801', BinningDim1='-1.21,0.41,81', BinningDim2='-8.01,8.01,801')

FindPeaksMD(InputWorkspace='q2_data', PeakDistanceThreshold=0.5, MaxPeaks=100, DensityThresholdFactor=1300, CalculateGoniometerForCW=True, Wavelength=1.488, OutputWorkspace='peaks2')

FindUBUsingLatticeParameters(PeaksWorkspace='peaks2', a=5.6418, b=5.6418, c=5.6418, alpha=90, beta=90, gamma=90)
IndexPeaks(PeaksWorkspace='peaks2')

IntegratePeaksUsingClusters(InputWorkspace='q2', PeaksWorkspace='peaks2', Threshold=60000, OutputWorkspace='integrated2', OutputWorkspaceMD='labeled2')




# IntegratePeaksMDHKL


hkl=ConvertWANDSCDtoQ(InputWorkspace='NaCl', NormalisationWorkspace='Vana_26613', UBWorkspace='peaks', Frame='HKL',BinningDim0='-0.82,0.82,41',BinningDim1='-8.02,8.02,401',BinningDim2='-8.02,8.02,401')

IntegratePeaksMDHKL(InputWorkspace='hkl', PeaksWorkspace='peaks', OutputWorkspace='hkl_integrated', DeltaHKL=0.5, NeighborPoints=10)


hkl2=ConvertWANDSCDtoQ(InputWorkspace='NaCl', NormalisationWorkspace='Vana_26613', UBWorkspace='peaks2', Frame='HKL',BinningDim0='-1.21,0.41,81',BinningDim1='-8.01,8.01,801',BinningDim2='-8.01,8.01,801')

IntegratePeaksMDHKL(InputWorkspace='hkl2', PeaksWorkspace='peaks2', OutputWorkspace='hkl_integrated2', DeltaHKL=0.5, NeighborPoints=10)
IntegratePeaksMDHKL(InputWorkspace='hkl2', PeaksWorkspace='peaks2', OutputWorkspace='hkl_integrated2_0.001', DeltaHKL=0.5, NeighborPoints=10, MinimumScale=0.001)

