from wand import convertToQSample, convertQSampleToHKL, accumulateMD
from mantid.simpleapi import LoadNexus, LoadMD

van = LoadNexus('/HFIR/HB2C/IPTS-7776/shared/autoreduce/HB2C_{}.nxs'.format(6558))

for filename in ['/HFIR/HB2C/IPTS-7776/shared/rwp/PNOe/HB2C_{}_MDE.nxs'.format(run) for run in range(4756,6557,100)]:
                 LoadMD(Filename=filename, LoadHistory=False, OutputWorkspace='md')
                 accumulateMD('md', OutputWorkspace='data')


UB=[1,0,0,0,1,0,0,0,1]

convertQSampleToHKL('data','hkl')
