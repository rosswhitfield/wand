import numpy as np
import matplotlib.pyplot as plt
import h5py
import time

run=2933
with h5py.File('/HFIR/HB2C/IPTS-7776/shared/autoreduce/HB2C_{}_group_4x4.nxs'.format(run)) as f:
    van = f['mantid_workspace_1/workspace/values'].value.reshape((960,128))

runs=range(2952,4754)
runs=range(2996,3780)

a=np.zeros((len(runs),480*2,128))
angle=np.zeros(len(runs))
t0=time.time()
for i, run in enumerate(runs):
    print(run)
    with h5py.File('/HFIR/HB2C/IPTS-7776/shared/autoreduce/HB2C_{}_group_4x4.nxs'.format(run)) as f:
        a[i] = f['mantid_workspace_1/workspace/values'].value.reshape((960,128))
        angle[i] = f['mantid_workspace_1/logs/HB2C:Mot:s1/value'].value[0]
    t1=time.time()
    print(t1-t0)
    t0=t1

#np.save('/SNS/users/rwp/a.npy',a)
#np.save('/SNS/users/rwp/angle.npy',angle)
plt.imshow(a[:,:,0])
plt.show()
plt.imshow(a.sum(axis=2))
plt.show()
