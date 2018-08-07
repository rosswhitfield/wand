ws=LoadEventNexus('/HFIR/HB2C/IPTS-20148/nexus/HB2C_55562.nxs.h5',LoadMonitors=True)

GenerateEventsFilter(InputWorkspace='ws', OutputWorkspace='filter', InformationWorkspace='info', LogName='HB2C:SE:SampleTemp', LogValueInterval=2,MinimumLogValue=150,MaximumLogValue=300)
FilterEvents(InputWorkspace='ws', SplitterWorkspace='filter', OutputWorkspaceBaseName='out', InformationWorkspace='info',GroupWorkspaces=True,FilterByPulseTime=True,OutputWorkspaceIndexedFrom1=True)
FilterEvents(InputWorkspace='ws_monitors', SplitterWorkspace='filter', OutputWorkspaceBaseName='mon', InformationWorkspace='info',GroupWorkspaces=True,FilterByPulseTime=True,SpectrumWithoutDetector='Skip only if TOF correction',OutputWorkspaceIndexedFrom1=True)

Ei=UnitConversion.run('Wavelength', 'Energy', 1.488, 0, 0, 0, Elastic, 0)

for n in range(mtd['out'].getNumberOfEntries()):
    AddSampleLog(mtd['out'].getItem(n), LogName="gd_prtn_chrg", LogType='Number', NumberType='Double',LogText=str(mtd['mon'].getItem(n).getNumberEvents()))
    AddSampleLog(mtd['out'], LogName="Ei", LogType='Number', NumberType='Double',LogText=str(Ei))

MaskBTP('out', Bank='8', Tube='475-480')
MaskBTP('out', Pixel='1,2,511,512')

name = 'LSCO_150to300'
IPTS = 20148
first_run = 55562
vanadium = 26613
vanadium_IPTS = 20148
normaliseBy='Monitor' # One on (None, Monitor, Time)
units = 'ElasticDSpacing' # One of (Theta, ElasticQ, ElasticDSpacing)
Binning = '1.5,2,201' # Min,Max,Number_of_bins
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

van_iptsdir = '/HFIR/HB2C/IPTS-{}/'.format(vanadium_IPTS)

if vanadium is not None:
    if 'cal' in mtd:
        cal = mtd['cal']
    else:
        if use_autoreduced_van:
            cal = LoadNexus(Filename=van_iptsdir+'shared/autoreduce/HB2C_{}.nxs'.format(vanadium))
        else:
            cal = LoadWAND(Filename=van_iptsdir+'shared/HB2C_{}.nxs.h5'.format(vanadium))
else:
    cal = None


xmin, xmax, bins = Binning.split(',')
group_list=[]
for n in range(mtd['out'].getNumberOfEntries()):
    nameT = name+'_{:05.1f}K'.format(mtd['out'][n].run().getLogData("HB2C:SE:SampleTemp").timeAverageValue())
    group_list.append(nameT)
    reduceToPowder(mtd['out'][n], OutputWorkspace=nameT, cal=cal, target=units, XMin=xmin, XMax=xmax, NumberBins=bins, normaliseBy=normaliseBy)

GroupWorkspaces(group_list,OutputWorkspace=name)
labels=','.join(['{:.1f}'.format(w.run().getLogData("HB2C:SE:SampleTemp").timeAverageValue()) for w in mtd['out']])
print(labels)

# ROI  1

ROI_workspace='MaskWorkspace'
roi_name = '_ROI1'
CloneWorkspace('out',OutputWorkspace='out'+roi_name)
CloneWorkspace('cal',OutputWorkspace='cal'+roi_name)
MaskDetectors('out'+roi_name,MaskedWorkspace=ROI_workspace)
MaskDetectors('cal'+roi_name,MaskedWorkspace=ROI_workspace)

xmin, xmax, bins = Binning.split(',')
group_list=[]
for n in range(mtd['out'+roi_name].getNumberOfEntries()):
    nameT = name+roi_name+'_{:05.1f}K'.format(mtd['out'+roi_name][n].run().getLogData("HB2C:SE:SampleTemp").timeAverageValue())
    group_list.append(nameT)
    reduceToPowder(mtd['out'+roi_name][n], OutputWorkspace=nameT, cal=cal, target=units, XMin=xmin, XMax=xmax, NumberBins=bins, normaliseBy=normaliseBy)
GroupWorkspaces(group_list,OutputWorkspace=name+roi_name)

# ROI  2

ROI_workspace='MaskWorkspace_2'
roi_name = '_ROI2'
CloneWorkspace('out',OutputWorkspace='out'+roi_name)
CloneWorkspace('cal',OutputWorkspace='cal'+roi_name)
MaskDetectors('out'+roi_name,MaskedWorkspace=ROI_workspace)
MaskDetectors('cal'+roi_name,MaskedWorkspace=ROI_workspace)

xmin, xmax, bins = Binning.split(',')
group_list=[]
for n in range(mtd['out'+roi_name].getNumberOfEntries()):
    nameT = name+roi_name+'_{:05.1f}K'.format(mtd['out'+roi_name][n].run().getLogData("HB2C:SE:SampleTemp").timeAverageValue())
    group_list.append(nameT)
    reduceToPowder(mtd['out'+roi_name][n], OutputWorkspace=nameT, cal=cal, target=units, XMin=xmin, XMax=xmax, NumberBins=bins, normaliseBy=normaliseBy)
GroupWorkspaces(group_list,OutputWorkspace=name+roi_name)

DeleteWorkspace('out'+roi_name)
DeleteWorkspace('cal'+roi_name)

# ROI  3

ROI_workspace='MaskWorkspace_3'
roi_name = '_ROI3'
CloneWorkspace('out',OutputWorkspace='out'+roi_name)
CloneWorkspace('cal',OutputWorkspace='cal'+roi_name)
MaskDetectors('out'+roi_name,MaskedWorkspace=ROI_workspace)
MaskDetectors('cal'+roi_name,MaskedWorkspace=ROI_workspace)

xmin, xmax, bins = Binning.split(',')
group_list=[]
for n in range(mtd['out'+roi_name].getNumberOfEntries()):
    nameT = name+roi_name+'_{:05.1f}K'.format(mtd['out'+roi_name][n].run().getLogData("HB2C:SE:SampleTemp").timeAverageValue())
    group_list.append(nameT)
    reduceToPowder(mtd['out'+roi_name][n], OutputWorkspace=nameT, cal=cal, target=units, XMin=xmin, XMax=xmax, NumberBins=bins, normaliseBy=normaliseBy)
GroupWorkspaces(group_list,OutputWorkspace=name+roi_name)

DeleteWorkspace('out'+roi_name)
DeleteWorkspace('cal'+roi_name)

# ROI  4

ROI_workspace='MaskWorkspace_4'
roi_name = '_ROI4'
CloneWorkspace('out',OutputWorkspace='out'+roi_name)
CloneWorkspace('cal',OutputWorkspace='cal'+roi_name)
MaskDetectors('out'+roi_name,MaskedWorkspace=ROI_workspace)
MaskDetectors('cal'+roi_name,MaskedWorkspace=ROI_workspace)

xmin, xmax, bins = Binning.split(',')
group_list=[]
for n in range(mtd['out'+roi_name].getNumberOfEntries()):
    nameT = name+roi_name+'_{:05.1f}K'.format(mtd['out'+roi_name][n].run().getLogData("HB2C:SE:SampleTemp").timeAverageValue())
    group_list.append(nameT)
    reduceToPowder(mtd['out'+roi_name][n], OutputWorkspace=nameT, cal=cal, target=units, XMin=xmin, XMax=xmax, NumberBins=bins, normaliseBy=normaliseBy)
GroupWorkspaces(group_list,OutputWorkspace=name+roi_name)

DeleteWorkspace('out'+roi_name)
DeleteWorkspace('cal'+roi_name)

# ROI  5

ROI_workspace='MaskWorkspace_5'
roi_name = '_ROI5'
CloneWorkspace('out',OutputWorkspace='out'+roi_name)
CloneWorkspace('cal',OutputWorkspace='cal'+roi_name)
MaskDetectors('out'+roi_name,MaskedWorkspace=ROI_workspace)
MaskDetectors('cal'+roi_name,MaskedWorkspace=ROI_workspace)

xmin, xmax, bins = Binning.split(',')
group_list=[]
for n in range(mtd['out'+roi_name].getNumberOfEntries()):
    nameT = name+roi_name+'_{:05.1f}K'.format(mtd['out'+roi_name][n].run().getLogData("HB2C:SE:SampleTemp").timeAverageValue())
    group_list.append(nameT)
    reduceToPowder(mtd['out'+roi_name][n], OutputWorkspace=nameT, cal=cal, target=units, XMin=xmin, XMax=xmax, NumberBins=bins, normaliseBy=normaliseBy)
GroupWorkspaces(group_list,OutputWorkspace=name+roi_name)

DeleteWorkspace('out'+roi_name)
DeleteWorkspace('cal'+roi_name)

# ROI  6

ROI_workspace='MaskWorkspace_6'
roi_name = '_ROI6'
CloneWorkspace('out',OutputWorkspace='out'+roi_name)
CloneWorkspace('cal',OutputWorkspace='cal'+roi_name)
MaskDetectors('out'+roi_name,MaskedWorkspace=ROI_workspace)
MaskDetectors('cal'+roi_name,MaskedWorkspace=ROI_workspace)

xmin, xmax, bins = Binning.split(',')
group_list=[]
for n in range(mtd['out'+roi_name].getNumberOfEntries()):
    nameT = name+roi_name+'_{:05.1f}K'.format(mtd['out'+roi_name][n].run().getLogData("HB2C:SE:SampleTemp").timeAverageValue())
    group_list.append(nameT)
    reduceToPowder(mtd['out'+roi_name][n], OutputWorkspace=nameT, cal=cal, target=units, XMin=xmin, XMax=xmax, NumberBins=bins, normaliseBy=normaliseBy)
GroupWorkspaces(group_list,OutputWorkspace=name+roi_name)

DeleteWorkspace('out'+roi_name)
DeleteWorkspace('cal'+roi_name)
