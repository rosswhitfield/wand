from mantid.simpleapi import *
from mantid.api import NumericAxis


van = LoadEventNexus(Filename='/HFIR/HB2C/IPTS-7776/nexus/HB2C_1035.nxs.h5')
#van = Rebin(van, '0,16670,16670', PreserveEvents=False)
van = Integration(van)
MaskDetectors(van,DetectorList=range(16384))

si = LoadEventNexus(Filename='/HFIR/HB2C/IPTS-7776/nexus/HB2C_1024.nxs.h5')
#si = Rebin(si, '0,16670,16670', PreserveEvents=False)
si = Integration(si)
MaskDetectors(si,DetectorList=range(16384))

# Fix missing s2 - # "HB2C:Mot:s2" 17.57 deg
AddSampleLog(van, LogName='HB2C:Mot:s2', LogText='17.57', LogType='Number Series')
AddSampleLog(van, LogName='HB2C:Mot:detz', LogText='7.05159', LogType='Number Series')
LoadInstrument(van, InstrumentName='WAND', RewriteSpectraMap=False)
AddSampleLog(si, LogName='HB2C:Mot:s2', LogText='17.57', LogType='Number Series')
AddSampleLog(si, LogName='HB2C:Mot:detz', LogText='7.05159', LogType='Number Series')
LoadInstrument(si, InstrumentName='WAND', RewriteSpectraMap=False)

norm = si/van
#norm=ReplaceSpecialValues(norm, NaNValue=0, InfinityValue=0)

norm_2theta=ConvertSpectrumAxis(norm, Target='Theta')
norm_2theta=Transpose(norm_2theta)

norm_d=ConvertSpectrumAxis(norm, Target='ElasticDSpacing', EFixed='36.9462') # Lambda = 1.488A
norm_d=Transpose(norm_d)

# Do convertion first

van_2theta=ConvertSpectrumAxis(van, Target='Theta')
van_2theta=Transpose(van_2theta)

van_d=ConvertSpectrumAxis(van, Target='ElasticDSpacing', EFixed='36.9462') # Lambda = 1.488A
van_d=Transpose(van_d)

si_2theta=ConvertSpectrumAxis(si, Target='Theta')
si_2theta=Transpose(si_2theta)

si_d=ConvertSpectrumAxis(si, Target='ElasticDSpacing', EFixed='36.9462') # Lambda = 1.488A
si_d=Transpose(si_d)

d=si_d/van_d
twotheta=si_2theta/van_2theta

# ResampleX
van_2theta2=ResampleX(van_2theta,XMin=20,XMax=135,NumberBins=2300)
si_2theta2=ResampleX(si_2theta,XMin=20,XMax=135,NumberBins=2300)
twotheta2=si_2theta2/van_2theta2

van_d2=ResampleX(van_d,XMin=0.8,XMax=4,NumberBins=3200)
si_d2=ResampleX(si_d,XMin=0.8,XMax=4,NumberBins=3200)
d2=si_d2/van_d2

# Save
SaveFocusedXYE(d2,Filename='HB2C_1024_1035_d.xye',Append=False)
SaveFocusedXYE(twotheta2,Filename='HB2C_1024_1035_2t.xye',Append=False)



# Try with ConvertUnits
si2=CloneWorkspace(si)
si2 = ConvertToPointData(si2)
si2.getAxis(0).setUnit("Wavelength")
w = np.array([1.488])
for idx in xrange(si2.getNumberHistograms()):
    si2.setX(idx, w)

# Try with ConvertUnits # 2
norm2 = CloneWorkspace(norm)
norm2 = ConvertToPointData(norm2)
norm2 = ConvertAxisByFormula(norm2,Formula='1.488',AxisUnits='Wavelength')


si2 = CloneWorkspace(si)
si2 = ConvertToPointData(si2)
si2 = ConvertAxisByFormula(si2,Formula='1.488',AxisUnits='Wavelength')

si2d = ConvertUnits(si2, Target='dSpacing')
si2dr = Rebin(si2d, '0.8,0.01,4.0')
si2dr = SumSpectra(si2dr)

van2 = CloneWorkspace(van)
van2 = ConvertToPointData(van2)
van2 = ConvertAxisByFormula(van2,Formula='1.488',AxisUnits='Wavelength')
norm22 = si2/van2



si3 = CloneWorkspace(si)
si3 = ConvertAxisByFormula(si3,Formula='1.488',AxisUnits='Wavelength')
si3d = ConvertUnits(si3, Target='dSpacing')

si4 = CloneWorkspace(si)
si4.getAxis(0).setUnit("Wavelength")
w = np.array([1.487,1.489])
for idx in xrange(si4.getNumberHistograms()):
    si4.setX(idx, w)
si4e=ConvertToEventWorkspace(si4)
si4ed = ConvertUnits(si4e, Target='dSpacing')
si4edr = Rebin(si4ed, Params='0.8,0.01,4.0')
si4edr = Rebin(si4ed, Params='1.0,3.0,4.0')
si4edrs = SumSpectra(si4edr)
