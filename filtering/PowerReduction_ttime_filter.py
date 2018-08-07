from mantid.simpleapi import *

name = 'AmV6a_time'
IPTS = 19834
run = 122687
vanadium = 101567 # Run number of `None`
vanadium_IPTS = 7776
normaliseBy='Monitor' # One on (None, Monitor, Time)
units = 'Theta' # One of (Theta, ElasticQ, ElasticDSpacing)
Binning = '3,123,1200' # Min,Max,Number_of_bins
use_autoreduced = False
use_autoreduced_van = False

###############################################################################

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
        ws_monitor = mtd[str(ws)].run().getProtonCharge()
        cal_monitor = mtd[str(cal)].run().getProtonCharge()        
        Scale(InputWorkspace=OutputWorkspace, OutputWorkspace=OutputWorkspace, Factor=cal_monitor/ws_monitor)
    elif normaliseBy == "Time":
        ws_duration = mtd[str(ws)].run().getLogData('duration').value
        cal_duration = mtd[str(cal)].run().getLogData('duration').value
        Scale(InputWorkspace=OutputWorkspace, OutputWorkspace=OutputWorkspace, Factor=cal_duration/ws_duration)
    return OutputWorkspace

###############################################################################

iptsdir = '/HFIR/HB2C/IPTS-{}/'.format(IPTS)
van_iptsdir = '/HFIR/HB2C/IPTS-{}/'.format(vanadium_IPTS)

LoadEventNexus(Filename=iptsdir+'nexus/HB2C_{}.nxs.h5'.format(run), OutputWorkspace='ws',LoadMonitors=True)

GenerateEventsFilter(InputWorkspace='ws', OutputWorkspace='filter', InformationWorkspace='info', TimeInterval='3600',StartTime='0',StopTime='84000')
FilterEvents(InputWorkspace='ws', SplitterWorkspace='filter', OutputWorkspaceBaseName='out', InformationWorkspace='info',GroupWorkspaces=True,FilterByPulseTime=True,OutputWorkspaceIndexedFrom1=True)
FilterEvents(InputWorkspace='ws_monitors', SplitterWorkspace='filter', OutputWorkspaceBaseName='mon', InformationWorkspace='info',GroupWorkspaces=True,FilterByPulseTime=True,SpectrumWithoutDetector='Skip only if TOF correction',OutputWorkspaceIndexedFrom1=True)

for n in range(mtd['out'].getNumberOfEntries()):
    AddSampleLog(mtd['out'].getItem(n), LogName="gd_prtn_chrg", LogType='Number', NumberType='Double',LogText=str(mtd['mon'].getItem(n).getNumberEvents()))

MaskBTP('out', Bank='8', Tube='475-480')
MaskBTP('out', Pixel='1,2,511,512')


if vanadium is not None:
    if 'cal' in mtd:
        cal = mtd['cal']
    else:
        if use_autoreduced_van:
            cal = LoadNexus(Filename=van_iptsdir+'shared/autoreduce/HB2C_{}.nxs'.format(vanadium))
        else:
            cal = LoadWAND(Filename=van_iptsdir+'nexus/HB2C_{}.nxs.h5'.format(vanadium))
else:
    cal = None

xmin, xmax, bins = Binning.split(',')
group_list=[]
for n in range(mtd['out'].getNumberOfEntries()):
    nameT = name+'_'+mtd['out'][n].name()
    group_list.append(nameT)
    reduceToPowder(mtd['out'][n], OutputWorkspace=nameT, cal=cal, target=units, XMin=xmin, XMax=xmax, NumberBins=bins, normaliseBy=normaliseBy)

GroupWorkspaces(group_list,OutputWorkspace=name)
