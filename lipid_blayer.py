LoadWANDSCD(IPTS='17751', RunNumbers='64974-65134', OutputWorkspace='DPPC')
LoadWANDSCD(IPTS='7776', RunNumbers='124736', OutputWorkspace='vanadium')

ReplicateMD(ShapeWorkspace='DPPC', DataWorkspace='vanadium', OutputWorkspace='vanadium')
DivideMD(LHSWorkspace='DPPC', RHSWorkspace='vanadium', OutputWorkspace='DPPC')

IntegrateMDHistoWorkspace(InputWorkspace='DPPC', P1Bin='160,350', OutputWorkspace='DPPC_int')
