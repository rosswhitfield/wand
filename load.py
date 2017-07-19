import h5py
import matplotlib.pyplot as plt
import numpy as np

values = np.empty((0),dtype=np.int64)
with h5py.File('WAND_1002.nxs.h5', 'r') as f:
    for b in range(8):
        values = np.concatenate((values,f['/entry/bank'+str(b+1)+'_events/event_id'].value))

bc=np.bincount(values,minlength=512*480*8)

bcc=bc.reshape((-1,512))
plt.imshow(bcc.T)
plt.show()
