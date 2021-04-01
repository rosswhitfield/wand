# import mantid algorithms, numpy and matplotlib
from mantid.simpleapi import *
from mantid.kernel import FloatTimeSeriesProperty
import matplotlib.pyplot as plt
import numpy as np

#ws = LoadMD('HB3A_data.nxs')
ws = LoadMD('HB3A_exp0724_scan0182.nxs')
SetGoniometer(ws, Axis0='omega,0,1,0,-1', Axis1='chi,0,0,1,-1', Axis2='phi,0,1,0,-1', Average=False)
r = ws.getExperimentInfo(0).run()
for i in range(r.getNumGoniometers()):
    print(i,r.getGoniometer(i).getEulerAngles('YZY'))

ws = LoadILLDiffraction(Filename='ILL/D20/000017.nxs')
SetGoniometer(ws, Axis0='omega.position,0,1,0,1', Average=False)
for i in range(ws.run().getNumGoniometers()):
    print(f'{i} omega = {ws.run().getGoniometer(i).getEulerAngles("YZY")[0]:.1f}')

SetGoniometer(ws, Axis0='omega.position,0,1,0,1')
for i in range(ws.run().getNumGoniometers()):
    print(f'{i} omega = {ws.run().getGoniometer(i).getEulerAngles("YZY")[0]:.1f}')


ws=LoadMD('ExternalData/Testing/Data/SystemTest/HB2C_WANDSCD_data.nxs')
s1 = ws.getExperimentInfo(0).run().getLogData('s1').value

s1_log = FloatTimeSeriesProperty('s1')
for n, v in enumerate(s1):
    s1_log.addValue(n*1e6,v)
ws.getExperimentInfo(0).run()['s1'] = s1_log
ws.getExperimentInfo(0).run().getProperty('s1').units = 'deg'

SetGoniometer(ws, Axis0='s1,0,1,0,1', Average=False)

r = ws.getExperimentInfo(0).run()
for i in range(r.getNumGoniometers()):
    print(f'{i} omega = {r.getGoniometer(i).getEulerAngles("YZY")[0]:.1f}')
