from mantid.simpleapi import *
import numpy as np
import matplotlib.pyplot as plt

runs=range(2952,4754)
runs=range(2996,3007)

a=np.zeros((len(runs),480*2,128))
angle=np.zeros(len(runs))
    
for i, run in enumerate(runs):
    md=LoadNexus(Filename='/HFIR/HB2C/IPTS-7776/shared/autoreduce/HB2C_{}_group_4x4.nxs'.format(run))
    a[i]=md.extractY().reshape((960,128))
    angle[i]=md.run().getLogData("HB2C:Mot:s1").lastValue()

#np.save('/SNS/users/rwp/a.npy',a)
#np.save('/SNS/users/rwp/angle.npy',angle)
