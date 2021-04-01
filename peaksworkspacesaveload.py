from mantid.simpleapi import *

ws = LoadEmptyInstrument(InstrumentName='TOPAZ')
peaks = CreatePeaksWorkspace(ws)
SaveNexus(peaks, Filename='peaks.nxs')
peaks_loaded = LoadNexus('peaks.nxs')
CompareWorkspaces(peaks, peaks_loaded)


leanpeaks = WorkspaceFactory.createPeaks('LeanElasticPeaksWorkspace')
AnalysisDataService.addOrReplace('leanpeaks',leanpeaks)
SetUB(leanpeaks)
leanpeaks.addPeak(leanpeaks.createPeakHKL((1,0,0)))
SaveNexus(leanpeaks, Filename='leanpeaks.nxs') # This runs surprisingly, but produces a file that is missing all the workpsace information
leanpeaks_loaded = LoadNexus('leanpeaks.nxs') # This fails as the file is missing a lot of the requied data
CompareWorkspaces(leanpeaks, leanpeaks_loaded) # Once everything is completed this should run successfully
