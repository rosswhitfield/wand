from mantid.simpleapi import (LoadEventNexus, Integration, MaskDetectors, mtd,
                              SetGoniometer, ConvertSpectrumAxis, Transpose,
                              ResampleX, ConvertToMD, SetUB, BinMD, SliceMD,
                              PlusMD, CloneMDWorkspace, Divide, DeleteWorkspace)
from mantid.geometry import OrientedLattice
import numpy as np


def loadIntegrateData(filename, OutputWorkspace, wavelength=1.488):
    LoadEventNexus(Filename=filename, OutputWorkspace='__ws')
    Integration(InputWorkspace='__ws', OutputWorkspace='__ws')
    MaskDetectors('__ws', DetectorList=range(16384))
    mtd['__ws'].getAxis(0).setUnit("Wavelength")
    w = np.array([wavelength-0.001, wavelength+0.001])
    for idx in range(mtd['__ws'].getNumberHistograms()):
        mtd['__ws'].setX(idx, w)
    SetGoniometer('__ws', Axis0="HB2C:Mot:s1,0,1,0,1")
    return mtd['__ws']


def reduceToPowder(ws, OutputWorkspace, norm=None, taget='Theta', XMin=10, XMax=135, NumberBins=2500):
    # Add scale by monitor
    ConvertSpectrumAxis(InputWorkspace=ws, Target=taget, OutputWorkspace=OutputWorkspace)
    Transpose(InputWorkspace=OutputWorkspace, OutputWorkspace=OutputWorkspace)
    ResampleX(InputWorkspace=OutputWorkspace, OutputWorkspace=OutputWorkspace, XMin=XMin, XMax=XMax, NumberBins=NumberBins)
    if norm is not None:
        ConvertSpectrumAxis(InputWorkspace=norm, Target=taget, OutputWorkspace='__norm')
        Transpose(InputWorkspace='__norm', OutputWorkspace='__norm')
        ResampleX(InputWorkspace='__norm', OutputWorkspace='__norm', XMin=XMin, XMax=XMax, NumberBins=NumberBins)
        Divide(LHSWorkspace=OutputWorkspace,RHSWorkspace='__norm',OutputWorkspace=OutputWorkspace)
        DeleteWorkspace('__norm')
    return mtd[OutputWorkspace]


def convertToMD(ws, norm=None, UB=None):
    """Output MDEventWorkspace in Q Sample
    """
    if UB is None:
        if norm is None:
            return ConvertToMD(ws, QDimensions='Q3D', dEAnalysisMode='Elastic', Q3DFrames='Q_sample')
        else:
            return (ConvertToMD(ws, QDimensions='Q3D', dEAnalysisMode='Elastic', Q3DFrames='Q_sample'),
                    ConvertToMD(norm, QDimensions='Q3D', dEAnalysisMode='Elastic', Q3DFrames='Q_sample'))
    else:
        SetUB(ws, UB=UB)
        if norm is None:
            return ConvertToMD(ws, QDimensions='Q3D', dEAnalysisMode='Elastic', Q3DFrames='HKL')
        else:
            SetUB(norm, UB=UB)
            return (ConvertToMD(ws, QDimensions='Q3D', dEAnalysisMode='Elastic', Q3DFrames='HKL'),
                    ConvertToMD(norm, QDimensions='Q3D', dEAnalysisMode='Elastic', Q3DFrames='HKL'))


def convertQSampleToHKL(ws, norm=None, UB=None, hist=True, Extents=[-10, 10, -10, 10, -10, 10], Bins=[101, 101, 101]):
    ol = OrientedLattice()
    ol.setUB(UB)
    q1 = ol.qFromHKL([1, 0, 0])
    q2 = ol.qFromHKL([0, 1, 0])
    q3 = ol.qFromHKL([0, 0, 1])
    if hist:
        return BinMD(InputWorkspace=ws, AxisAligned=False,
                     BasisVector0='[H,0,0],A^-1,{},{},{}'.format(q1.X(), q1.Y(), q1.Z()),
                     BasisVector1='[0,K,0],A^-1,{},{},{}'.format(q2.X(), q2.Y(), q2.Z()),
                     BasisVector2='[0,0,L],A^-1,{},{},{}'.format(q3.X(), q3.Y(), q3.Z()),
                     OutputExtents=Extents, OutputBins=Bins)
    else:
        return SliceMD(InputWorkspace=ws, AxisAligned=False,
                       BasisVector0='[H,0,0],A^-1,{},{},{}'.format(q1.X(), q1.Y(), q1.Z()),
                       BasisVector1='[0,K,0],A^-1,{},{},{}'.format(q2.X(), q2.Y(), q2.Z()),
                       BasisVector2='[0,0,L],A^-1,{},{},{}'.format(q3.X(), q3.Y(), q3.Z()),
                       OutputExtents=Extents, OutputBins=Bins)


def accumlateMD(accum, ws):
    if accum in mtd:
        return PlusMD(LHSWorkspace=accum, RHSWorkspace=ws)
    else:
        return CloneMDWorkspace(InputWorkspace=ws)
