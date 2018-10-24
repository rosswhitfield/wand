import numpy as np

peaks = mtd['peaks']
data = mtd['NaCl'].getSignalArray()

dx = dy = 20

lines = []

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
output = CreateWorkspace(DataY=lines,DataX=range(len(lines[0])), NSpec=len(lines))
