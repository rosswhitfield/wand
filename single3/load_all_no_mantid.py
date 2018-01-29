import numpy as np
import matplotlib.pyplot as plt
import h5py

runs=range(2952,4754)
runs=range(2952,2984)

a=np.zeros((len(runs),480*8,512))
angle=np.zeros(len(runs))
    
for i, run in enumerate(runs):
    with h5py.File('/HFIR/HB2C/IPTS-7776/shared/autoreduce/HB2C_{}.nxs'.format(run)) as f:
        a[i] = f['mantid_workspace_1/worksapce/values'].value.reshape((3840,512))
        #a[i]=md.extractY().reshape((3840,512))
        #angle[i]=md.run().getLogData("HB2C:Mot:s1").lastValue()
        angle[i]=f['mantid_workspace_1/logs/HB2C:Mot:s1/values'].value[0]

#np.save('/SNS/users/rwp/a.npy',a)
#np.save('/SNS/users/rwp/angle.npy',angle)
