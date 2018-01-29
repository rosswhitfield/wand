from mantid.simpleapi import *

van = LoadNexus(Filename='/HFIR/HB2C/IPTS-7776/shared/autoreduce/HB2C_2933.nxs')

si = LoadNexus(Filename='/HFIR/HB2C/IPTS-7776/shared/autoreduce/HB2C_2929.nxs')

norm = si/van
norm=ReplaceSpecialValues(norm, NaNValue=0, InfinityValue=0)

norm_2theta=ConvertSpectrumAxis(norm, Target='Theta')
norm_2theta=Transpose(norm_2theta)

norm_d=ConvertSpectrumAxis(norm, Target='ElasticDSpacing', EFixed='36.9462') # Lambda = 1.488A
norm_d=Transpose(norm_d)

# Do convertion first

van_2theta=ConvertSpectrumAxis(van, Target='Theta')
van_2theta=Transpose(van_2theta)

van_d=ConvertSpectrumAxis(van, Target='ElasticDSpacing', EFixed='36.9462') # Lambda = 1.488A
van_d=Transpose(van_d)

van_q=ConvertSpectrumAxis(van, Target='ElasticQ', EFixed='36.9462') # Lambda = 1.488A
van_q=Transpose(van_q)

si_2theta=ConvertSpectrumAxis(si, Target='Theta')
si_2theta=Transpose(si_2theta)

si_d=ConvertSpectrumAxis(si, Target='ElasticDSpacing', EFixed='36.9462') # Lambda = 1.488A
si_d=Transpose(si_d)

si_q=ConvertSpectrumAxis(si, Target='ElasticQ', EFixed='36.9462') # Lambda = 1.488A
si_q=Transpose(si_q)

#d=si_d/van_d
#twotheta=si_2theta/van_2theta
#q=si_q/van_q

# ResampleX
van_2theta2=ResampleX(van_2theta,XMin=20,XMax=135,NumberBins=2300)
si_2theta2=ResampleX(si_2theta,XMin=20,XMax=135,NumberBins=2300)
twotheta2=si_2theta2/van_2theta2

van_d2=ResampleX(van_d,XMin=0.8,XMax=4,NumberBins=3200)
si_d2=ResampleX(si_d,XMin=0.8,XMax=4,NumberBins=3200)
d2=si_d2/van_d2

van_q2=ResampleX(van_q,XMin=1,XMax=10,NumberBins=1800)
si_q2=ResampleX(si_q,XMin=1,XMax=10,NumberBins=1800)
q2=si_q2/van_q2



cu = LoadNexus(Filename='/HFIR/HB2C/IPTS-7776/shared/autoreduce/HB2C_2930.nxs')
cu_norm = cu/van
cu_norm=ReplaceSpecialValues(cu_norm, NaNValue=0, InfinityValue=0)

cu_2theta=ConvertSpectrumAxis(cu, Target='Theta')
cu_2theta=Transpose(cu_2theta)
cu_2theta2=ResampleX(cu_2theta,XMin=20,XMax=135,NumberBins=2300)
cu_twotheta2=cu_2theta2/van_2theta2


NCFA = LoadNexus(Filename='/HFIR/HB2C/IPTS-7776/shared/autoreduce/HB2C_2931.nxs')
NCFA_norm = NCFA/van
NCFA_norm=ReplaceSpecialValues(NCFA_norm, NaNValue=0, InfinityValue=0)

NCFA_2theta=ConvertSpectrumAxis(NCFA, Target='Theta')
NCFA_2theta=Transpose(NCFA_2theta)
NCFA_2theta2=ResampleX(NCFA_2theta,XMin=18,XMax=135,NumberBins=2540)
van_2theta2=ResampleX(van_2theta,XMin=18,XMax=135,NumberBins=2540)
NCFA_twotheta2=NCFA_2theta2/van_2theta2
