from mantid.simpleapi import (LoadEventNexus, Integration,
                              MaskDetectors, mtd, SetGoniometer,
                              ConvertSpectrumAxis, Transpose,
                              ResampleX, ConvertToMD, SetUB, BinMD,
                              PlusMD, CloneMDWorkspace, Divide,
                              DeleteWorkspace)
from mantid.geometry import OrientedLattice
import numpy as np


def loadIntegrateData(filename, OutputWorkspace='__ws', wavelength=1.488):
    LoadEventNexus(Filename=filename, OutputWorkspace=OutputWorkspace)
    Integration(InputWorkspace=OutputWorkspace, OutputWorkspace=OutputWorkspace)
    MaskDetectors(OutputWorkspace, DetectorList=range(16384))
    mtd[OutputWorkspace].getAxis(0).setUnit("Wavelength")
    w = np.array([wavelength-0.001, wavelength+0.001])
    for idx in range(mtd[OutputWorkspace].getNumberHistograms()):
        mtd[OutputWorkspace].setX(idx, w)
    SetGoniometer(OutputWorkspace, Axis0="HB2C:Mot:s1,0,1,0,1")
    return OutputWorkspace


def reduceToPowder(ws, OutputWorkspace, norm=None, taget='Theta', XMin=10, XMax=135, NumberBins=2500):
    # Add scale by monitor
    ConvertSpectrumAxis(InputWorkspace=ws, Target=taget, OutputWorkspace=OutputWorkspace)
    Transpose(InputWorkspace=OutputWorkspace, OutputWorkspace=OutputWorkspace)
    ResampleX(InputWorkspace=OutputWorkspace, OutputWorkspace=OutputWorkspace, XMin=XMin, XMax=XMax, NumberBins=NumberBins)
    if norm is not None:
        ConvertSpectrumAxis(InputWorkspace=norm, Target=taget, OutputWorkspace='__norm')
        Transpose(InputWorkspace='__norm', OutputWorkspace='__norm')
        ResampleX(InputWorkspace='__norm', OutputWorkspace='__norm', XMin=XMin, XMax=XMax, NumberBins=NumberBins)
        Divide(LHSWorkspace=OutputWorkspace, RHSWorkspace='__norm', OutputWorkspace=OutputWorkspace)
        DeleteWorkspace('__norm')
    return OutputWorkspace


def convertToQSample(ws, OutputWorkspace='__md_q_sample'):
    """Output MDEventWorkspace in Q Sample
    """
    ConvertToMD(ws, QDimensions='Q3D', dEAnalysisMode='Elastic', Q3DFrames='Q_sample',
                MinValues='-10,-1,-10', MaxValues='10,1,10', OutputWorkspace=OutputWorkspace)
    return OutputWorkspace


def convertToHKL(ws, OutputWorkspace='__md_hkl', norm=None, UB=None, Extents=[-10, 10, -10, 10, -10, 10], Bins=[101, 101, 101]):
    """Output MDEventWorkspace in HKL
    """
    SetUB(ws, UB=UB)
    ConvertToMD(ws, QDimensions='Q3D', QConversionScales='HKL', dEAnalysisMode='Elastic', Q3DFrames='HKL', OutputWorkspace=OutputWorkspace)
    AlignedDim0="{},{},{},{}".format(mtd[OutputWorkspace].getDimension(0).name, Extents[0], Extents[1], int(Bins[0]))
    AlignedDim1="{},{},{},{}".format(mtd[OutputWorkspace].getDimension(1).name, Extents[2], Extents[3], int(Bins[1]))
    AlignedDim2="{},{},{},{}".format(mtd[OutputWorkspace].getDimension(2).name, Extents[4], Extents[5], int(Bins[2]))
    BinMD(InputWorkspace=OutputWorkspace,
          OutputWorkspace=OutputWorkspace,
          AlignedDim0=AlignedDim0,
          AlignedDim1=AlignedDim1,
          AlignedDim2=AlignedDim2)
    if norm is not None:
        SetUB(norm, UB=UB)
        ConvertToMD(norm, QDimensions='Q3D', QConversionScales='HKL', dEAnalysisMode='Elastic', Q3DFrames='HKL', OutputWorkspace=str(OutputWorkspace)+'_norm')
        BinMD(InputWorkspace=str(OutputWorkspace)+'_norm',
              OutputWorkspace=str(OutputWorkspace)+'_norm',
              AlignedDim0=AlignedDim0,
              AlignedDim1=AlignedDim1,
              AlignedDim2=AlignedDim2)
    return OutputWorkspace


def convertQSampleToHKL(ws, OutputWorkspace='__md_hkl', norm=None, UB=None, Extents=[-10, 10, -10, 10, -10, 10], Bins=[101, 101, 101]):
    ol = OrientedLattice()
    ol.setUB(UB)
    q1 = ol.qFromHKL([1, 0, 0])
    q2 = ol.qFromHKL([0, 1, 0])
    q3 = ol.qFromHKL([0, 0, 1])
    BinMD(InputWorkspace=ws, AxisAligned=False,NormalizeBasisVectors=False,
          BasisVector0='[H,0,0],A^-1,{},{},{}'.format(q1.X(), q1.Y(), q1.Z()),
          BasisVector1='[0,K,0],A^-1,{},{},{}'.format(q2.X(), q2.Y(), q2.Z()),
          BasisVector2='[0,0,L],A^-1,{},{},{}'.format(q3.X(), q3.Y(), q3.Z()),
          OutputExtents=Extents, OutputBins=Bins,
          OutputWorkspace=OutputWorkspace)
    if norm is not None:
        mtd[str(norm)].run().getGoniometer().setR(mtd[str(ws)].getExperimentInfo(0).run().getGoniometer().getR())
        convertToHKL(norm, OutputWorkspace=str(OutputWorkspace)+'_norm', UB=UB, Extents=Extents, Bins=Bins)
    return OutputWorkspace


def accumulateMD(ws, norm=None, OutputWorkspace='__mdh_sum'):
    if OutputWorkspace in mtd:
        PlusMD(LHSWorkspace=OutputWorkspace, RHSWorkspace=ws, OutputWorkspace=OutputWorkspace)
        if norm is not None:
            PlusMD(LHSWorkspace=str(OutputWorkspace)+'_norm', RHSWorkspace=norm, OutputWorkspace=str(OutputWorkspace)+'_norm')
    else:
        CloneMDWorkspace(InputWorkspace=ws, OutputWorkspace=OutputWorkspace)
        if norm is not None:
            CloneMDWorkspace(InputWorkspace=norm, OutputWorkspace=str(OutputWorkspace)+'_norm')
    return OutputWorkspace
