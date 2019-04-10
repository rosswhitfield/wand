Uproj = [1, 0, 0]
Vproj = [0, 1, 0]
Wproj = [0, 0, 1]

wavelenght = 1.488

ws=mtd['ws']


################################################################################

s1 = ws.getExperimentInfo(0).run().getProperty('s1').value
twotheta = ws.getExperimentInfo(0).run().getProperty('twotheta').value
azimuthal = ws.getExperimentInfo(0).run().getProperty('azimuthal').value
