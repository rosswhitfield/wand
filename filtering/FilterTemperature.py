from mantid.simpleapi import *

name = 'output'
IPTS = 20325
run = 26563
background = None
BackgroundScale = 1
vanadium = 7553 # Run number or `None`
vanadium_IPTS = 7776
normaliseBy='Monitor' # One on (None, Monitor, Time)
units = 'Theta' # One of (Theta, ElasticQ, ElasticDSpacing)
Binning = '3,123,1200' # Min,Max,Number_of_bins

# Temperature filter options
LogName = 'HB2C:SE:SampleTemp'
LogValueInterval = 100
MinimumLogValue = None
MaximumLogValue = None

###############################################################################

# Load vandium if not already loaded.
vanadium_ws = 'HB2C_{}'.format(vanadium)

if vanadium_ws not in mtd:
     LoadWAND(IPTS=vanadium_IPTS, RunNumbers=vanadium, OutputWorkspace=vanadium_ws)

# Load background if needed and if not already loaded.

if background is not None:
     background_ws = 'HB2C_{}'.format(vanadium)
     if background_ws not in mtd:
          LoadWAND(IPTS=IPTS, RunNumbers=background, OutputWorkspace=background_ws)
else:
     background_ws = None

# Load data if not already loaded
ws = 'HB2C_{}'.format(run)

if ws not in mtd:
    LoadEventNexus(Filename='/HFIR/HB2C/IPTS-{}/nexus/HB2C_{}.nxs.h5'.format(IPTS, run), OutputWorkspace=ws,LoadMonitors=True)
    # Mask detectors to be the same as vanadium
    MaskDetectors(ws, MaskedWorkspace=vanadium_ws)

# Filter events

GenerateEventsFilter(InputWorkspace=ws, OutputWorkspace='filter', InformationWorkspace='info', LogName=LogName,
                     LogValueInterval=LogValueInterval, MinimumLogValue=MinimumLogValue, MaximumLogValue=MaximumLogValue)
FilterEvents(InputWorkspace=ws, SplitterWorkspace='filter', OutputWorkspaceBaseName=ws+'_filtered', InformationWorkspace='info',
             GroupWorkspaces=True,FilterByPulseTime=True,OutputWorkspaceIndexedFrom1=True)
FilterEvents(InputWorkspace=ws+'_monitors', SplitterWorkspace='filter', OutputWorkspaceBaseName=ws+'_filtered_mon', InformationWorkspace='info',
             GroupWorkspaces=True,FilterByPulseTime=True,SpectrumWithoutDetector='Skip only if TOF correction',OutputWorkspaceIndexedFrom1=True)

# Set the monitor count on filtered WS
for n in range(mtd[ws+'_filtered'].getNumberOfEntries()):
    AddSampleLog(mtd[ws+'_filtered'].getItem(n), LogName="gd_prtn_chrg",
                 LogType='Number', NumberType='Double',LogText=str(mtd[ws+'_filtered_mon'].getItem(n).getNumberEvents()))


# Run powder diffraction reduction
xmin, xmax, bins = Binning.split(',')
WANDPowderReduction(ws+'_filtered',
                    CalibrationWorkspace=vanadium_ws,
                    BackgroundWorkspace=background_ws, BackgroundScale=BackgroundScale,
                    XMin=xmin, XMax=xmax, NumberBins=bins,
                    NormaliseBy=normaliseBy,
                    OutputWorkspace=name)
