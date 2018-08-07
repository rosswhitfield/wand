#!/usr/bin/env python2
import os
import sys
import h5py
try:
    from postprocessing.publish_plot import publish_plot, plot_heatmap
except ImportError:
    from finddata import publish_plot

filename = sys.argv[1]
output_file = os.path.split(filename)[-1].replace('.nxs.h5', '')
outdir = sys.argv[2]

powder = False

with h5py.File(filename, 'r') as f:
    if '/entry/DASlogs/HB2C:CS:ITEMS:Nature' in f:
        nature = f['/entry/DASlogs/HB2C:CS:ITEMS:Nature/value'].value[0][0]
        if nature == 'Powder':
            powder = True

if powder:

    sys.path.append("/opt/mantidnightly/bin")
    from mantid.simpleapi import LoadWAND, WANDPowderReduction, SavePlot1D

    data = LoadWAND(filename)
    runNumber = data.getRunNumber()
    cal = LoadWAND(IPTS=7776, RunNumbers=101567)
    WANDPowderReduction(InputWorkspace=data,
                        CalibrationWorkspace=cal,
                        Target='Theta',
                        NumberBins=1000,
                        OutputWorkspace='reduced')
    div = SavePlot1D('reduced', OutputType='plotly')
    request = publish_plot('HB2C', runNumber, files={'file': div})

else:  # Single Crystal

    from plotly.offline import plot
    import plotly.graph_objs as go
    import numpy as np
    with h5py.File(filename, 'r') as f:
        offset = f['/entry/DASlogs/HB2C:Mot:s2.RBV/average_value'].value[0]
        title = f['/entry/title'].value[0]
        mon = f['/entry/monitor1/total_counts'].value[0]
        duration = f['/entry/duration'].value[0]
        run_number = f['/entry/run_number'].value[0]
        bc = np.zeros((512*480*8))
        for b in range(8):
            bc += np.bincount(f['/entry/bank'+str(b+1)+'_events/event_id'].value,
                              minlength=512*480*8)
        bc = bc.reshape((480*8, 512))
        bc = (bc[::4, ::4] + bc[1::4, ::4] + bc[2::4, ::4] + bc[3::4, ::4]
              + bc[::4, 1::4] + bc[1::4, 1::4] + bc[2::4, 1::4] + bc[3::4, 1::4]
              + bc[::4, 2::4] + bc[1::4, 2::4] + bc[2::4, 2::4] + bc[3::4, 2::4]
              + bc[::4, 3::4] + bc[1::4, 3::4] + bc[2::4, 3::4] + bc[3::4, 3::4])

    vanadium = np.load('/HFIR/HB2C/shared/autoreduce/vanadium_101567.npy')
    vanadium_mon = 163519902
    bc = bc / vanadium * vanadium_mon / mon

    plot_heatmap(run_number,
                 np.linspace(120+offset,offset,960), np.arange(0,128), bc.T,
                 x_title=u'2theta', instrument='HB2C')
