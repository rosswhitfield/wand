import numpy as np
import vtk
from vtk.util.numpy_support import numpy_to_vtk, get_vtk_array_type
from mantid.simpleapi import LoadMD

ws = LoadMD('/SNS/users/rwp/wand/IPTS-21442/skyrmion_4D.nxs')

signal=ws.getSignalArray()

vtkArray = numpy_to_vtk(num_array=signal.flatten('F'), deep=True,
                        array_type=get_vtk_array_type(signal.dtype))

origin = np.array([ws.getDimension(d).getMinimum() for d in range(4)])
spacing = np.array([ws.getDimension(d).getBinWidth() for d in range(4)])

imageData = vtk.vtkImageData()
imageData.SetOrigin(origin)
imageData.SetSpacing(spacing)
imageData.SetDimensions(signal.shape)
imageData.GetPointData().SetScalars(vtkArray)
writer = vtk.vtkXMLImageDataWriter()
writer.SetFileName('/SNS/users/rwp/wand/IPTS-21442/skyrmion_4D.vti')
writer.SetInputData(imageData)
writer.Write()
