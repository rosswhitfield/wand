from mantid.simpleapi import CreateWorkspace, LoadInstrument, SetGoniometer, AddSampleLog
import h5py
import time

run = 6558
t0=time.time()
with h5py.File('HB2C_{}.nxs'.format(run), 'r') as f:
    data = f['data']
    instrument = data.attrs['instrument']
    wavelength = data.attrs['wavelength']
    s1 = data.attrs['s1']
    s2 = data.attrs['s2']
    detz = data.attrs['detz']
    y = data["y"].value
    e = data["e"].value

t1=time.time()

CreateWorkspace(OutputWorkspace='ws', DataX=wavelength, DataY=y, DataE=e, NSpec=y.size, UnitX='Wavelength')
SetGoniometer('ws', Axis0="{},0,1,0,1".format(s1))
AddSampleLog('ws', LogName='HB2C:Mot:s2.RBV', LogText=str(s2), LogType='Number Series')
AddSampleLog('ws', LogName='HB2C:Mot:detz.RBV', LogText=str(detz), LogType='Number Series')
LoadInstrument('ws', InstrumentName=instrument,RewriteSpectraMap=True)

t2=time.time()

print("t1={}".format(t1-t0))
print("t2={}".format(t2-t1))
