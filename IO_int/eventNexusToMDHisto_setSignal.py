from mantid.simpleapi import CreateMDHistoWorkspace, CreateMDWorkspace, BinMD
import h5py
import numpy as np
import time
runs=range(15954, 15954+1801) #17754+1)
ipts=20367

instrument='WAND'
wavelength = 1.488

pixels = 480*512*8
npoints = len(runs)

t0=time.time()
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

t1=time.time()
print(t1-t0)
print(data_array.shape)

mdws = CreateMDWorkspace(Dimensions=3, Extents='-10,10,-10,10,-10,10', Names='A,B,C', Units='U,U,U')
t2=time.time()
binned_ws = BinMD(InputWorkspace=mdws, AlignedDim0='A,0,10,1801', AlignedDim1='B,-10,10,512', AlignedDim2='C,-10,10,3840')
t3=time.time()
binned_ws.setSignalArray(data_array)
t4=time.time()
print(t2-t1)
print(t3-t2)
print(t4-t3)
