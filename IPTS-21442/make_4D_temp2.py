from mantid.simpleapi import LoadWAND, SetUB, ConvertToMD, PlusMD, mtd, DeleteWorkspace, CloneMDWorkspace
import numpy as np
import re

if 'data' in mtd:
    DeleteWorkspace('data')

for run in range(95409, 98459, 1):
    ws = LoadWAND(IPTS=21442,RunNumbers=run,Grouping='4x4')
    ub = np.array(re.findall(r'-?\d+\.*\d*', ws.run().getProperty('HB2C:CS:CrystalAlign:UBMatrix').value[0]),
                  dtype=np.float).reshape(3,3)
    sgl = np.deg2rad(ws.run().getProperty('HB2C:Mot:sgl.RBV').value[0]) # 'HB2C:Mot:sgl.RBV,1,0,0,-1'
    sgu = np.deg2rad(ws.run().getProperty('HB2C:Mot:sgu.RBV').value[0]) # 'HB2C:Mot:sgu.RBV,0,0,1,-1'
    sgl_a = np.array([[           1,            0,           0],
                      [           0,  np.cos(sgl), np.sin(sgl)],
                      [           0, -np.sin(sgl), np.cos(sgl)]])
    sgu_a = np.array([[ np.cos(sgu),  np.sin(sgu),           0],
                      [-np.sin(sgu),  np.cos(sgu),           0],
                      [           0,            0,           1]])
    UB = sgl_a.dot(sgu_a).dot(ub) # Apply the Goniometer tilts to the UB matrix
    SetUB(ws, UB=UB)
    md = ConvertToMD(ws,
                     QDimensions='Q3D',
                     dEAnalysisMode='Elastic',
                     Q3DFrames='HKL',
                     QConversionScales='HKL',
                     OtherDimensions='HB2C:SE:SampleTemp',
                     MinValues='-10,-10,-10,0',
                     MaxValues='10,10,10,30')
    if 'data' in mtd:
        PlusMD(LHSWorkspace='data',
               RHSWorkspace='md',
               OutputWorkspace='data')
    else:
        CloneMDWorkspace(InputWorkspace='md',
                         OutputWorkspace='data')

BinMD(InputWorkspace='data',
      AlignedDim0='[H,0,0],-1,3,200',
      AlignedDim1='[0,K,0],0,3,150',
      AlignedDim2='[0,0,L],-1,3,40',
      AlignedDim3='HB2C:SE:SampleTemp,0,30,10',
      OutputWorkspace='bin')
