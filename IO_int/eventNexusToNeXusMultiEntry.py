import h5py
import numpy as np
import datetime
runs=[26565,26584]
ipts=20325
out_filename='HB2C_{}.nxs'.format('test')

instrument='WAND'
wavelength = 1.488
n=0

pixels = 480*512*8

copy_list = ['title',
             'start_time',
             'end_time',
             'duration',
             'entry_identifier',
             'experiment_identifier',
             'experiment_title']

with h5py.File(out_filename, 'w') as f_out:
    f_out.attrs['NX_class'] = 'NXroot'
    f_out.attrs['file_time'] = datetime.datetime.now().isoformat()
    f_out.attrs['file_name'] = out_filename
    f_out.attrs['HDF5_Version'] = h5py.version.hdf5_version
    f_out.attrs['h5py_version'] = h5py.version.version
    f_out.attrs['default'] = 'entry1'

    for run in runs:
        n+=1
        filename='/HFIR/HB2C/IPTS-{}/nexus/HB2C_{}.nxs.h5'.format(ipts,run)
        with h5py.File(filename, 'r') as f_in:
            bc = np.zeros((pixels),dtype=np.int64)
            for b in range(8):
                bc += np.bincount(f_in['/entry/bank'+str(b+1)+'_events/event_id'].value,minlength=pixels)
            bc=bc.reshape((-1,512))
            s1 = f_in['entry/DASlogs/HB2C:Mot:s1.RBV/average_value'].value[0]
            s2 = f_in['entry/DASlogs/HB2C:Mot:s2.RBV/average_value'].value[0]
            detz = f_in['entry/DASlogs/HB2C:Mot:detz.RBV/average_value'].value[0]

            entry = f_out.create_group("entry{}".format(n))
            entry.attrs['NX_class'] = 'NXentry'

            for item in copy_list:
                entry.copy(f_in['/entry/'+item], item)

            data = entry.create_group("data")
            data.attrs['NX_class'] = 'NXdata'
            data.attrs['signal'] = 'counts'

            counts = data.create_dataset("counts", data=bc.T)

            inst = entry.create_group("instrument")
            inst.attrs['NX_class'] = 'NXinstrument'
            inst.copy(f_in['entry/instrument/name'], 'name')

            mono = inst.create_group("monochromator")
            mono.attrs['NX_class'] = 'NXmonochromator'
            wl = mono.create_dataset('wavelength', shape=(1,), data=wavelength)
            wl.attrs['units'] = 'Angstrom'

            gon = inst.create_group("goniometer")
            gon.attrs['NX_class'] = 'NXtransformations'
            phi = gon.create_dataset('phi', shape=(1,), data=s1)
            phi.attrs['transformation_type'] = 'rotation'
            phi.attrs['vector'] = np.array([0, 1, 0])
            phi.attrs['unit'] = 'degrees'

            det = inst.create_group("detector")
            sample.attrs['NX_class'] = 'NXdetector'
            # radius
            # active_height
            # active_width
            # total_counts
            # x_pixel_angular_offset
            # y_pixel_offset

            data.attrs['s2'] = s2
            data.attrs['detz'] = detz
