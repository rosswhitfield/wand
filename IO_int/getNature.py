import h5py
from mantid.simpleapi import LoadEventNexus

filename = '/HFIR/HB2C/IPTS-7776/nexus/HB2C_26625.nxs.h5'

ws = LoadEventNexus(Filename=filename, MetaDataOnly=True)
if ws.run().hasProperty('HB2C:CS:ITEMS:Nature'):
    nature = ws.run().getProperty('HB2C:CS:ITEMS:Nature').value[0]
    print(nature)
    print('Powder: {}'.format(nature == "Powder"))

with h5py.File(filename, 'r') as f:
    if '/entry/DASlogs/HB2C:CS:ITEMS:Nature' in f:
        nature = f['/entry/DASlogs/HB2C:CS:ITEMS:Nature/value'].value[0][0]
        print(nature)
        print('Powder: {}'.format(nature == "Powder"))
