import numpy as np
s2 = 3
k = 2*np.pi/1.488
phi = 0
theta = np.deg2rad(s2+120)
x = -k*np.sin(theta)*np.cos(0)
z = -k*(1-np.cos(theta))
print(x,z,np.linalg.norm((x,z)))

s1_0 = -180
s1_00 = -49.6

s1 = np.deg2rad(np.linspace(-180,-49.6,1305))

x_min = 0
x_max = 0
z_min = 0
z_max = 0
for angle in s1:
    rot = [[np.cos(angle), np.sin(angle)],[-np.sin(angle), np.cos(angle)]]
    xx, zz = np.dot(rot,[x,z])
    x_min = min(x_min, xx)
    x_max = max(x_max, xx)
    z_min = min(z_min, zz)
    z_max = max(z_max, zz)

print(x_min,x_max)
print(z_min,z_max)
