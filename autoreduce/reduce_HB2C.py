#!/usr/bin/env python2
import os
import sys
import h5py

filename = sys.argv[1]
output_file=os.path.split(filename)[-1].replace('.nxs.h5','')
outdir = sys.argv[2]

powder=False

with h5py.File(filename, 'r') as f:
    if '/entry/DASlogs/HB2C:CS:ITEMS:Nature' in f:
        nature = f['/entry/DASlogs/HB2C:CS:ITEMS:Nature/value'].value[0][0]
        if nature == 'Powder':
            powder=True

if powder:
    sys.path.append("/opt/mantidnightly/bin")
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
    import matplotlib as mpl
    mpl.use( "agg" )
    import matplotlib.pyplot as plt
    #from matplotlib.image import imsave
    import numpy as np
    with h5py.File(filename, 'r') as f:
        offset=f['/entry/DASlogs/HB2C:Mot:s2.RBV/average_value'].value[0]
        print(offset)
        bc = np.zeros((512*480*8),dtype=np.int64)
        for b in range(8):
            bc += np.bincount(f['/entry/bank'+str(b+1)+'_events/event_id'].value,minlength=512*480*8)
        bc = bc.reshape((480*8, 512))
        bc = (bc[::4,::4]    + bc[1::4,::4]  + bc[2::4,::4]  + bc[3::4,::4]
              + bc[::4,1::4] + bc[1::4,1::4] + bc[2::4,1::4] + bc[3::4,1::4]
              + bc[::4,2::4] + bc[1::4,2::4] + bc[2::4,2::4] + bc[3::4,2::4]
              + bc[::4,3::4] + bc[1::4,3::4] + bc[2::4,3::4] + bc[3::4,3::4])
    f, (ax1, ax2) = plt.subplots(2)
    ax1.set_title(u'{}, s2={:.2f}°'.format(output_file,offset))
    ax1.plot(np.linspace(offset,120+offset,960),bc.sum(1))
    ax1.set_xlim(offset,120+offset)
    ax2.imshow(bc.T[::-1,::-1], cmap='viridis',aspect=1/7.5,extent=(offset,120+offset,0,128),vmin=0,vmax=np.sqrt(bc.max()))
    ax2.set_xlabel('2theta')
    ax2.set_xlim(offset,120+offset)
    ax2.set_ylim(0,128)
    ax2.get_yaxis().set_visible(False)
    #f.subplots_adjust(top=0)
    f.tight_layout()
    plt.savefig(outdir+output_file)
    
    #imsave(outdir+output_file, bc.T)
