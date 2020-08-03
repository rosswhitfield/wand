# import mantid algorithms, numpy and matplotlib
from mantid.simpleapi import *
import matplotlib.pyplot as plt
import numpy as np

runs = [225078, 225095]
vanadium = 368221

start=-6
end=6
step=2


van=LoadWAND('HB2C{}'.format(vanadium))

for run in runs:
    ws = LoadWAND('HB2C{}'.format(run), OutputWorkspace='HB2C_{}'.format(run))
    di=ws.detectorInfo()
    azimuthal = np.array([di.azimuthal(n) for n in range(di.size())])
    ws_list = []
    for phi_start in range(start, end, step):
        mask=np.where(np.logical_or(azimuthal<np.deg2rad(phi_start), azimuthal>np.deg2rad(phi_start+step)))[0]
        ws_name = '{}_from_{}_to_{}'.format(ws, phi_start, phi_start+step)
        ws_list.append(ws_name)
        CloneWorkspace(ws, OutputWorkspace=ws_name)
        MaskDetectors(ws_name, DetectorList=mask)
    ws_group = GroupWorkspaces(ws_list, OutputWorkspace='{}_group'.format(ws))
    ws_powder = WANDPowderReduction(ws_group, CalibrationWorkspace=van, Target='Theta', NumberBins=1000, OutputWorkspace='{}_powder'.format(ws))
    for w in ws_powder:
        SaveFocusedXYE(w, SplitFiles=False, IncludeHeader=False,
                       Filename='{}.xye'.format(w))
