from mantid.simpleapi import *
import numpy as np
import matplotlib.pyplot as plt

runs=range(2952,4754)
runs=range(2952,2984)

a=np.zeros((len(runs),480*8,512))
angle=np.zeros(len(runs))
    
for i, run in enumerate(runs):
    md=LoadNexus(Filename='/HFIR/HB2C/IPTS-7776/shared/autoreduce/HB2C_{}.nxs'.format(run))
    a[i]=md.extractY().reshape((3840,512))
    angle[i]=md.run().getLogData("HB2C:Mot:s1").lastValue()

#np.save('/SNS/users/rwp/a.npy',a)
#np.save('/SNS/users/rwp/angle.npy',angle)
