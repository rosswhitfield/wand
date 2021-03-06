LoadWANDSCD(IPTS='7776', RunNumbers='124736', OutputWorkspace='Vana_124736')
LoadWANDSCD(IPTS='21680', RunNumbers='122935-124735', OutputWorkspace='Er2Ge2O7')
ConvertWANDSCDtoQ(InputWorkspace='Er2Ge2O7', NormalisationWorkspace='Vana_124736', UBWorkspace='Er2Ge2O7', Wavelength='1.486', Vproj='0,0,1', Wproj='0,1,0', BinningDim0='-4.3,7.4,1201', BinningDim1='-1.1,1.1,51', BinningDim2='-6,7.4,1201', OutputWorkspace='q')
IntegrateMDHistoWorkspace(InputWorkspace='q', P2Bin='-0.97,0,0.07', OutputWorkspace='q2')
PredictPeaks(InputWorkspace='q', CalculateGoniometerForCW=True, Wavelength=1.488, MaxAngle=0, OutputWorkspace='predict')
IntegratePeaksUsingClusters(InputWorkspace='q2', PeaksWorkspace='predict', Threshold=25000, OutputWorkspace='integrated', OutputWorkspaceMD='labeled')
SaveHKL('integrated', Filename='/SNS/users/rwp/wand/integration/file.hkl')
SaveReflections('integrated', Filename='/SNS/users/rwp/wand/integration/peaks.hkl')



q=LoadMD('/SNS/users/rwp/Er2Ge2O7_q.nxs')
