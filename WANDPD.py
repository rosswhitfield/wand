si1=LoadWAND('/HFIR/HB2C/IPTS-7776/nexus/HB2C_26506.nxs.h5')
si2=LoadWAND('/HFIR/HB2C/IPTS-7776/nexus/HB2C_26507.nxs.h5')
van=LoadWAND('/HFIR/HB2C/IPTS-7776/nexus/HB2C_26509.nxs.h5')


WANDPowderReduction(InputWorkspace='si1', CalibrationWorkspace='van', Target='Theta', NumberBins=1000, OutputWorkspace='out1')
WANDPowderReduction(InputWorkspace='si1', CalibrationWorkspace='van', Target='Theta', NumberBins=1000, OutputWorkspace='out1_time', NormaliseBy='Time')
WANDPowderReduction(InputWorkspace='si1', CalibrationWorkspace='van', Target='Theta', NumberBins=1000, OutputWorkspace='out1_none', NormaliseBy='None')
WANDPowderReduction(InputWorkspace='si1', CalibrationWorkspace='van', Target='ElasticDSpacing', NumberBins=1000, OutputWorkspace='out1_d')

WANDPowderReduction(InputWorkspace='si2', CalibrationWorkspace='van', Target='Theta', NumberBins=1000, OutputWorkspace='out2')
WANDPowderReduction(InputWorkspace='si2', CalibrationWorkspace='van', Target='Theta', NumberBins=1000, MaskAngle=15, OutputWorkspace='out2_15')
WANDPowderReduction(InputWorkspace='si2', CalibrationWorkspace='van', Target='Theta', NumberBins=1000, OutputWorkspace='out2_time', NormaliseBy='Time')
WANDPowderReduction(InputWorkspace='si2', CalibrationWorkspace='van', Target='Theta', NumberBins=1000, OutputWorkspace='out2_none', NormaliseBy='None')
WANDPowderReduction(InputWorkspace='si2', CalibrationWorkspace='van', Target='ElasticDSpacing', NumberBins=1000, OutputWorkspace='out2_d')


WANDPowderReduction(InputWorkspace='si2', CalibrationWorkspace='van', BackgroundWorkspace='si2',Target='Theta', NumberBins=1000, OutputWorkspace='out2_bg')
