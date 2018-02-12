from mantid.simpleapi import LoadEmptyInstrument, AddSampleLog, LoadInstrument
import resource

m0=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
LoadEmptyInstrument(Filename='/SNS/users/rwp/wand/IDF/test4/WAND_Definition_fixed.xml', OutputWorkspace='wand_fixed')
m1=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
LoadEmptyInstrument(Filename='/SNS/users/rwp/wand/IDF/test4/WAND_Definition_2952.xml', OutputWorkspace='wand_rect_fixed')
m2=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
LoadEmptyInstrument(Filename='/SNS/users/rwp/wand/IDF/test4/WAND_Definition.xml', OutputWorkspace='wand')
m3=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
AddSampleLog('wand', LogName='HB2C:Mot:s2.RBV', LogText='17.57', LogType='Number Series')
AddSampleLog('wand', LogName='HB2C:Mot:detz.RBV', LogText='7.05159', LogType='Number Series')
m4=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
LoadInstrument('wand',Filename='/SNS/users/rwp/wand/IDF/test4/WAND_Definition.xml', RewriteSpectraMap=False)
m5=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss

print(m1-m0)
print(m2-m1)
print(m3-m2)
print(m4-m3)
print(m5-m4)
print(m0)
print(m1)
print(m2)
print(m3)
print(m4)
print(m5)

for n in range(5):
    m10=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    LoadEmptyInstrument(Filename='/SNS/users/rwp/wand/IDF/test4/WAND_Definition_2952.xml', OutputWorkspace='wand{}'.format(n+300))
    m13=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    print("rect",m13-m10)
    print(m13)

for n in range(5):
    m10=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    LoadEmptyInstrument(Filename='/SNS/users/rwp/wand/IDF/test4/WAND_Definition_fixed.xml', OutputWorkspace='wand{}'.format(n+100))
    m13=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    print("fixed",m13-m10)
    print(m13)


for n in range(5):
    m10=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    LoadEmptyInstrument(Filename='/SNS/users/rwp/wand/IDF/test4/WAND_Definition.xml', OutputWorkspace='wand{}'.format(n+200))
    m13=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    print("wand",m13-m10)
    print(m13)


for n in range(5):
    m10=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    LoadEmptyInstrument(Filename='/SNS/users/rwp/wand/IDF/test4/WAND_Definition.xml', OutputWorkspace='wand{}'.format(n))
    m11=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    AddSampleLog('wand{}'.format(n), LogName='HB2C:Mot:s2.RBV', LogText='17.57', LogType='Number Series')
    AddSampleLog('wand{}'.format(n), LogName='HB2C:Mot:detz.RBV', LogText='7.05159', LogType='Number Series')
    m12=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    LoadInstrument('wand{}'.format(n),Filename='/SNS/users/rwp/wand/IDF/test4/WAND_Definition.xml', RewriteSpectraMap=False)
    m13=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    print(m11-m10)
    print(m12-m11)
    print(m13-m12)
    print(m13-m10)
    print(m13)
