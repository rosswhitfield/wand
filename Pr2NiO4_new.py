import numpy as np

LoadWANDSCD(IPTS=7776, RunNumbers='4756-6557', Grouping='4x4', OutputWorkspace='data')
ConvertWANDSCDtoQ(InputWorkspace='data', NormaliseBy='None', KeepTemporaryWorkspaces=True, OutputWorkspace='q', BinningDim0='-8.01,8.01,801', BinningDim1='-0.81,0.81,81',BinningDim2='-8.01,8.01,801')

FindPeaksMD(InputWorkspace='q_data', PeakDistanceThreshold=1, MaxPeaks=100, DensityThresholdFactor=500, CalculateGoniometerForCW=True, Wavelength=1.488, OutputWorkspace='peaks')

tt0=np.array(data.getExperimentInfo(0).run().getLogData('twotheta').value)
az0=np.array(data.getExperimentInfo(0).run().getLogData('azimuthal').value)


FindUBUsingLatticeParameters('peaks',5.414,5.414,12.457,90,90,90)

ws=LoadEventNexus(Filename='/HFIR/HB2C/IPTS-7776/nexus/HB2C_4756.nxs.h5', MetaDataOnly=True)
AddSampleLog(ws, LogName='HB2C:Mot:detz.RBV', LogText='3.85', LogType='Number Series')
LoadInstrument(ws, InstrumentName='WAND', RewriteSpectraMap='True')

grouping = 4
tmp_group, _, _ = CreateGroupingWorkspace(InputWorkspace=ws)

group_number = 0
for x in range(0,480*8,grouping):
    for y in range(0,512,grouping):
        group_number += 1
        for j in range(grouping):
            for i in range(grouping):
                tmp_group.dataY(y+i+(x+j)*512)[0] = group_number
    
tmp_ws = GroupDetectors(InputWorkspace=ws, CopyGroupingFromWorkspace=tmp_group)

table=PreprocessDetectorsToMD(tmp_ws)
twotheta = table.column(2)
azimuthal = table.column(3)
data.getExperimentInfo(0).run().addProperty('twotheta', twotheta, True)
data.getExperimentInfo(0).run().addProperty('azimuthal', azimuthal, True)


ConvertWANDSCDtoQ(InputWorkspace='data', NormaliseBy='None', KeepTemporaryWorkspaces=True, OutputWorkspace='q', BinningDim0='-8.01,8.01,801', BinningDim1='-0.81,0.81,81',BinningDim2='-8.01,8.01,801')

FindPeaksMD(InputWorkspace='q_data', PeakDistanceThreshold=1, MaxPeaks=100, DensityThresholdFactor=500, CalculateGoniometerForCW=True, Wavelength=1.488, OutputWorkspace='peaks')

FindUBUsingLatticeParameters('peaks',5.414,5.414,12.457,90,90,90)
