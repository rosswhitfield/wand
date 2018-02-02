from mantid.simpleapi import *

van = LoadNexus(Filename='/HFIR/HB2C/IPTS-7776/shared/autoreduce/HB2C_2933.nxs')

si = LoadNexus(Filename='/HFIR/HB2C/IPTS-7776/shared/autoreduce/HB2C_2929.nxs')

norm = si/van
norm=ReplaceSpecialValues(norm, NaNValue=0, InfinityValue=0)

van_2theta=ConvertSpectrumAxis(van, Target='Theta')
van_2theta=Transpose(van_2theta)

si_2theta=ConvertSpectrumAxis(si, Target='Theta')
si_2theta=Transpose(si_2theta)

# ResampleX
van_2theta2=ResampleX(van_2theta,XMin=20,XMax=135,NumberBins=2300)
si_2theta2=ResampleX(si_2theta,XMin=20,XMax=135,NumberBins=2300)
twotheta2=si_2theta2/van_2theta2

SaveFocusedXYE('twotheta2', 'Silicon.txt', SplitFiles=False)
