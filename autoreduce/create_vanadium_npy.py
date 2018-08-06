import numpy as np
import h5py

runNumber = 29780

with h5py.File('/HFIR/HB2C/IPTS-7776/nexus/HB2C_{}.nxs.h5'.format(runNumber), 'r') as f:
    bc = np.zeros((512*480*8))
    for b in range(8):
        bc += np.bincount(f['/entry/bank'+str(b+1)+'_events/event_id'].value,minlength=512*480*8)
    bc = bc.reshape((480*8, 512))
    bc = (bc[::4,::4]    + bc[1::4,::4]  + bc[2::4,::4]  + bc[3::4,::4]
          + bc[::4,1::4] + bc[1::4,1::4] + bc[2::4,1::4] + bc[3::4,1::4]
          + bc[::4,2::4] + bc[1::4,2::4] + bc[2::4,2::4] + bc[3::4,2::4]
          + bc[::4,3::4] + bc[1::4,3::4] + bc[2::4,3::4] + bc[3::4,3::4])

np.save('vanadium_{}.npy'.format(runNumber), bc)
