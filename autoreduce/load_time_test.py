from mantid.simpleapi import LoadNexus

for run in range(6530,6534):
    print('HB2C_{}.nxs'.format(run))
    ws = LoadNexus('/HFIR/HB2C/IPTS-7776/shared/autoreduce/HB2C_{}.nxs'.format(run))
