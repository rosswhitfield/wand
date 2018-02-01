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


norm_q=np.linalg.norm(ql)
refBeamFrame=mtd['md_lab'].getExperimentInfo(0).getInstrument().getReferenceFrame().vecPointingAlongBeam()
qBeam = np.dot(ql,refBeamFrame)
print(norm_q**2/2/qBeam)

i=mtd['md_lab'].getExperimentInfo(0).getInstrument()
for d in xrange(512*480*8):
    det=i.getDetector(d)
    phi=det.getPhi()
    theta=det.getTwoTheta(V3D(0,0,0),V3D(0,0,1))
    ql=[-k*np.sin(theta)*np.cos(phi), -k*np.sin(theta)*np.sin(phi), k*(1-np.cos(theta)]
    print(d,ql)
