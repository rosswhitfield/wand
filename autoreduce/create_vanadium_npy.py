with h5py.File(filename, 'r') as f:
        offset=f['/entry/DASlogs/HB2C:Mot:s2.RBV/average_value'].value[0]
        title=f['/entry/title'].value[0]
        bc = np.zeros((512*480*8),dtype=np.int64)
        for b in range(8):
                bc += np.bincount(f['/entry/bank'+str(b+1)+'_events/event_id'].value,minlength=512*480*8)
        bc = bc.reshape((480*8, 512))
        bc = (bc[::4,::4]    + bc[1::4,::4]  + bc[2::4,::4]  + bc[3::4,::4]
              + bc[::4,1::4] + bc[1::4,1::4] + bc[2::4,1::4] + bc[3::4,1::4]
              + bc[::4,2::4] + bc[1::4,2::4] + bc[2::4,2::4] + bc[3::4,2::4]
              + bc[::4,3::4] + bc[1::4,3::4] + bc[2::4,3::4] + bc[3::4,3::4])
