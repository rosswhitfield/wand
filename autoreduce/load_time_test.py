from mantid.simpleapi import *

for run in range(6530,6534):
    ws = LoadNexus('/HFIR/HB2C/IPTS-7776/shared/autoreduce/HB2C_{}.nxs'.format(run))
