from mantid.simpleapi import LoadEventNexus
ws = LoadEventNexus(Filename='/HFIR/HB2C/IPTS-7776/nexus/HB2C_26625.nxs.h5', MetaDataOnly=True)
if ws.run().hasProperty('HB2C:CS:ITEMS:Nature'):
    nature = ws.run().getProperty('HB2C:CS:ITEMS:Nature').value[0]
    print(nature)
    print('Powder: {}'.format(nature == "Powder"))
