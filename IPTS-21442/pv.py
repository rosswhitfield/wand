#### import the simple module from the paraview
from paraview.simple import *

# create a new 'Image Reader'
ringraw = ImageReader(FilePrefix='/SNS/users/rwp/wand/IPTS-21442/ring.raw')

ringraw.DataScalarType = 'double'
ringraw.DataByteOrder = 'LittleEndian'
ringraw.DataExtent = [0, 40, 0, 40, 0, 24]
ringraw.DataSpacing = [1.0, 1.0, 2.0]
ringraw.DataOrigin = [-20.0, -20.0, -24.0]

# get active view
renderView1 = GetActiveViewOrCreate('RenderView')

# uncomment following to set a specific view size
# renderView1.ViewSize = [1106, 1633]

# show data in view
ringrawDisplay = Show(ringraw, renderView1)

# reset view to fit data
# renderView1.ResetCamera()

# change representation type
ringrawDisplay.SetRepresentationType('Volume')

# set scalar coloring
ColorBy(ringrawDisplay, ('POINTS', 'ImageFile'))

# get color transfer function/color map for 'ImageFile'
imageFileLUT = GetColorTransferFunction('ImageFile')

# get opacity transfer function/opacity map for 'ImageFile'
imageFilePWF = GetOpacityTransferFunction('ImageFile')

# show color bar/color legend
# ringrawDisplay.SetScalarBarVisibility(renderView1, True)

# Rescale transfer function
imageFileLUT.RescaleTransferFunction(0.0, 10.0)

# Rescale transfer function
imageFilePWF.RescaleTransferFunction(4.0, 10.0)

# Apply a preset using its name. Note this may not work as expected when presets have duplicate names.
imageFileLUT.ApplyPreset('Inferno (matplotlib)', True)

renderView1.CameraViewUp = [0,0,1]
renderView1.CameraPosition = [100, 100, -50]

scene = GetAnimationScene()
scene.NumberOfFrames = 200

cameraAnimationCue1 = GetCameraTrack(view=renderView1)

import vtk
p=vtk.vtkSMUtilities.CreateOrbit((0,0,0), (0,0,1), 7, (80,80,-50))
keyFrame0 = CameraKeyFrame()
keyFrame0.ViewUp = [0.0, 0.0, 1.0]
keyFrame0.PositionPathPoints = sum([list(p.GetPoint(n)) for n in range(p.GetNumberOfPoints())], [])
keyFrame0.ClosedPositionPath = 1
keyFrame1 = CameraKeyFrame()
keyFrame1.KeyTime = 1.0
keyFrame1.ViewUp = [0.0, 0.0, 1.0]

cameraAnimationCue1.Mode = 'Path-based'
cameraAnimationCue1.KeyFrames = [keyFrame0, keyFrame1]

SaveAnimation('/tmp/Skyrmion.png', renderView1, ImageResolution=[1280, 720])

# ffmpeg -i /tmp/Skyrmion.%04d.png Skyrmion.mp4

scene.NumberOfFrames = 100
SaveAnimation('/tmp/Skyrmion.png', renderView1, ImageResolution=[400, 400])

# ffmpeg -i /tmp/Skyrmion.%04d.png Skyrmion.gif

#### uncomment the following to render all views
# RenderAllViews()
# alternatively, if you want to write images, you can use SaveScreenshot(...).
