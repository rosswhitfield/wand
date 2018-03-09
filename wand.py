from mantid.simpleapi import (mtd, ConvertSpectrumAxis, Transpose,
                              ResampleX, ConvertToMD, SetUB, BinMD,
                              PlusMD, CloneMDWorkspace, Divide,
                              DeleteWorkspace, Scale,
                              CopyInstrumentParameters,
                              NormaliseByCurrent)
from mantid.geometry import OrientedLattice


def reduceToPowder(ws, OutputWorkspace, cal=None, target='Theta', XMin=10, XMax=135, NumberBins=2500, normaliseBy='Monitor'):
    ConvertSpectrumAxis(InputWorkspace=ws, Target=target, OutputWorkspace=OutputWorkspace)
    Transpose(InputWorkspace=OutputWorkspace, OutputWorkspace=OutputWorkspace)
    ResampleX(InputWorkspace=OutputWorkspace, OutputWorkspace=OutputWorkspace, XMin=XMin, XMax=XMax, NumberBins=NumberBins)

    if cal is not None:
        CopyInstrumentParameters(ws, cal)
        ConvertSpectrumAxis(InputWorkspace=cal, Target=target, OutputWorkspace='__cal')
        Transpose(InputWorkspace='__cal', OutputWorkspace='__cal')
        ResampleX(InputWorkspace='__cal', OutputWorkspace='__cal', XMin=XMin, XMax=XMax, NumberBins=NumberBins)
        Divide(LHSWorkspace=OutputWorkspace, RHSWorkspace='__cal', OutputWorkspace=OutputWorkspace)
        DeleteWorkspace('__cal')

    if normaliseBy == "Monitor":
        NormaliseByCurrent(InputWorkspace=OutputWorkspace, OutputWorkspace=OutputWorkspace)
    elif normaliseBy == "Time":
        duration = mtd[ws].getRun().getLogData('duration').value
        Scale(InputWorkspace=OutputWorkspace, OutputWorkspace=OutputWorkspace, Factor=1./duration)

    return OutputWorkspace


def convertToQSample(ws, OutputWorkspace='__md_q_sample'):
    """Output MDEventWorkspace in Q Sample
    """
    ConvertToMD(ws, QDimensions='Q3D', dEAnalysisMode='Elastic', Q3DFrames='Q_sample',
                MinValues='-10,-1,-10', MaxValues='10,1,10', OutputWorkspace=OutputWorkspace)
    return OutputWorkspace


def convertToHKL(ws, OutputWorkspace='__md_hkl', UB=None, Extents=[-10, 10, -10, 10, -10, 10], Bins=[101, 101, 101], Append=False, scale=None,
                 Uproj=(1,0,0), Vproj=(0,1,0), Wproj=(0,0,1)):
    """Output MDHistoWorkspace in HKL
    """

    SetUB(ws, UB=UB)

    ConvertToMD(ws, QDimensions='Q3D', QConversionScales='HKL', dEAnalysisMode='Elastic', Q3DFrames='HKL', OutputWorkspace='__temp',
                Uproj=Uproj, Vproj=Vproj, Wproj=Wproj)

    if scae is not None:
        Scale(InputWorkspace='__temp', OutputWorkspace='__temp', Factor=scale)

    AlignedDim0 = "{},{},{},{}".format(mtd['__temp'].getDimension(0).name, Extents[0], Extents[1], int(Bins[0]))
    AlignedDim1 = "{},{},{},{}".format(mtd['__temp'].getDimension(1).name, Extents[2], Extents[3], int(Bins[1]))
    AlignedDim2 = "{},{},{},{}".format(mtd['__temp'].getDimension(2).name, Extents[4], Extents[5], int(Bins[2]))

    BinMD(InputWorkspace='__temp',
          TemporaryDataWorkspace=OutputWorkspace if Append and mtd.doesExist(OutputWorkspace) else None,
          OutputWorkspace=OutputWorkspace,
          AlignedDim0=AlignedDim0,
          AlignedDim1=AlignedDim1,
          AlignedDim2=AlignedDim2)
    DeleteWorkspace('__temp')

    return OutputWorkspace


def convertQSampleToHKL(ws, OutputWorkspace='__md_hkl', norm=None, UB=None, Extents=[-10, 10, -10, 10, -10, 10], Bins=[101, 101, 101], Append=False,
                        Uproj=(1,0,0), Vproj=(0,1,0), Wproj=(0,0,1)):
    ol = OrientedLattice()
    ol.setUB(UB)
    q1 = ol.qFromHKL(Uproj)
    q2 = ol.qFromHKL(Vproj)
    q3 = ol.qFromHKL(Wproj)
    BinMD(InputWorkspace=ws, AxisAligned=False, NormalizeBasisVectors=False,
          BasisVector0='Q1,A^-1,{},{},{}'.format(q1.X(), q1.Y(), q1.Z()),
          BasisVector1='Q2,A^-1,{},{},{}'.format(q2.X(), q2.Y(), q2.Z()),
          BasisVector2='Q3,A^-1,{},{},{}'.format(q3.X(), q3.Y(), q3.Z()),
          OutputExtents=Extents, OutputBins=Bins,
          TemporaryDataWorkspace=OutputWorkspace if Append and mtd.doesExist(OutputWorkspace) else None,
          OutputWorkspace=OutputWorkspace)
    if norm is not None:
        mtd[str(norm)].run().getGoniometer().setR(mtd[str(ws)].getExperimentInfo(0).run().getGoniometer().getR())
        convertToHKL(norm, OutputWorkspace=str(OutputWorkspace)+'_norm', UB=UB, Extents=Extents, Bins=Bins, Append=Append, Scale=mtd[ws].getExperimentInfo(0).run().getProtonCharge(),
                     Uproj=Uproj, Vproj=Vproj, Wproj=Wproj)
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
