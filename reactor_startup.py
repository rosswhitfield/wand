from mantid.simpleapi import *

ws=LoadEventNexus('/HFIR/HB2C/IPTS-7776/nexus/HB2C_6560.nxs.h5')
ws=SumSpectra(ws)
ws=RebinByPulseTimes(ws, 1)
