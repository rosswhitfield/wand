from mantid.simpleapi import *

p=WorkspaceFactory.createPeaks('LeanElasticPeaksWorkspace')


from mantid.dataobjects import PeaksWorkspace, LeanElasticPeaksWorkspace

print(isinstance(p, PeaksWorkspace))
print(isinstance(p, LeanElasticPeaksWorkspace))

p.addPeak(p.createPeakQSample(( 1, 0, 0)))
p.addPeak(p.createPeakQSample(( 0, 1, 0)))
p.addPeak(p.createPeakQSample(( 0, 0, 1)))
p.addPeak(p.createPeakQSample((-1, 0, 0)))
p.addPeak(p.createPeakQSample(( 0,-1, 0)))
p.addPeak(p.createPeakQSample(( 0, 0,-1)))

AnalysisDataService.addOrReplace('p',p)

SetUB(p)

p.addPeak(p.createPeakHKL((1,0,0)))
p.addPeak(p.createPeakHKL((0,-100,0)))
p.addPeak(p.createPeakHKL((-1,-1,-1)))

peak = p.createPeakHKL((1,1,1))
peak.setWavelength(1.5)
peak.setIntensity(100)
peak.setSigmaIntensity(10)
peak.setBinCount(50)
peak.setRunNumber(12345)
peak.setAbsorptionWeightedPathLength(1.1)
peak.setPeakNumber(99)
p.addPeak(peak)

print(p.row(0))


ws = CreateSampleWorkspace()
p2=CreatePeaksWorkspace(ws)
print(p2.row(0))
