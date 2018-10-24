import numpy as np

LoadWANDSCD(IPTS='7776', RunNumbers='26613', OutputWorkspace='Vana_26613', Grouping='4x4')
LoadWANDSCD(IPTS='7776', RunNumbers='26640-27944', OutputWorkspace='NaCl', Grouping='4x4')

q=ConvertWANDSCDtoQ(InputWorkspace='NaCl', NormalisationWorkspace='Vana_26613', KeepTemporaryWorkspaces=True)
FindPeaksMD(InputWorkspace='q_data', PeakDistanceThreshold=0.5, MaxPeaks=100, DensityThresholdFactor=250, CalculateGoniometerForCW=True, Wavelength=1.488, OutputWorkspace='peaks')

FindUBUsingLatticeParameters(PeaksWorkspace='peaks', a=5.6418, b=5.6418, c=5.6418, alpha=90, beta=90, gamma=90)
IndexPeaks(PeaksWorkspace='peaks')

# Normalise
ReplicateMD(ShapeWorkspace='NaCl', DataWorkspace='Vana_26613', OutputWorkspace='Vana_26613')
DivideMD(LHSWorkspace='NaCl', RHSWorkspace='Vana_26613', OutputWorkspace='NaCl')

peaks = mtd['peaks']

dx = dy = 20

lines = []

# Integrate each peak to get a line
for p in range(peaks.getNumberPeaks()):
    peak = peaks.getPeak(p)
    g = peak.getGoniometerMatrix()
    detID = peak.getDetectorID()
    x=detID//(4*4*128)-1
    y=detID%(4*128)//4-1
    print(detID, peak.getQSampleFrame(), np.mod(np.arctan(g[0,2]/g[0,0])*180/np.pi,-180), x, y)
    line = IntegrateMDHistoWorkspace('NaCl',
                                     P1Bin='{},{}'.format(y-dy, y+dy),
                                     P2Bin='{},{}'.format(x-dx, x+dx))
    lines.append(line.getSignalArray().flatten())
    
lines = np.array(lines)
lines = CreateWorkspace(DataY=lines,DataX=range(len(lines[0])), NSpec=len(lines))

s1 = np.array(mtd['NaCl'].getExperimentInfo(0).run().getProperty('s1').value)

# FitPeaks with Gaussian and integrate
for p in range(peaks.getNumberPeaks()):
    peak = peaks.getPeak(p)
    g = peak.getGoniometerMatrix()
    s1_index = np.searchsorted(s1, np.mod(np.arctan(g[0,2]/g[0,0])*180/np.pi,-180))
    FitPeak(InputWorkspace=lines,
                OutputWorkspace='peak_{}'.format(p),
                ParameterTableWorkspace='param_{}'.format(p),
                WorkspaceIndex=p,
                PeakFunctionType='Gaussian (Height, PeakCentre, Sigma)',
                PeakParameterValues='30000,{},10'.format(s1_index),
                BackgroundType='Flat (A0)',
                BackgroundParameterValues='200',
                FitWindow='{},{}'.format(s1_index-20, s1_index+20),
                PeakRange='{},{}'.format(s1_index-10, s1_index+10))
    height = mtd['param_{}'.format(p)].cell(2,1)
    sigma = mtd['param_{}'.format(p)].cell(4,1)
    peak.setIntensity(height*sigma*np.sqrt(2*np.pi))
