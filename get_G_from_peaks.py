import numpy as np

peak_ws = 'peaks'

k=2*np.pi/1.488

for n in range(mtd[peak_ws].getNumberPeaks()):
    peak = mtd[peak_ws].getPeak(n)
    qs=peak.getQSampleFrame()
    theta = np.arccos(1-np.linalg.norm(qs)**2/(2*k**2))
    qsx=qs[0]
    qsy=qs[1]
    qsz=qs[2]
    phi = np.arcsin(-qsy/(k*np.sin(theta)))
    qlx = -k*np.sin(theta)*np.cos(phi)
    qly = -k*np.sin(theta)*np.sin(phi)
    qlz = k*(1-np.cos(theta))
    q=np.dot(np.linalg.inv([[qsx, qsz],[qsz, -qsx]]),np.array([qlx, qlz]))
    r2 = np.arctan2(q[1], q[0])
    print("Peak Q Sample: {}, HKL: {}, Rot: {}".format(qs,peak.getHKL(),r2*180/np.pi))
