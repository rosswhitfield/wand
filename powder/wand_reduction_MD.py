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

si2 = CloneWorkspace(si)
si2.getAxis(0).setUnit("Wavelength")
w = np.array([1.487,1.489])
for idx in xrange(si2.getNumberHistograms()):
    si2.setX(idx, w)

van2 = CloneWorkspace(van)
van2.getAxis(0).setUnit("Wavelength")
w = np.array([1.487,1.489])
for idx in xrange(van2.getNumberHistograms()):
    van2.setX(idx, w)



# ConvertToMD

ConvertToMD(InputWorkspace='si2', QDimensions='|Q|', dEAnalysisMode='Elastic', OutputWorkspace='si_md')#,MinValues='0',MaxValues='10.0')
ConvertToMD(InputWorkspace='van2', QDimensions='|Q|', dEAnalysisMode='Elastic', OutputWorkspace='van_md')#,MinValues='0',MaxValues='10.0')
si_bin=BinMD('si_md', AlignedDim0='|Q|,1,10,1800')
van_bin=BinMD('van_md', AlignedDim0='|Q|,1,10,1800')
norm=si_bin/van_bin
