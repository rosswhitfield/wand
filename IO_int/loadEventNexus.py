import h5py
import numpy as np
run=6558
filename='/HFIR/HB2C/IPTS-7776/nexus/HB2C_{}.nxs.h5'.format(run)

#f=h5py.File(filename, 'r')
#entry=f["entry"]

instrument='WAND'
wavelenght = 1.488

pixels = 480*512*8

values = np.empty((0),dtype=np.int64)
histo = np.zeros((pixels),dtype=np.int64)
with h5py.File(filename, 'r') as f:
    for b in range(8):
        values = np.concatenate((values,f['/entry/bank'+str(b+1)+'_events/event_id'].value))
    s1 = f['entry/DASlogs/HB2C:Mot:s1.RBV/average_value'].value[0]
    s2 = f['entry/DASlogs/HB2C:Mot:s2.RBV/average_value'].value[0]
    detz = f['entry/DASlogs/HB2C:Mot:detz.RBV/average_value'].value[0]


bc=np.bincount(values,minlength=512*480*8)

#%timeit np.bincount(values)
#%timeit np.histogram(values)
