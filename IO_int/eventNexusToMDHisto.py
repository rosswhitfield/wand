from mantid.simpleapi import CreateMDHistoWorkspace
import h5py
import numpy as np
import datetime
runs=range(15954, 15954+100) #17754+1)
ipts=20367

instrument='WAND'
wavelength = 1.488

pixels = 480*512*8
npoints = len(runs)

data_array = np.empty((npoints, 512, 480*8), dtype=np.int64)
phi_array = np.empty((npoints), dtype=np.float64)

for n, run in enumerate(runs):
    filename='/HFIR/HB2C/IPTS-{}/nexus/HB2C_{}.nxs.h5'.format(ipts,run)
    print(filename)
    with h5py.File(filename, 'r') as f_in:
        bc = np.zeros((pixels),dtype=np.int64)
        for b in range(8):
            bc += np.bincount(f_in['/entry/bank'+str(b+1)+'_events/event_id'].value,minlength=pixels)
        bc=bc.reshape((-1,512)).T
        data_array[n] = bc
        phi_array[n] = f_in['entry/DASlogs/HB2C:Mot:s1.RBV/average_value'].value[0]

print(data_array.shape)

md2=CreateMDHistoWorkspace(SignalInput=data_array.flatten(),
                          ErrorInput=data_array.flatten(),
                          Dimensionality=3,
                          Extents='0.5,3840.5,0.5,512.5,{},{}'.format(phi_array[0],phi_array[-1]),
                          NumberOfBins='{},{},{}'.format(3840,512,npoints),
                          Names='x,y,phi',
                          Units='bin,bin,degrees')
