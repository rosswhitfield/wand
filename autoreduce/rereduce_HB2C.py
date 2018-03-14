#!/usr/bin/env python2
import os
import sys
import random

sys.path.append("/opt/mantidnightly/bin")
from mantid.simpleapi import *

ipts = 21293
ipts_dir = '/HFIR/HB2C/IPTS-{}/'.format(ipts)
nexus_dir = ipts_dir+'nexus/'
reduce_dir = ipts_dir+'shared/autoreduce/'

raw_files = os.listdir(nexus_dir)
random.shuffle(raw_files)

for raw_file in raw_files:
    name = raw_file.replace('.nxs.h5','')
    outfile = reduce_dir+name+"_MDE.nxs"
    if os.path.isfile(outfile):
        print("found: "+outfile)
        continue
    print("reducing: "+outfile)
    ws = LoadWAND(nexus_dir+raw_file)
    ConvertToMD('ws', QDimensions='Q3D', dEAnalysisMode='Elastic', Q3DFrames='Q_sample', OutputWorkspace='md',MinValues='-10,-1,-10',MaxValues='10,1,10')
    SaveMD('md',outfile)
