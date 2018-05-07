Rsi=LoadEventNexus('/HFIR/HB2C/IPTS-7776/nexus/HB2C_26632.nxs.h5')
van=LoadWAND('/HFIR/HB2C/IPTS-7776/nexus/HB2C_26617.nxs.h5')

GenerateEventsFilter(InputWorkspace='si', OutputWorkspace='filter', InformationWorkspace='info', TimeInterval='0.5',StartTime='0',StopTime='40')
FilterEvents(InputWorkspace='si', SplitterWorkspace='filter', OutputWorkspaceBaseName='out', InformationWorkspace='info',GroupWorkspaces=True,FilterByPulseTime=True,OutputWorkspaceIndexedFrom1=True)
WANDPowderReduction(InputWorkspace='out', CalibrationWorkspace='van', NumberBins=1000, Target='Theta', NormaliseBy='None',OutputWorkspace='pd')

for n in range(10):
    name='pd_sum_{}'.format(n)
    for i in range(8):
        inWS = 'pd_{}'.format(n+10*i+1)
        if name in mtd:
            Plus(LHSWorkspace=name, RHSWorkspace=inWS, OutputWorkpspace=name)
        else:
            CloneWorkspace(InputWorkspace=inWS, OutputWorkspace=name)

