#!/usr/bin/env python2
import sys
import numpy as np

sys.path.append("/opt/mantidnightly/bin")
from mantid.simpleapi import *
from mantid import logger

if (len(sys.argv) != 3): 
    logger.error("autoreduction code requires a filename and an output directory")
    sys.exit()
if not(os.path.isfile(sys.argv[1])):
    logger.error("data file "+sys.argv[1]+ " not found")
    sys.exit()    
else:
    filename = sys.argv[1]
    outdir = sys.argv[2]
nexus_file=sys.argv[1]
output_directory=sys.argv[2]
output_file=os.path.split(nexus_file)[-1].replace('.nxs.h5','')
ipts = nexus_file.split('/')[3]

ws, mon = LoadEventNexus(Filename=filename, LoadMonitors=True)
ws = Integration(ws)
MaskDetectors(ws,DetectorList=range(16384))
ws.getAxis(0).setUnit("Wavelength")
w = np.array([1.487,1.489])
for idx in xrange(ws.getNumberHistograms()):
    ws.setX(idx, w)
SetGoniometer('ws', Axis0="HB2C:Mot:s1,0,1,0,1")
AddSampleLog(ws,LogName="gd_prtn_chrg",LogType='Number',NumberType='Double',
             LogText=str(mon.getNumberEvents()))
SaveNexus('ws',os.path.join(output_directory,output_file+".nxs"))
ConvertToMD('ws', QDimensions='Q3D', dEAnalysisMode='Elastic', Q3DFrames='Q_sample', OutputWorkspace='md',MinValues='-10,-1,-10',MaxValues='10,1,10')
SaveMD('md',os.path.join(output_directory,output_file+"_MDE.nxs"))

# Group data
"""
ws = GroupDetectors('ws', MapFile='/HFIR/HB2C/shared/autoreduce/HB2C_4x4.map')
SaveNexus('ws',os.path.join(output_directory,output_file+"_group_4x4.nxs"))
ConvertToMD('ws', QDimensions='Q3D', dEAnalysisMode='Elastic', Q3DFrames='Q_sample', OutputWorkspace='md')
SaveMD('md',os.path.join(output_directory,output_file+"_group_4x4_MDE.nxs"))
"""
