#!/usr/bin/env python2
import sys
import numpy as np

sys.path.append("/opt/mantidnightly/bin")
from mantid.simpleapi import *
from mantid import logger

powder=False

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

ws=LoadWAND(filename)
if powder:
    SaveNexus('ws',os.path.join(output_directory,output_file+".nxs"))
ConvertToMD('ws', QDimensions='Q3D', dEAnalysisMode='Elastic', Q3DFrames='Q_sample', OutputWorkspace='md',MinValues='-10,-1,-10',MaxValues='10,1,10')
SaveMD('md',os.path.join(output_directory,output_file+"_MDE.nxs"))
