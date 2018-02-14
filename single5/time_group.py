from mantid.simpleapi import LoadNexus, LoadMD

for _ in range(5):
    ws1=LoadNexus('/HFIR/HB2C/IPTS-7776/shared/autoreduce/HB2C_3000.nxs')
    ws2=LoadNexus('/HFIR/HB2C/IPTS-7776/shared/autoreduce/HB2C_3000_group_4x4.nxs')
    md1=LoadMD('/HFIR/HB2C/IPTS-7776/shared/autoreduce/HB2C_3000_MDE.nxs')
    md2=LoadMD('/HFIR/HB2C/IPTS-7776/shared/autoreduce/HB2C_3000_group_4x4_MDE.nxs')
    print()
