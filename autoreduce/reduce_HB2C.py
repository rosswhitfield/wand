#!/usr/bin/env python2
import os
import sys

sys.path.append("/opt/mantidnightly/bin") # noqa
from mantid.simpleapi import *
from mantid import logger

powder = True

if (len(sys.argv) != 3): 
    logger.error("autoreduction code requires a filename and an output directory")
    sys.exit()
if not(os.path.isfile(sys.argv[1])):
    logger.error("data file " + sys.argv[1] + " not found")
    sys.exit()    
else:
    filename = sys.argv[1]
    outdir = sys.argv[2]
nexus_file = sys.argv[1]
output_directory = sys.argv[2]
output_file = os.path.split(nexus_file)[-1].replace('.nxs.h5','')

ws = LoadWAND(filename)
ConvertToMD('ws', QDimensions='Q3D', dEAnalysisMode='Elastic', Q3DFrames='Q_sample', OutputWorkspace='md',MinValues='-10,-1,-10',MaxValues='10,1,10')
SaveMD('md',os.path.join(output_directory,output_file+"_MDE.nxs"))

if powder:
    #SaveNexus('ws',os.path.join(output_directory,output_file+".nxs"))
    runNumber = mtd['ws'].getRunNumber()
    ConvertSpectrumAxis(InputWorkspace='ws', Target='Theta', OutputWorkspace='ws')
    Transpose(InputWorkspace='ws', OutputWorkspace='ws')
    ResampleX(InputWorkspace='ws', OutputWorkspace='ws', XMin=1, XMax=179, NumberBins=3561)
    div = SavePlot1D('ws', OutputType='plotly')
    from finddata import publish_plot
    request = publish_plot('HB2C', runNumber, files={'file': div})
    print("post returned %d" % request.status_code)
    print("resulting document:")
    print(request.text)

