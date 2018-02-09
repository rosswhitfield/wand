#!/usr/bin/env python2
import sys
import numpy as np
import time

from mantid.simpleapi import *

nexus_file='/HFIR/HB2C/IPTS-7776/nexus/HB2C_3000.nxs.h5'
output_directory='/tmp'
output_file=os.path.split(nexus_file)[-1].replace('.nxs.h5','')
ipts = nexus_file.split('/')[3]

ws = LoadEventNexus(Filename=nexus_file)
ws = Integration(ws)
MaskDetectors(ws,DetectorList=range(16384))
ws.getAxis(0).setUnit("Wavelength")
w = np.array([1.487,1.489])
for idx in xrange(ws.getNumberHistograms()):
    ws.setX(idx, w)
SetGoniometer('ws', Axis0="HB2C:Mot:s1,0,1,0,1")
SaveNexus('ws',os.path.join(output_directory,output_file+".nxs"))
ConvertToMD('ws', QDimensions='Q3D', dEAnalysisMode='Elastic', Q3DFrames='Q_sample', OutputWorkspace='md')
SaveMD('md',os.path.join(output_directory,output_file+"_MDE.nxs"))

# Group data
ws = GroupDetectors('ws', MapFile='/HFIR/HB2C/shared/autoreduce/HB2C_4x4.map')
SaveNexus('ws',os.path.join(output_directory,output_file+"_group_4x4.nxs"))
ConvertToMD('ws', QDimensions='Q3D', dEAnalysisMode='Elastic', Q3DFrames='Q_sample', OutputWorkspace='md')
SaveMD('md',os.path.join(output_directory,output_file+"_group_4x4_MDE.nxs"))
