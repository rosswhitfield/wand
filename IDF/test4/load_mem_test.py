from mantid.simpleapi import LoadEmptyInstrument, AddSampleLog, LoadInstrument
import resource

m0=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
LoadEmptyInstrument(Filename='/SNS/users/rwp/wand/IDF/test4/WAND_Definition_fixed.xml', OutputWorkspace='wand_fixed')
m1=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
LoadEmptyInstrument(Filename='/SNS/users/rwp/wand/IDF/test4/WAND_Definition_2952.xml', OutputWorkspace='wand_rect_fixed')
m2=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
LoadEmptyInstrument(Filename='/SNS/users/rwp/wand/IDF/test4/WAND_Definition.xml', OutputWorkspace='wand')
m3=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
AddSampleLog('wand', LogName='HB2C:Mot:s2', LogText='17.57', LogType='Number Series')
AddSampleLog('wand', LogName='HB2C:Mot:detz', LogText='7.05159', LogType='Number Series')
LoadInstrument('wand',Filename='/SNS/users/rwp/wand/IDF/test4/WAND_Definition.xml', RewriteSpectraMap=False)
m4=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss

print(m1-m0)
print(m2-m1)
print(m3-m2)
print(m4-m3)
