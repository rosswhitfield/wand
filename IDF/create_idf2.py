import numpy as np
r=0.728*0.98
height=0.20
width=0.1872
xp=480
yp=512

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

for d in range(8):
    angle=7.5+(7-d)*15
    rad=np.deg2rad(angle)
    print('  <component type="panel" idstart="{}" idfillbyfirst="y" idstepbyrow="{}">'.format(d*xp*yp,yp)) #d*xp*yp,yp))
    print('    <location x="{}" y="0.0" z="{}" name="{}">'.format(np.sin(rad)*r,np.cos(rad)*r,"bank"+str(d+1)))
    print('      <rot axis-x="0" axis-y="1" axis-z="0" val="{}"/>'.format(angle+180))
    print("""    </location>
  </component>""")
    


print("""  <type name="panel" is="rectangular_detector" type="pixel"
    xpixels="480" xstart="-0.0936" xstep="+0.00039"
    ypixels="512" ystart="-0.1" ystep="+0.000390625" >
  <properties/>
  </type>

  <type is="detector" name="pixel">
  <cuboid id="pixel-shape">
    <left-front-bottom-point y="-0.0001953125" x="-0.0001953125" z="0.0"/>
    <left-front-top-point y="0.0001953125" x="-0.0001953125" z="0.0"/>
    <left-back-bottom-point y="-0.0001953125" x="-0.0001953125" z="-0.0001"/>
    <right-front-bottom-point y="-0.0001953125" x="0.0001953125" z="0.0"/>
  </cuboid>
  </type>

</instrument>
""")
