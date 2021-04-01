# import mantid algorithms, numpy and matplotlib
from mantid.simpleapi import *
import matplotlib.pyplot as plt
import numpy as np

ws=CreateSampleWorkspace()
peaks=CreatePeaksWorkspace(ws, 0)
SetUB(peaks, a=5, b=5, c=5)

peaks2=CreatePeaksWorkspace()

for vector in [[i,j,k] for i in (0,1) for j in (0,1) for k in (0,1) if not (i==j==k)]:
    p = peaks.createPeakHKL(vector)
    peaks2.addPeak(p)

