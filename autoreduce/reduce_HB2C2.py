#!/usr/bin/env python
from __future__ import (absolute_import, division, print_function, unicode_literals)
import os
import sys
import h5py
import numpy as np
try:
    from postprocessing.publish_plot import publish_plot, plot_heatmap
except ImportError:
    from finddata.publish_plot import publish_plot, plot_heatmap

filename = sys.argv[1]
output_file = os.path.split(filename)[-1].replace('.nxs.h5', '')
outdir = sys.argv[2]


def decode(value):
    try:
        return value.decode()
    except:
        return value

powder = False

with h5py.File(filename, 'r') as f:
    if '/entry/DASlogs/HB2C:CS:ITEMS:Nature' in f:
        nature = decode(f['/entry/DASlogs/HB2C:CS:ITEMS:Nature/value'].value[0][0])
        if nature == 'Powder':
            powder = True
    if '/entry/notes' in f:
        notes = decode(f['/entry/notes'].value[0].tostring().lower())
        if 'powder' in notes:
            powder = True


def get_vanadium(run_number, npy=False):
    """
    Pre-process vanadium only the first time it's used
    """
    vanadiums = sorted(int(n.replace('HB2C_', '').replace('.nxs.h5', ''))
                       for n in os.listdir('/HFIR/HB2C/shared/Vanadium')
                       if 'HB2C_' in n and '.nxs.h5' in n)
    van_run_number = vanadiums[np.searchsorted(vanadiums, run_number, side='right')-1]
    upstream_van_file = '/HFIR/HB2C/shared/Vanadium/HB2C_{}.nxs.h5'.format(van_run_number)
    if npy:
        npy_van_file = '/HFIR/HB2C/shared/autoreduce/vanadium/HB2C_{}.npy'.format(van_run_number)
        if os.path.exists(npy_van_file):
            return np.load(npy_van_file)
        else:
            with h5py.File(upstream_van_file, 'r') as f:
                bc = np.zeros((512*480*8))
                for b in range(8):
                    bc += np.bincount(f['/entry/bank'+str(b+1)+'_events/event_id'].value,
                                      minlength=512*480*8)
                bc = bc.reshape((480*8, 512))
                bc = (bc[::4, ::4] + bc[1::4, ::4] + bc[2::4, ::4] + bc[3::4, ::4]
                      + bc[::4, 1::4] + bc[1::4, 1::4] + bc[2::4, 1::4] + bc[3::4, 1::4]
                      + bc[::4, 2::4] + bc[1::4, 2::4] + bc[2::4, 2::4] + bc[3::4, 2::4]
                      + bc[::4, 3::4] + bc[1::4, 3::4] + bc[2::4, 3::4] + bc[3::4, 3::4])
            np.save(npy_van_file, bc)
            return bc
    else:
        from mantid.simpleapi import LoadWAND, LoadNexus, SaveNexus
        nxs_van_file = '/HFIR/HB2C/shared/autoreduce/vanadium/HB2C_{}.nxs'.format(van_run_number)
        if os.path.exists(nxs_van_file):
            ws = LoadNexus(nxs_van_file)
        else:
            ws = LoadWAND(upstream_van_file, Grouping='4x4')
            SaveNexus(ws, nxs_van_file)
        return ws

if powder:

    from mantid.simpleapi import LoadWAND, WANDPowderReduction, SavePlot1D, SaveFocusedXYE, Scale

    data = LoadWAND(filename, Grouping='4x4')
    runNumber = data.getRunNumber()
    cal = get_vanadium(runNumber)
    WANDPowderReduction(InputWorkspace=data,
                        CalibrationWorkspace=cal,
                        Target='Theta',
                        NumberBins=1200,
                        OutputWorkspace='reduced')
    Scale(InputWorkspace='reduced',OutputWorkspace='reduced',Factor=100)
    SaveFocusedXYE('reduced', Filename=os.path.join(outdir, output_file+'.xye'), SplitFiles=False, IncludeHeader=False)
    div = SavePlot1D('reduced', OutputType='plotly')
    request = publish_plot('HB2C', runNumber, files={'file': div})

else:  # Single Crystal

    with h5py.File(filename, 'r') as f:
        offset = decode(f['/entry/DASlogs/HB2C:Mot:s2.RBV/average_value'].value[0])
        title = decode(f['/entry/title'].value[0])
        mon = decode(f['/entry/monitor1/total_counts'].value[0])
        duration = decode(f['/entry/duration'].value[0])
        run_number = decode(f['/entry/run_number'].value[0])
        bc = np.zeros((512*480*8))
        for b in range(8):
            bc += np.bincount(f['/entry/bank'+str(b+1)+'_events/event_id'].value,
                              minlength=512*480*8)
        bc = bc.reshape((480*8, 512))
        bc = (bc[::4, ::4] + bc[1::4, ::4] + bc[2::4, ::4] + bc[3::4, ::4]
              + bc[::4, 1::4] + bc[1::4, 1::4] + bc[2::4, 1::4] + bc[3::4, 1::4]
              + bc[::4, 2::4] + bc[1::4, 2::4] + bc[2::4, 2::4] + bc[3::4, 2::4]
              + bc[::4, 3::4] + bc[1::4, 3::4] + bc[2::4, 3::4] + bc[3::4, 3::4])

    vanadium = get_vanadium(run_number, npy=True)
    vanadium_mon = 163519902  # ?
    bc = bc / vanadium * vanadium_mon / mon

    plot_heatmap(run_number,
                 np.linspace(120+offset, offset, 960), np.arange(0, 128), bc.T,
                 x_title=u'2theta', instrument='HB2C')
