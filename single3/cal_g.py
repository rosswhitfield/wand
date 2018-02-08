import numpy as np
from mantid.simpleapi import *

w = np.array([1.487,1.489])


ws = LoadEventNexus(Filename='/HFIR/HB2C/IPTS-7776/nexus/HB2C_2972.nxs.h5')
ws = Integration(ws)
MaskDetectors(ws,DetectorList=range(16384))
ws.getAxis(0).setUnit("Wavelength")
w = np.array([1.487,1.489])
for idx in xrange(ws.getNumberHistograms()):
    ws.setX(idx, w)
SetGoniometer(ws, Axis0="HB2C:Mot:s1,0,1,0,1")
print(ws.run().getGoniometer().getR())

ConvertToMD(ws, QDimensions='Q3D', dEAnalysisMode='Elastic', Q3DFrames='Q_sample', OutputWorkspace='md_sample')
ConvertToMD(ws, QDimensions='Q3D', dEAnalysisMode='Elastic', Q3DFrames='Q_lab', OutputWorkspace='md_lab')

FindPeaksMD(InputWorkspace='md_sample', PeakDistanceThreshold=0.5, DensityThresholdFactor=500, OutputWorkspace='peaks')
FindPeaksMD(InputWorkspace='md_lab', PeakDistanceThreshold=0.5, DensityThresholdFactor=500, OutputWorkspace='peaks_lab')

p0=mtd['peaks'].getPeak(0)
print(p0.getQSampleFrame())
print(p0.getQLabFrame())
print(p0.getWavelength())
print(p0.getGoniometerMatrix())

k=2*np.pi/1.488
print(k)
q2=np.sum(np.square(p0.getQSampleFrame()))
print(q2)
twoTheta = mtd['md_lab'].getExperimentInfo(0).getInstrument().getDetector(p0.getDetectorID()).getTwoTheta(V3D(0,0,0),V3D(0,0,1))
print(twoTheta)
print(2*k**2*(1-np.cos(twoTheta)))
print(np.sqrt(q2/(2*(1-np.cos(twoTheta)))))


ql = p0.getQLabFrame()
qs = p0.getQSampleFrame()
g = p0.getGoniometerMatrix()
ql2 = np.dot(g, qs)
print(ql,ql2)
print(np.linalg.norm(ql),np.linalg.norm(qs))
print(qs)

norm_q=np.linalg.norm(ql)
refBeamFrame=mtd['md_lab'].getExperimentInfo(0).getInstrument().getReferenceFrame().vecPointingAlongBeam()
qBeam = np.dot(ql,refBeamFrame)
print(norm_q**2/2/qBeam)



k=2*np.pi/1.488
qs = p0.getQSampleFrame()

#cos(theta) = 1-Q^2/(2*k^2)
theta = np.arccos(1-np.linalg.norm(qs)**2/(2*k**2))
qsx=qs[0]
qsy=qs[1]
qsz=qs[2]
phi = np.arcsin(-qsy/(k*np.sin(theta)))
qlx = -k*np.sin(theta)*np.cos(phi)
qly = -k*np.sin(theta)*np.sin(phi)
qlz = k*(1-np.cos(theta))
print(qlx, qly, qlz)

r = np.arcsin((qlx-qlz*qsx/qsz)/(qsz*(1+qsx**2/qsz**2)))
print(r*180/np.pi)


q=np.linalg.inv([[qsx, qsz],[qsz, qsz]])*np.array([qlx, qlz])

