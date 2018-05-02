#!/usr/bin/env python2
import sys
import h5py

filename = sys.argv[1]
outdir = sys.argv[2]

with h5py.File(filename, 'r') as f:
    if '/entry/DASlogs/HB2C:CS:ITEMS:Nature' in f:
        nature = f['/entry/DASlogs/HB2C:CS:ITEMS:Nature/value'].value[0][0]
        if nature != 'Powder':
            print("Sample is {}, skipping autoreduction\nAutoreduction is only run on Powder samples".format(nature))
            sys.exit()
    else:
        print("Sample Nature not found, skipping autoreduction")
        sys.exit()

sys.path.append("/opt/mantidnightly/bin")
from mantid.simpleapi import LoadWAND, WANDPowderReduction, SavePlot1D

van_file = '/HFIR/HB2C/IPTS-7776/nexus/HB2C_26509.nxs.h5'

data = LoadWAND(filename)
runNumber = data.getRunNumber()
cal = LoadWAND(van_file)
WANDPowderReduction(InputWorkspace=data,
                    CalibrationWorkspace=cal,
                    Target='Theta',
                    NumberBins=1000,
                    OutputWorkspace='reduced')
div = SavePlot1D('reduced', OutputType='plotly')
from postprocessing.publish_plot import publish_plot
request = publish_plot('HB2C', runNumber, files={'file': div})
