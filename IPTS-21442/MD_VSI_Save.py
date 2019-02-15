ws = LoadMD('/SNS/users/rwp/wand/IPTS-21442/skyrmion_4D.nxs',LoadHistory=False)

#######
# Open VSI!
#######

from paraview.simple import *
import vtk

source=GetActiveSource()

SaveData('/SNS/users/rwp/wand/IPTS-21442/skyrmion_4D.vts', source)
