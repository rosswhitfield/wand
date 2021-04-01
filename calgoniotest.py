from mantid.geometry import Goniometer
from mantid.kernel import V3D, FloatTimeSeriesProperty
import numpy as np
from mantid.simpleapi import CreatePeaksWorkspace, HFIRCalculateGoniometer, AddTimeSeriesLog, LoadEmptyInstrument

omega = np.deg2rad(42)

R = np.array([[np.cos(omega), 0, np.sin(omega)],
              [0, 1, 0],
              [-np.sin(omega), 0, np.cos(omega)]])

wl = 1.54
k = 2*np.pi/wl
theta = np.deg2rad(47)
phi = np.deg2rad(13)

q_lab = np.array([-np.sin(theta)*np.cos(phi),
                   -np.sin(theta)*np.sin(phi),
                   1 - np.cos(theta)]) * k

q_sample = np.dot(np.linalg.inv(R), q_lab)

peaks = CreatePeaksWorkspace(OutputType="LeanElasticPeak", NumberOfPeaks=0)

p = peaks.createPeakQSample(q_sample)
peaks.addPeak(p)

HFIRCalculateGoniometer(peaks, wl, OverrideProperty=True, InnerGoniometer=True)

g = Goniometer()
g.setR(peaks.getPeak(0).getGoniometerMatrix())
print(g.getEulerAngles('YZY'))
assert np.isclose(g.getEulerAngles('YZY')[0], 42)


chi = np.deg2rad(-3)
phi = np.deg2rad(23)

R1 = np.array([[np.cos(omega), 0, -np.sin(omega)], # omega 0,1,0,-1
               [               0, 1,                 0],
               [np.sin(omega), 0,  np.cos(omega)]])
R2 = np.array([[ np.cos(chi),  np.sin(chi), 0], # chi 0,0,1,-1
               [-np.sin(chi),  np.cos(chi), 0],
               [              0,               0, 1]])
R3 = np.array([[np.cos(phi), 0, -np.sin(phi)], # phi 0,1,0,-1
               [             0, 1,               0],
               [np.sin(phi), 0,  np.cos(phi)]])
R = np.dot(np.dot(R1, R2), R3)

q_sample = np.dot(np.linalg.inv(R), q_lab)


peaks = CreatePeaksWorkspace(OutputType="LeanElasticPeak", NumberOfPeaks=0)

p = peaks.createPeakQSample(q_sample)
p.setGoniometerMatrix(np.dot(R2, R3))
peaks.addPeak(p)

HFIRCalculateGoniometer(peaks, wl)

g = Goniometer()
g.setR(peaks.getPeak(0).getGoniometerMatrix())
print(g.getEulerAngles('YZY'))
assert np.isclose(g.getEulerAngles('YZY')[0], -42)
assert np.isclose(g.getEulerAngles('YZY')[1], 3)
assert np.isclose(g.getEulerAngles('YZY')[2], -23)


peaks = CreatePeaksWorkspace(NumberOfPeaks=0, OutputType="LeanElasticPeak")

#peaks.run().getGoniometer().setR(np.dot(R1, R2))
peaks.run().getGoniometer().setR(R)
p = peaks.createPeakQSample(q_sample)
peaks.addPeak(p)

HFIRCalculateGoniometer(peaks, wl, OverrideProperty=True, InnerGoniometer=True)

g = Goniometer()
g.setR(peaks.getPeak(0).getGoniometerMatrix())
print(g.getEulerAngles('YZY'))
assert np.isclose(g.getEulerAngles('YZY')[0], -42)
assert np.isclose(g.getEulerAngles('YZY')[1], 3)
assert np.isclose(g.getEulerAngles('YZY')[2], -23)
