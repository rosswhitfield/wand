# import mantid algorithms, numpy and matplotlib
from mantid.simpleapi import *
import matplotlib.pyplot as plt
import numpy as np

from mantid import config
config['Q.convention'] = "Inelastic"
#config['Q.convention'] = "Crystallography"

# data IPTS and run numbers ----------------------------------------------------
data_ipts = 24695
data_runs = [226469, 228269]

# vandium IPTS and run number --------------------------------------------------
van_ipts = 23858
van_run = 145309

# wavelength (angstrom) --------------------------------------------------------
wavelength = 1.486

# minimum and maximum values for Q sample --------------------------------------
min_values = [-7.5,-0.65,-4.4]
max_values = [6.8,0.65,7.5]

# detector grouping for loading data faster ------------------------------------
grouping = '2x2' # '2x2', 'None', '4x4'

# ---

# predict peak centering -------------------------------------------------------
ReflectionCondition = 'Primitive'
# 'Primitive'
# 'C-face centred', 'A-face centred', 'B-face centred',
# 'Body centred', 'All-face centred',
# 'Rhombohedrally centred, obverse',
# 'Rhombohedrally centred, reverse',
# 'Hexagonally centred, reverse'

# modulation vectors for indexing satellite peaks ------------------------------
ModVector1 = [0.05,0,0.5]
ModVector2 = [-0.05,0.05,0.5]
ModVector3 = [0,0.05,0.5]

# maximum order of satellite peaks ---------------------------------------------
MaxOrder = 1

# include cross terms for satellite peaks --------------------------------------
CrossTerms = False

# ellipsoidal peak integration envelope semi-axes ------------------------------
PeakRadius = [0.1,0.1,0.1]

# ellipsoidal peak integration background envelope semi-axes -------------------
BackgroundInnerRadius = [0.1,0.1,0.1]
BackgroundOuterRadius = [0.2,0.2,0.2]

# radius for determining peak center -------------------------------------------
PeakRadiuscen = 0.1

# tolerance for indexing main bragg peaks --------------------------------------
Tolerance = 0.05

# minimum integrated intensity -------------------------------------------------
FilterValue = 0

# ---

norm = LoadWANDSCD(IPTS=van_ipts,
                   RunNumbers=van_run,
                   Grouping=grouping)

data = LoadWANDSCD(IPTS=data_ipts,
                   RunNumbers=str(data_runs[0])+'-'+str(data_runs[1]),
                   Grouping=grouping)

#Q = ConvertWANDSCDtoQ(InputWorkspace='data',
#                      NormalisationWorkspace='norm',
#                      BinningDim1='-1,1,1')

count = Load(Filename='/HFIR/HB2C/IPTS-{}/nexus/HB2C_{}.nxs.h5'.format(van_ipts, van_run))

CalculateCountRate(Workspace=count, NormalizeTheRate=False)

s = count.getRun()

van_average_per_pixel = s.getProperty('block_count_rate').value.mean()*s.getProperty('duration').value*60/(3840*512)*eval(grouping.replace('x','*').replace('None','1'))

print('van average per pixel = {}'.format(int(van_average_per_pixel)))

van = mtd['norm']
data_temp = mtd['data']

UB = data.getExperimentInfo(0).sample().getOrientedLattice().getUB()

van.setErrorSquaredArray(van.getErrorSquaredArray()/van_average_per_pixel**2)
van.setSignalArray(van.getSignalArray()/van_average_per_pixel)

data_temp.setErrorSquaredArray((data_temp.getSignalArray()*data_temp.getSignalArray()/van.getSignalArray()/van.getSignalArray())*(data_temp.getErrorSquaredArray()/data_temp.getSignalArray()/data_temp.getSignalArray()+van.getErrorSquaredArray()/van.getSignalArray()/van.getSignalArray()))
data_temp.setSignalArray(data_temp.getSignalArray()/van.getSignalArray())

data_norm = ConvertHFIRSCDtoMDE(data_temp,
                                wavelength=wavelength,
                                MinValues=str(min_values[0])+','+str(min_values[1])+','+str(min_values[2]),
                                MaxValues=str(max_values[0])+','+str(max_values[1])+','+str(max_values[2]))

peaks = PredictPeaks(InputWorkspace=data_norm,
                     ReflectionCondition=ReflectionCondition,
                     CalculateGoniometerForCW=True,
                     Wavelength=wavelength,
                     FlipX=False,
                     InnerGoniometer=False,
                     MinAngle=-90,
                     MaxAngle=90)

peaks = CentroidPeaksMD(InputWorkspace=data_norm,
                        PeakRadius=PeakRadiuscen,
                        PeaksWorkspace=peaks)

IndexPeaks(PeaksWorkspace=peaks,
           Tolerance=Tolerance,
           RoundHKLs=False,
           ModVector1=ModVector1,
           ModVector2=ModVector2,
           ModVector3=ModVector3,
           MaxOrder=MaxOrder,
           SaveModulationInfo=True)

peaks = PredictSatellitePeaks(Peaks=peaks,
                              ModVector1=ModVector1,
                              ModVector2=ModVector2,
                              ModVector3=ModVector3,
                              WavelengthMin=wavelength-0.02,
                              WavelengthMax=wavelength+0.02,
                              IncludeIntegerHKL=False,
                              MaxOrder=MaxOrder)

peaks = IntegratePeaksMD(InputWorkspace=data_norm,
                         PeakRadius=PeakRadius,
                         BackgroundInnerRadius=BackgroundInnerRadius,
                         BackgroundOuterRadius=BackgroundOuterRadius,
                         PeaksWorkspace=peaks,
                         Ellipsoid=True,
                         IntegrateIfOnEdge=False)

peaks = FilterPeaks(InputWorkspace=peaks,
                    FilterVariable='Intensity',
                    FilterValue=FilterValue,
                    Operator='>')

for p in range(peaks.getNumberPeaks()):
    peak = peaks.getPeak(p)
    lorentz = np.abs(np.sin(peak.getScattering()*np.cos(peak.getAzimuthal())))
    peak.setIntensity(peak.getIntensity()*lorentz)


## now with the new stuff


peaks = PredictPeaks(InputWorkspace=data_norm,
                     ReflectionCondition=ReflectionCondition,
                     CalculateGoniometerForCW=True,
                     Wavelength=wavelength,
                     FlipX=False,
                     InnerGoniometer=False,
                     MinAngle=-90,
                     MaxAngle=90,
                     OutputType='LeanElasticPeak')

peaks = CentroidPeaksMD(InputWorkspace=data_norm,
                        PeakRadius=PeakRadiuscen,
                        PeaksWorkspace=peaks)

IndexPeaks(PeaksWorkspace=peaks,
           Tolerance=Tolerance,
           RoundHKLs=False,
           ModVector1=ModVector1,
           ModVector2=ModVector2,
           ModVector3=ModVector3,
           MaxOrder=MaxOrder,
           SaveModulationInfo=True)

peaks = PredictSatellitePeaks(Peaks=peaks,
                              ModVector1=ModVector1,
                              ModVector2=ModVector2,
                              ModVector3=ModVector3,
                              IncludeIntegerHKL=False,
                              MaxOrder=MaxOrder)

peaks = IntegratePeaksMD(InputWorkspace=data_norm,
                         PeakRadius=PeakRadius,
                         BackgroundInnerRadius=BackgroundInnerRadius,
                         BackgroundOuterRadius=BackgroundOuterRadius,
                         PeaksWorkspace=peaks,
                         Ellipsoid=True,
                         IntegrateIfOnEdge=False)

peaks = FilterPeaks(InputWorkspace=peaks,
                    FilterVariable='Intensity',
                    FilterValue=FilterValue,
                    Operator='>')
                    
                    

for p in range(peaks.getNumberPeaks()):
    peak = peaks.getPeak(p)
    lorentz = np.abs(np.sin(peak.getScattering()*np.cos(peak.getAzimuthal())))
    peak.setIntensity(peak.getIntensity()*lorentz)