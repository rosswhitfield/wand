from mantid.simpleapi import *
import numpy as np

ws = CreateSampleWorkspace()

#create string of workspaces to fit (ws,i0; ws,i1, ws,i2 ...)
workspaces = [ws.name() + ',i%d' % i for i in range(ws.getNumberHistograms())]
workspaces = ';'.join(workspaces)


function = "name=Gaussian,Height=10.0041,PeakCentre=10098.6,Sigma=48.8581"
peaks = PlotPeakByLogValue(workspaces, function, Spectrum=1)

function = "name=Gaussian,Height=10.0041,PeakCentre=10098.6,Sigma=48.8581;name=FlatBackground,A0=0.3"
peaks = PlotPeakByLogValue(workspaces, function, Spectrum=1)
