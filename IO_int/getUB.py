from mantid.simpleapi import LoadEventNexus
ws = LoadEventNexus(Filename='/HFIR/HB2C/IPTS-7776/nexus/HB2C_26625.nxs.h5', MetaDataOnly=True)
if ws.run().hasProperty('HB2C:CS:CrystalAlign:UBMatrix'):
    ub = ','.join(ws.run().getProperty('HB2C:CS:CrystalAlign:UBMatrix').value[0].replace('[','').replace(']','').split())
    print(ub)
