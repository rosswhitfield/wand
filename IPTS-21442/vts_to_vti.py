import glob
from paraview.simple import *

filenames = glob.glob('*.vts')
for filename in filenames:
    vts = XMLStructuredGridReader(FileName=[filename])
    Show(vts) # So it actually loads the data
    _, x, _, y, _, z = vts.GetDataInformation().DataInformation.GetExtent()
    print(x,y,z)
    resampleToImage = ResampleToImage(Input=vts)
    resampleToImage.SamplingDimensions = [x, y, z]
    SaveData(filename.replace('vts','vti'), proxy=resampleToImage)
