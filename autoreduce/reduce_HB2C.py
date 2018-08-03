#!/usr/bin/env python2
import sys
import h5py

filename = sys.argv[1]
outdir = sys.argv[2]

powder=True

with h5py.File(filename, 'r') as f:
    if '/entry/DASlogs/HB2C:CS:ITEMS:Nature' in f:
        nature = f['/entry/DASlogs/HB2C:CS:ITEMS:Nature/value'].value[0][0]
        if nature != 'Powder':
            powder=False
            print("Sample is {}, skipping autoreduction\nAutoreduction is only run on Powder samples".format(nature))
            #sys.exit()
    else:
        print("Sample Nature not found, skipping autoreduction")
        sys.exit()

sys.path.append("/opt/mantidnightly/bin")

if powder:
    from mantid.simpleapi import LoadWAND, WANDPowderReduction, SavePlot1D

    data = LoadWAND(filename)
    runNumber = data.getRunNumber()
    cal = LoadWAND(IPTS=7776,RunNumbers=29780)
    WANDPowderReduction(InputWorkspace=data,
                        CalibrationWorkspace=cal,
                        Target='Theta',
                        NumberBins=1000,
                        OutputWorkspace='reduced')
    div = SavePlot1D('reduced', OutputType='plotly')
    from postprocessing.publish_plot import publish_plot
    request = publish_plot('HB2C', runNumber, files={'file': div})


else: # Single Crystal
    import matplotlib
    import numpy as np
    with h5py.File(filename, 'r') as f:
        bc = np.zeros((512*480*8),dtype=np.int64)
        for b in range(8):
            bc += np.bincount(f['/entry/bank'+str(b+1)+'_events/event_id'].value,minlength=512*480*8)
        bc = bc.reshape((480*8, 512))
        bc = (bc[::4,::4]    + bc[1::4,::4]  + bc[2::4,::4]  + bc[3::4,::4]
              + bc[::4,1::4] + bc[1::4,1::4] + bc[2::4,1::4] + bc[3::4,1::4]
              + bc[::4,2::4] + bc[1::4,2::4] + bc[2::4,2::4] + bc[3::4,2::4]
              + bc[::4,3::4] + bc[1::4,3::4] + bc[2::4,3::4] + bc[3::4,3::4])
    matplotlib.image.imsave(outdir+'file.png', bc)
