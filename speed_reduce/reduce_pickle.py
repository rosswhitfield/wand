#!/usr/bin/env python2
import sys
import numpy as np
import time

from mantid.simpleapi import *
from mantid import logger

t0=time.time()
nexus_file='/HFIR/HB2C/IPTS-7776/nexus/HB2C_3000.nxs.h5' # Samll ~25sec
#nexus_file='/HFIR/HB2C/IPTS-7776/nexus/HB2C_6578.nxs.h5' # Si ~1000sec
#nexus_file='/HFIR/HB2C/IPTS-7776/nexus/HB2C_6586.nxs.h5' # V ~18380sec
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
RemoveLogs('ws', KeepLogs="HB2C:Mot:s1")
#ws=Transpose('ws')
t1=time.time()
SaveNexus('ws',os.path.join(output_directory,output_file+".nxs"))
t2=time.time()
ConvertToMD('ws', QDimensions='Q3D', dEAnalysisMode='Elastic', Q3DFrames='Q_sample', OutputWorkspace='md')
t3=time.time()
SaveMD('md',os.path.join(output_directory,output_file+"_MDE.nxs"))
t4=time.time()

# Group data
ws = GroupDetectors('ws', MapFile='/HFIR/HB2C/shared/autoreduce/HB2C_4x4.map')
t5=time.time()
SaveNexus('ws',os.path.join(output_directory,output_file+"_group_4x4.nxs"))
t6=time.time()
ConvertToMD('ws', QDimensions='Q3D', dEAnalysisMode='Elastic', Q3DFrames='Q_sample', OutputWorkspace='md')
t7=time.time()
SaveMD('md',os.path.join(output_directory,output_file+"_group_4x4_MDE.nxs"))
t8=time.time()

logger.notice('t1={}'.format(t1-t0))
logger.notice('t2={}'.format(t2-t1))
logger.notice('t3={}'.format(t3-t2))
logger.notice('t4={}'.format(t4-t3))
logger.notice('t5={}'.format(t5-t4))
logger.notice('t6={}'.format(t6-t5))
logger.notice('t7={}'.format(t7-t6))
logger.notice('t8={}'.format(t8-t7))


t10=time.time()
ws=LoadNexus(os.path.join(output_directory,output_file+".nxs"))
t11=time.time()
md=LoadMD(os.path.join(output_directory,output_file+"_MDE.nxs"))
t12=time.time()
ws=LoadNexus(os.path.join(output_directory,output_file+"_group_4x4.nxs"))
t13=time.time()
md=LoadMD(os.path.join(output_directory,output_file+"_group_4x4_MDE.nxs"))
t14=time.time()

logger.notice('t11={}'.format(t11-t10))
logger.notice('t12={}'.format(t12-t11))
logger.notice('t13={}'.format(t13-t12))
logger.notice('t14={}'.format(t14-t13))
