from mantid.simpleapi import LoadNexus
import numpy as np
import h5py

run=6558

van=LoadNexus('/HFIR/HB2C/IPTS-7776/shared/autoreduce/HB2C_{}.nxs'.format(run))

y=van.extractY()
e=van.extractY()
s2=van.run().getLogData('HB2C:Mot:s2.RBV').timeAverageValue()
detz=van.run().getLogData('HB2C:Mot:detz.RBV').timeAverageValue()
s1=van.run().getLogData('HB2C:Mot:s1').timeAverageValue()
w=1.488

f = h5py.File('HB2C_{}.nxs'.format(run), 'r')
