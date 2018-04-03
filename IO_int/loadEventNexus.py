import h5py
import numpy as np
import time
run=6558
filename='/HFIR/HB2C/IPTS-7776/nexus/HB2C_{}.nxs.h5'.format(run)

#f=h5py.File(filename, 'r')
#entry=f["entry"]

instrument='WAND'
wavelenght = 1.488
n=1

pixels = 480*512*8

bc = np.empty((pixels),dtype=np.int64)
with h5py.File(filename, 'r') as f:
    for b in range(8):
        bc += np.bincount(f['/entry/bank'+str(b+1)+'_events/event_id'].value,minlength=pixels)
    s1 = f['entry/DASlogs/HB2C:Mot:s1.RBV/average_value'].value[0]
    s2 = f['entry/DASlogs/HB2C:Mot:s2.RBV/average_value'].value[0]
    detz = f['entry/DASlogs/HB2C:Mot:detz.RBV/average_value'].value[0]

with h5py.File('HB2C_{}.nxs'.format(run), 'w') as f:
    entry = f.create_group("entry{}".format(n))
    entry.attrs['NX_class'] = 'NXentry'

    data = entry.create_group("data")
    data.attrs['NX_class'] = 'NXdata'

    y_dset = data.create_dataset("y", data=bc)
    e_dset = data.create_dataset("e", data=bc)

    inst = entry.create_group("instrument")
    inst.attrs['NX_class'] = 'NXinstrument'

    name = inst.create_dataset('name', instrument)
    name.attrs['short_name'] = 'HB2C'

    mono = inst.create_group("monochromator")
    mono.attrs['NX_class'] = 'NXmonochromator'
    mono.create_dataset('wavelength', w)

    sample = entry.create_group("sample")
    sample.attrs['NX_class'] = 'NXsample'
    rot = sample.create_dataset('rotation_angle', s2)
    rot.attrs['unit'] = 'degree'


    data.attrs['s2'] = s2
    data.attrs['detz'] = detz
