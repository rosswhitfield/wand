from mantid.simpleapi import *
import numpy as np

van=LoadNexus('/HFIR/HB2C/IPTS-7776/shared/autoreduce/HB2C_{}.nxs'.format(6558))

a=van.extractY()
new=np.random.random(a.shape)

for n, val in enumerate(new):
    van.setY(n,val)
