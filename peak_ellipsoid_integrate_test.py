from mantid.simpleapi import *
from mantid.kernel import V3D

import numpy as np

X_lim = [-5,5]
Y_lim = [-5,5]
Z_lim = [-5,5]

N = 1000000

mux, muy, muz = 1, 2, 3
sigmax, sigmay, sigmaz = 0.1, 0.1, 0.5

exts = str(X_lim[0])+','+str(X_lim[1])+','+str(Y_lim[0])+','+str(Y_lim[1])+','+str(Z_lim[0])+','+str(Z_lim[1])

ws = CreateMDWorkspace(Dimensions='3', \
                       EventType='MDEvent',\
                       Extents=exts,\
                       Names='Q_lab_x,Q_lab_y,Q_lab_z',\
                       Units='MomentumTransfer,MomentumTransfer,MomentumTransfer',
                       Frames='QLab,QLab,QLab')
                       
params = str(N)+','+str(mux)+','+str(muy)+','+str(muz)+',1,0,0,0,1,0,0,0,1,'+str(sigmax**2)+','+str(sigmay**2)+','+str(sigmaz**2)+',0'
                       
FakeMDEventData(ws, EllipsoidParams=params)

inst_dir = config.getInstrumentDirectory()
sxd_ws = LoadEmptyInstrument(os.path.join(inst_dir, "SXD_Definition.xml"))
AddSampleLog(sxd_ws, 'run_number', '1', 'Number')

peak_ws = CreatePeaksWorkspace(InstrumentWorkspace=sxd_ws, NumberOfPeaks=0)

a, b, c = 1, 1, 1
alpha, beta, gamma = 90, 90, 90

SetUB(peak_ws, a=a, b=b, c=c, alpha=alpha, beta=beta, gamma=gamma)
#SetUB(peak_ws, UB='1,0,0,0,1,0,0,0,1')

qlab = V3D(mux, muy, muz)
p = peak_ws.createPeak(qlab)
peak_ws.addPeak(p)


IntegratePeaksMD(InputWorkspace=ws,
                 PeaksWorkspace='peak_ws',
                 PeakRadius=1,
                 OutputWorkspace='int')

IntegratePeaksMD(InputWorkspace=ws,
                 PeaksWorkspace='peak_ws',
                 PeakRadius=1,
                 Ellipsoid=True,
                 OutputWorkspace='int_ellipsoid')
