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
t1=time.time()
SaveNexus('ws',os.path.join(output_directory,output_file+".nxs"))
t2=time.time()
ws=Transpose('ws')
t3=time.time()
SaveNexus('ws',os.path.join(output_directory,output_file+"_T.nxs"))
t4=time.time()


logger.notice('t1={}'.format(t1-t0))
logger.notice('t2={}'.format(t2-t1))
logger.notice('t3={}'.format(t3-t2))
logger.notice('t4={}'.format(t4-t3))


t10=time.time()
ws=LoadNexus(os.path.join(output_directory,output_file+".nxs"))
t11=time.time()
ws_T=LoadNexus(os.path.join(output_directory,output_file+"_T.nxs"))
t12=time.time()
ws_T=Transpose('ws_T')
t13=time.time()
for s in xrange(ws_T.getNPoints()):
    ws_T.getSpectrum(s).setDetectorID(s)
t14=time.time()


logger.notice('t11={}'.format(t11-t10))
logger.notice('t12={}'.format(t12-t11))
logger.notice('t13={}'.format(t13-t12))
logger.notice('t14={}'.format(t14-t13))
