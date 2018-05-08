#LoadWANDSCD(IPTS=20367, RunNumbers='15954-17754', OutputWorkspace='md')
#SaveMD('md','/SNS/users/rwp/IPTS-20367_md.nxs')
md=LoadMD('/SNS/users/rwp/IPTS-20367_md.nxs')
#LoadWANDSCD(IPTS=20367, RunNumbers='15954-16154', OutputWorkspace='md')
ConvertWANDSCDtoQ(InputWorkspace='md', OutputWorkspace='q')
#SaveMD('md','/SNS/users/rwp/IPTS-20367_Q_sample.nxs')

LoadWANDSCD(IPTS=7776, RunNumbers=26509, OutputWorkspace='norm')

ConvertWANDSCDtoQ(InputWorkspace='md', NormalisationWorkspace='norm', OutputWorkspace='q_norm')

# out of bounds
ConvertWANDSCDtoQ(InputWorkspace='md', OutputWorkspace='q',BinningDim2='-5,5,201')



md=LoadMD('/SNS/users/rwp/IPTS-20367_md.nxs')
CreateSingleValuedWorkspace(OutputWorkspace='ub')
LoadIsawUB(InputWorkspace='ub', Filename='/HFIR/HB2C/IPTS-20367/shared/Hexaferrite_200K_2.mat')
ConvertWANDSCDtoQ(InputWorkspace='md', OutputWorkspace='hkl',Frame='HKL', UBWorkspace='ub',BinningDim0='-8.01,8.01,801',BinningDim1='-8.01,8.01,801',BinningDim2='-5.01,5.01,501')

md=LoadMD('/SNS/users/rwp/IPTS-20367_md.nxs')
CreateSingleValuedWorkspace(OutputWorkspace='ub')
LoadIsawUB(InputWorkspace='ub', Filename='/HFIR/HB2C/IPTS-20367/shared/Hexaferrite_200K_2.mat')
ConvertWANDSCDtoQ(InputWorkspace='md', OutputWorkspace='hkl_110',Frame='HKL', UBWorkspace='ub',BinningDim0='-10.025,10.025,401',BinningDim1='-10.025,10.025,401',BinningDim2='-5.02,5.02,251',Uproj='1,1,0',Vproj='1,-1,0',Wproj='0,0,1')



LoadWANDSCD(IPTS=7776, RunNumbers='2952-4753', OutputWorkspace='NaCl')
#LoadWANDSCD(IPTS=7776, RunNumbers='2952-3052', OutputWorkspace='NaCl')
ConvertWANDSCDtoQ(InputWorkspace='NaCl', OutputWorkspace='NaClq')

LoadWANDSCD(IPTS=7776, RunNumbers=2934, OutputWorkspace='NaClnorm')

ConvertWANDSCDtoQ(InputWorkspace='NaCl', NormalisationWorkspace='NaClnorm', OutputWorkspace='NaClq_norm')


##############################

LoadWANDSCD(IPTS=7776, RunNumbers=26509, OutputWorkspace='norm')
LoadWANDSCD(IPTS=20367, RunNumbers=','.join(str(n) for n in range(15954,16954,4)), OutputWorkspace='md')
#LoadWANDSCD(IPTS=20367, RunNumbers=','.join(str(n) for n in range(15954,16754,2)), OutputWorkspace='md')
ConvertWANDSCDtoQ(InputWorkspace='md', OutputWorkspace='q')
ConvertWANDSCDtoQ(InputWorkspace='md', NormalisationWorkspace='norm',OutputWorkspace='q_norm')
ConvertWANDSCDtoQ(InputWorkspace='md', NormalisationWorkspace='norm',OutputWorkspace='q_norm2',BinningDim0='-8.01,8.01,801',BinningDim1='-0.81,0.81,81',BinningDim2='-8.01,8.01,801')

CreateSingleValuedWorkspace(OutputWorkspace='ub')
LoadIsawUB(InputWorkspace='ub', Filename='/HFIR/HB2C/IPTS-20367/shared/Hexaferrite_200K_2.mat')
ConvertWANDSCDtoQ(InputWorkspace='md', OutputWorkspace='hkl',Frame='HKL', UBWorkspace='ub',BinningDim0='-8.01,8.01,401',BinningDim1='-8.01,8.01,401',BinningDim2='-5.01,5.01,251')
ConvertWANDSCDtoQ(InputWorkspace='md', NormalisationWorkspace='norm', OutputWorkspace='hkl_norm',Frame='HKL', UBWorkspace='ub',BinningDim0='-8.02,8.02,401',BinningDim1='-8.02,8.02,401',BinningDim2='-5.02,5.02,251')

ConvertWANDSCDtoQ(InputWorkspace='md', OutputWorkspace='hkl_110',Frame='HKL', UBWorkspace='ub',BinningDim0='-10.025,10.025,401',BinningDim1='-10.025,10.025,401',BinningDim2='-5.02,5.02,251',Uproj='1,1,0',Vproj='1,-1,0',Wproj='0,0,1')

ConvertWANDSCDtoQ(InputWorkspace='md', NormalisationWorkspace='norm', OutputWorkspace='hkl_110_norm',Frame='HKL', UBWorkspace='ub',BinningDim0='-10.025,10.025,401',BinningDim1='-10.025,10.025,401',BinningDim2='-5.02,5.02,251',Uproj='1,1,0',Vproj='1,-1,0',Wproj='0,0,1')



ConvertWANDSCDtoQ(InputWorkspace='md', NormalisationWorkspace='norm', OutputWorkspace='hkl',Frame='HKL', UBWorkspace='ub',BinningDim0='-10.025,10.025,401',BinningDim1='-10.025,10.025,401',BinningDim2='-5.02,5.02,251',Uproj='1,0,0',Vproj='0,1,0',Wproj='0,0,1')

ConvertWANDSCDtoQ(InputWorkspace='md', NormalisationWorkspace='norm', OutputWorkspace='hkl_-1',Frame='HKL', UBWorkspace='ub',BinningDim0='-10.025,10.025,401',BinningDim1='-10.025,10.025,401',BinningDim2='-5.02,5.02,251',Uproj='-1,0,0',Vproj='0,1,0',Wproj='0,0,1')

ConvertWANDSCDtoQ(InputWorkspace='md', NormalisationWorkspace='norm', OutputWorkspace='hkl_0-1',Frame='HKL', UBWorkspace='ub',BinningDim0='-10.025,10.025,401',BinningDim1='-10.025,10.025,401',BinningDim2='-5.02,5.02,251',Uproj='1,0,0',Vproj='0,-1,0',Wproj='0,0,1')

ConvertWANDSCDtoQ(InputWorkspace='md', NormalisationWorkspace='norm', OutputWorkspace='khl',Frame='HKL', UBWorkspace='ub',BinningDim0='-10.025,10.025,401',BinningDim1='-10.025,10.025,401',BinningDim2='-5.02,5.02,251',Uproj='0,1,0',Vproj='1,0,0',Wproj='0,0,1')



ConvertWANDSCDtoQ(InputWorkspace='md', NormalisationWorkspace='norm', OutputWorkspace='hkl_110_2',Frame='HKL', UBWorkspace='ub',BinningDim0='-4.51,4.51,451',BinningDim1='-7.52,7.52,376',BinningDim2='-4.08,4.08,51',Uproj='1,1,0',Vproj='1,-1,0',Wproj='0,0,1')
