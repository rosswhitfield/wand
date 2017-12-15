import numpy as np
r=0.728
height=0.20
xp=48
yp=51

xr = np.deg2rad(np.linspace(0,15,xp+1))
x = np.sin(xr)*r
z = np.cos(xr)*r
y = np.linspace(0,height,yp+1)


print("""<?xml version='1.0' encoding='ASCII'?>
<instrument xmlns="http://www.mantidproject.org/IDF/1.0"
            xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
            xsi:schemaLocation="http://www.mantidproject.org/IDF/1.0 Schema/IDFSchema.xsd"
            name="WAND"
            valid-from   ="1900-01-31 23:59:59"
            valid-to     ="2100-01-31 23:59:59"
            last-modified="2012-03-13 00:00:00">

  <defaults>
    <length unit="meter"/>
    <angle unit="degree"/>
    <reference-frame>
      <along-beam axis="z"/>
      <pointing-up axis="y"/>
      <handedness val="right"/>
    </reference-frame>
    <default-view axis-view="cylindrical_y"/>
  </defaults>

  <component type="monochromator">
    <location z="-3.289"/>
  </component>
  <type name="monochromator" is="Source" />

  <component type="sample-position">
    <location x="0.0" y="0.0" z="0.0"/>
  </component>
  <type name="sample-position" is="SamplePos" />
""")

print("""  <component name="DetectorBank" type="fan" idstart="0" idfillbyfirst="y" idstepbyrow="480" idstep="1">
            <location x="0.0" y="0.0" z="0.0"/>
          </component>
""")


print('  <type name="fan" is="StructuredDetector" xpixels="'+str(xp)+'" ypixels="'+str(yp)+'" type="pixel">')

for j in y:
    for i in xr:
        print('    <vertex x="'+str(np.sin(i)*r)+'" y="'+str(j)+'" z="'+str(np.cos(i)*r)+'" />')

print("""  </type>

  <type is="detector" name="pixel">
  </type>

</instrument>
""")
