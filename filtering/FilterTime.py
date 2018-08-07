from mantid.simpleapi import *

name = 'output'
IPTS = 19834
run = 122687
vanadium = 101567 # Run number or `None`
vanadium_IPTS = 7776
normaliseBy='Monitor' # One on (None, Monitor, Time)
units = 'Theta' # One of (Theta, ElasticQ, ElasticDSpacing)
Binning = '3,123,1200' # Min,Max,Number_of_bins

# Time filter options
TimeInterval=3600
StartTime=None
StopTime=None

###############################################################################

# Load vandium if not already loaded.
vanadium_ws = 'HB2C_{}'.format(vanadium)

if vanadium_ws not in mtd:
     cal = LoadWAND(Filename=van_iptsdir+'nexus/HB2C_{}.nxs.h5'.format(vanadium))

# Load data if not already loaded
ws = 'HB2C_{}'.format(vanadium)

if ws not in mtd:
    LoadEventNexus(Filename='/HFIR/HB2C/IPTS-{}/nexus/HB2C_{}.nxs.h5'.format(IPTS, run), OutputWorkspace=ws,LoadMonitors=True)

# Filter events

GenerateEventsFilter(InputWorkspace=ws, OutputWorkspace='filter', InformationWorkspace='info', TimeInterval='3600',StartTime='0',StopTime='84000')
FilterEvents(InputWorkspace=ws, SplitterWorkspace='filter', OutputWorkspaceBaseName=ws+'_filtered', InformationWorkspace='info',
             GroupWorkspaces=True,FilterByPulseTime=True,OutputWorkspaceIndexedFrom1=True)
FilterEvents(InputWorkspace=ws+'_monitors', SplitterWorkspace='filter', OutputWorkspaceBaseName=ws+'_filtered_mon', InformationWorkspace='info',
             GroupWorkspaces=True,FilterByPulseTime=True,SpectrumWithoutDetector='Skip only if TOF correction',OutputWorkspaceIndexedFrom1=True)

for n in range(mtd['out'].getNumberOfEntries()):
    AddSampleLog(mtd['out'].getItem(n), LogName="gd_prtn_chrg", LogType='Number', NumberType='Double',LogText=str(mtd['mon'].getItem(n).getNumberEvents()))

MaskBTP('out', Bank='8', Tube='475-480')
MaskBTP('out', Pixel='1,2,511,512')

xmin, xmax, bins = Binning.split(',')
group_list=[]
for n in range(mtd['out'].getNumberOfEntries()):
    nameT = name+'_'+mtd['out'][n].name()
    group_list.append(nameT)
    WANDPowderReduction(mtd['out'][n], OutputWorkspace=nameT, cal=cal, target=units, XMin=xmin, XMax=xmax, NumberBins=bins, normaliseBy=normaliseBy)

GroupWorkspaces(group_list,OutputWorkspace=name)
