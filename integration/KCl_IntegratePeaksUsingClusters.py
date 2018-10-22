LoadWANDSCD(IPTS='7776', RunNumbers='26613', OutputWorkspace='Vana_26613', Grouping='4x4')
LoadWANDSCD(IPTS='7776', RunNumbers='27976-29776', OutputWorkspace='KCl', Grouping='4x4')

q=ConvertWANDSCDtoQ(InputWorkspace='KCl', NormalisationWorkspace='Vana_26613', KeepTemporaryWorkspaces=True)

FindPeaksMD(InputWorkspace='q_data', PeakDistanceThreshold=0.5, MaxPeaks=100, DensityThresholdFactor=1000, CalculateGoniometerForCW=True, Wavelength=1.488, OutputWorkspace='peaks')

FindUBUsingLatticeParameters(PeaksWorkspace='peaks', a=6.292, b=6.292, c=6.292, alpha=90, beta=90, gamma=90)
IndexPeaks(PeaksWorkspace='peaks')

IntegratePeaksUsingClusters(InputWorkspace='q', PeaksWorkspace='peaks', Threshold=5000, OutputWorkspace='integrated', OutputWorkspaceMD='labeled')


q2=ConvertWANDSCDtoQ(InputWorkspace='KCl', NormalisationWorkspace='Vana_26613', KeepTemporaryWorkspaces=True, BinningDim0='-8.01,8.01,801', BinningDim1='-0.81,0.81,81', BinningDim2='-8.01,8.01,801')

FindPeaksMD(InputWorkspace='q2_data', PeakDistanceThreshold=0.5, MaxPeaks=100, DensityThresholdFactor=1800, CalculateGoniometerForCW=True, Wavelength=1.488, OutputWorkspace='peaks2')

FindUBUsingLatticeParameters(PeaksWorkspace='peaks2', a=6.292, b=6.292, c=6.292, alpha=90, beta=90, gamma=90)
IndexPeaks(PeaksWorkspace='peaks2')

IntegratePeaksUsingClusters(InputWorkspace='q2', PeaksWorkspace='peaks2', Threshold=60000, OutputWorkspace='integrated2', OutputWorkspaceMD='labeled2')

q2bck = mtd['q2']-0.2
IntegratePeaksUsingClusters(InputWorkspace='q2bck', PeaksWorkspace='peaks2', Threshold=60000, OutputWorkspace='integratedbkg2', OutputWorkspaceMD='labeledbkg2')
