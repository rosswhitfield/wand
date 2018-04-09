import numpy as np

data = np.load('IPTS_20367_data.npy')
phi = np.load('IPTS_20367_phi.npy')

output = np.zeros((501,51,501))

s2 = 2.0
detz = 0.0
k = 2*np.pi/1.488

theta = np.linspace(0,120,8*380)+s2
x = np.sin(theta)*0.72
z = np.sin(theta)*0.72
y = np.linspace(-10,10,512)+detz
