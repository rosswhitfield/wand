from mantid.simpleapi import *
import numpy as np

def loadIntegrateData(filename, wavelength=1.488):
    LoadEventNexus(Filename=filename,OutputWorkspace='__ws')
    Integration(InputWorkspace='__ws',,OutputWorkspace='__ws')
    MaskDetectors(ws,DetectorList=range(16384))
    mtd['__ws'].getAxis(0).setUnit("Wavelength")
    w = np.array([wavelength-0.001,wavelength+0.001])
    for idx in xrange(ws.getNumberHistograms()):
        mtd['__ws'].setX(idx, w)
    SetGoniometer('__ws', Axis0="HB2C:Mot:s1,0,1,0,1")
    return mtd['__ws']    

def reduceToPowder(ws, taget='Theta',XMin=10,XMax=135,NumberBins=2500):
    ConvertSpectrumAxis(InputWorkspace=ws, Target=taget, OutputWorkspace='__out')
    Transpose(InputWorkspace='__out', OutputWorkspace='__out')
    ResampleX(InputWorkspace='__out', OutputWorkspace='__out',XMin=XMin,XMax=XMax,NumberBins=NumberBins)
    return mtd['__out']

def reduceToQSample(ws):
    return ConvertToMD(ws, QDimensions='Q3D', dEAnalysisMode='Elastic', Q3DFrames='Q_sample')

def qSampleToHKL(ws, UB, hist=True):
    pass

def accumlateMD(accum, ws):
    if accum in mtd:
        return PlusMD(LHSWorkspace=accum, RHSWorkspace=ws)
    else:
        return CloneMDWorkspace(InputWorkspace=ws)
