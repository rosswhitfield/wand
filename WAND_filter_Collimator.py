si=LoadEventNexus('/HFIR/HB2C/IPTS-7776/nexus/HB2C_26632.nxs.h5')
van=LoadWAND('/HFIR/HB2C/IPTS-7776/nexus/HB2C_26617.nxs.h5')

GenerateEventsFilter(InputWorkspace='si', OutputWorkspace='filter', InformationWorkspace='info', TimeInterval='1',StartTime='0',StopTime='20')
FilterEvents(InputWorkspace='si', SplitterWorkspace='filter', OutputWorkspaceBaseName='out', InformationWorkspace='info',GroupWorkspaces=True,FilterByPulseTime=True,OutputWorkspaceIndexedFrom1=True)
WANDPowderReduction(InputWorkspace='out', CalibrationWorkspace='van', NumberBins=1000, Target='Theta', NormaliseBy='None',OutputWorkspace='pd')
