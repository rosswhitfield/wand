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
PeakRadius = [0.05,0.05,0.1]

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
"""
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

s = count.getRun()data_norm = LoadMD('/home/rwp/WAND_satellite_test.nxs')


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

SaveMD(data_norm,Filename='/SNS/users/rwp/WAND_satellite_test.nxs')
"""
data_norm = LoadMD('/home/rwp/WAND_satellite_test.nxs')

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
                         #BackgroundInnerRadius=BackgroundInnerRadius,
                         #BackgroundOuterRadius=BackgroundOuterRadius,
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
ModVector1 = [0.05,0.05,0]
ModVector2 = [-0.1,0.05,0]
ModVector3 = [-0.05,0.1,0]
PeakRadius = [0.05,0.05,0.1]

peaks2 = PredictPeaks(InputWorkspace=data_norm,
                     ReflectionCondition=ReflectionCondition,
                     CalculateGoniometerForCW=True,
                     Wavelength=wavelength,
                     FlipX=False,
                     InnerGoniometer=False,
                     MinAngle=-90,
                     MaxAngle=90,
                     OutputType='LeanElasticPeak')

peaks2 = CentroidPeaksMD(InputWorkspace=data_norm,
                        PeakRadius=PeakRadiuscen,
                        PeaksWorkspace=peaks2)

IndexPeaks(PeaksWorkspace=peaks2,
           Tolerance=Tolerance,
           RoundHKLs=False,
           ModVector1=ModVector1,
           ModVector2=ModVector2,
           ModVector3=ModVector3,
           MaxOrder=MaxOrder,
           SaveModulationInfo=True)

sate_peaks2 = PredictSatellitePeaks(Peaks=peaks2,
                              ModVector1=ModVector1,
                              ModVector2=ModVector2,
                              ModVector3=ModVector3,
                              IncludeIntegerHKL=False,
                              MaxOrder=MaxOrder)
HFIRCalculateGoniometer(sate_peaks2,wavelength)
sate_peaks2 = IntegratePeaksMD(InputWorkspace=data_norm,
                         PeakRadius=PeakRadius,
                         PeaksWorkspace=sate_peaks2,
                         Ellipsoid=True)

for p in range(peaks2.getNumberPeaks()):
    peak2 = peaks2.getPeak(p)
    lorentz = np.abs(np.sin(peak2.getScattering()*np.cos(peak2.getAzimuthal())))
    peak2.setIntensity(peak2.getIntensity()*lorentz)

clone=CloneMDWorkspace(data_norm)
HHL = ConvertQtoHKLMDHisto(clone,Uproj='1,1,0',Vproj='1,-1,0',Extents='-5.01,5.01,-3.51,3.51,-0.21,0.81',Bins='501,501,51')
HHL.getExperimentInfo(0).run().addProperty('W_MATRIX',[1,1,0,1,-1,0,0,0,1], True)
HKL = ConvertQtoHKLMDHisto(clone,Extents='-5.01,5.01,-5.01,5.01,-0.21,0.81',Bins='501,501,51')
clone.delete()


# slightly different approach
ModVector1 = [0.05,0.05,0]
ModVector2 = [-0.1,0.05,0]
ModVector3 = [-0.05,0.1,0]
PeakRadius = [0.05,0.05,0.1]

peaks3 = PredictPeaks(InputWorkspace=data_norm,
                      ReflectionCondition=ReflectionCondition,
                      Wavelength=wavelength,
                      OutputType='LeanElasticPeak',
                      CalculateWavelength=False,
                      MinDSpacing=0.8)

peaks3 = CentroidPeaksMD(InputWorkspace=data_norm,
                         PeakRadius=PeakRadiuscen,
                         PeaksWorkspace=peaks3)

IndexPeaks(PeaksWorkspace=peaks3,
           Tolerance=Tolerance,
           RoundHKLs=False,
           ModVector1=ModVector1,
           ModVector2=ModVector2,
           ModVector3=ModVector3,
           MaxOrder=MaxOrder,
           SaveModulationInfo=True)

sate_peaks3 = PredictSatellitePeaks(Peaks=peaks3,
                                    ModVector1=ModVector1,
                                    ModVector2=ModVector2,
                                    ModVector3=ModVector3,
                                    IncludeIntegerHKL=False,
                                    MaxOrder=MaxOrder)

HFIRCalculateGoniometer(sate_peaks3, wavelength)

sate_peaks3 = IntegratePeaksMD(InputWorkspace=data_norm,
                               PeakRadius=PeakRadius,
                               PeaksWorkspace=sate_peaks3,
                               Ellipsoid=True)

sate_peaks3 = FilterPeaks(InputWorkspace=sate_peaks3,
                          FilterVariable='Intensity',
                          FilterValue=FilterValue,
                          Operator='>')

for p in range(peaks3.getNumberPeaks()):
    peak3 = peaks3.getPeak(p)
    lorentz = np.abs(np.sin(peak3.getScattering()*np.cos(peak3.getAzimuthal())))
    peak3.setIntensity(peak3.getIntensity()*lorentz)

# doing this to avoid bug in sliceviewer
clone=CloneMDWorkspace(data_norm)
#HHL = ConvertQtoHKLMDHisto(clone,Uproj='1,1,0',Vproj='1,-1,0',Extents='-5.01,5.01,-3.51,3.51,-0.21,0.81',Bins='501,501,51')
#HHL.getExperimentInfo(0).run().addProperty('W_MATRIX',[1,1,0,1,-1,0,0,0,1], True)
HKL = ConvertQtoHKLMDHisto(clone,Extents='-5.01,5.01,-5.01,5.01,-0.21,0.81',Bins='501,501,51')
clone.delete()



#####

ModVector1 = [0.05,0.05,0]
ModVector2 = [-0.1,0.05,0]
ModVector3 = [-0.05,0.1,0]
PeakRadius = [0.05,0.05,0.1]

peaks = PredictPeaks(InputWorkspace=data_norm,
                     ReflectionCondition=ReflectionCondition,
                     Wavelength=wavelength,
                     OutputType='LeanElasticPeak',
                     CalculateWavelength=False,
                     MinDSpacing=0.8)

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

HFIRCalculateGoniometer(peaks, wavelength)

peaks = IntegratePeaksMD(InputWorkspace=data_norm,
                         PeakRadius=PeakRadius,
                         PeaksWorkspace=peaks,
                         Ellipsoid=True)

peaks = FilterPeaks(InputWorkspace=peaks,
                    FilterVariable='Intensity',
                    FilterValue=FilterValue,
                    Operator='>')

for p in range(peaks.getNumberPeaks()):
    peak = peaks.getPeak(p)
    lorentz = np.abs(np.sin(peak.getScattering()*np.cos(peak.getAzimuthal())))
    peak.setIntensity(peak.getIntensity()*lorentz)

# doing this to avoid bug in sliceviewer SCD #275
clone=CloneMDWorkspace(data_norm)
HKL = ConvertQtoHKLMDHisto(clone,Extents='-5.01,5.01,-5.01,5.01,-0.21,0.81',Bins='501,501,51')
clone.delete()
