from mantid.simpleapi import *
LoadMD('HB3A_data.nxs', OutputWorkspace='ConvertHFIRSCDtoMDE_HB3ATest_data')
SetGoniometer('ConvertHFIRSCDtoMDE_HB3ATest_data',
              Axis0='omega,0,1,0,-1',
              Axis1='chi,0,0,1,-1',
              Axis2='phi,0,1,0,-1')
ConvertHFIRSCDtoMDETest_Q = ConvertHFIRSCDtoMDE(InputWorkspace='ConvertHFIRSCDtoMDE_HB3ATest_data',
                                                Wavelength=1.008)
SaveMD(ConvertHFIRSCDtoMDETest_Q, '/tmp/md.nxs')
md=LoadMD('/tmp/md.nxs')
md_ref=LoadMD('ConvertHFIRSCDtoMDE_HB3A_Test.nxs')
print(md.getNEvents())
print(md_ref.getNEvents())
