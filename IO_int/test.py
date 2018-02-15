from mantid.simpleapi import *
import numpy as np

van=LoadNexus('/HFIR/HB2C/IPTS-7776/shared/autoreduce/HB2C_{}.nxs'.format(6558))

y=van.extractY()
e=van.extractY()
x=np.full(y.shape, 1.488)
w=1.488

CreateWorkspace(OutputWorkspace='new', DataX=1.488, DataY=y, DataE=e, NSpec=y.size, UnitX='Wavelength')

LoadInstrument('new', InstrumentName='WAND')
