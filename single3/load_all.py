from mantid.simpleapi import *
import numpy as np
import matplotlib.pyplot as plt

runs=range(2952,4754)
runs=range(2952,2968)

a=np.zeros((len(runs),512,480*8))
angle=np.zeros(len(runs))
    
for i, run in enumerate(runs):
    md=LoadNexus(Filename='/HFIR/HB2C/IPTS-7776/shared/autoreduce/HB2C_{}.nxs'.format(run))
    a[i]=md.extractY().reshape((512,3840))
    angle[i]=md.run().getLogData("HB2C:Mot:s1").lastValue()

#np.save('/SNS/users/rwp/a.npy',a)
#np.save('/SNS/users/rwp/angle.npy',angle)
