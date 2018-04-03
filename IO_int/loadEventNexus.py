import h5py
import numpy as np
import time
run=6558
filename='/HFIR/HB2C/IPTS-7776/nexus/HB2C_{}.nxs.h5'.format(run)

instrument='WAND'
wavelenght = 1.488
n=1

pixels = 480*512*8

copy_list = ['title',
             'start_time']

bc = np.empty((pixels),dtype=np.int64)
with h5py.File(filename, 'r') as f_in:
    for b in range(8):
        bc += np.bincount(f_in['/entry/bank'+str(b+1)+'_events/event_id'].value,minlength=pixels)
    s1 = f_in['entry/DASlogs/HB2C:Mot:s1.RBV/average_value'].value[0]
    s2 = f_in['entry/DASlogs/HB2C:Mot:s2.RBV/average_value'].value[0]
    detz = f_in['entry/DASlogs/HB2C:Mot:detz.RBV/average_value'].value[0]
    #title = f_in['entry/title'].value[0]
    #start_time = f_in['entry/start_time'].value[0]
    #instrument_name = f_in['entry/instrument/name']

    with h5py.File('HB2C_{}.nxs'.format(run), 'w') as f_out:
        entry = f_out.create_group("entry{}".format(n))
        entry.attrs['NX_class'] = 'NXentry'

        for item in copy_list:
            entry.copy(f_in['/entry/'+item], item)

        data = entry.create_group("data")
        data.attrs['NX_class'] = 'NXdata'

        y_dset = data.create_dataset("y", data=bc)
        e_dset = data.create_dataset("e", data=bc)

        inst = entry.create_group("instrument")
        inst.attrs['NX_class'] = 'NXinstrument'
        inst.copy(instrument_name)

        #name = inst.create_dataset('name', instrument)
        #name.attrs['short_name'] = 'HB2C'

        mono = inst.create_group("monochromator")
        mono.attrs['NX_class'] = 'NXmonochromator'
        mono.create_dataset('wavelength', w)

        gon = entry.create_group("goniometer")
        gon.attrs['NX_class'] = 'NXtransformations'
        phi = gon.create_dataset('phi', s2)
        phi.attrs['transformation_type'] = 'rotation'
        phi.attrs['vector'] = (0, 1, 0)
        phi.attrs['unit'] = 'degree'

        sample =  entry.create_group("sample")
        sample.attrs['NX_class'] = 'NXsample'

        data.attrs['s2'] = s2
        data.attrs['detz'] = detz
