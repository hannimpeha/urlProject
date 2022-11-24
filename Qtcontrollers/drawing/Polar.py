import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cbook as cbook


data_path = "../../output/#3-2/angular_intensity/output_angular_intensity_bottom.txt"
image = '/Users/hannahlee/PycharmProjects/penProject/resources/polar_plot.png'
data = np.genfromtxt(data_path, unpack=True)

theta = np.linspace(0,np.pi/2, 10)
r = np.cos(theta)
r_data = data
fig = plt.figure()
ax = fig.add_subplot(111, polar=True)
ax.set_thetamin(0)
ax.set_thetamax(90)

image_file = cbook.get_sample_data(image)
img = plt.imread(image_file)
ax.scatter(theta, r_data)
ax.scatter(theta, r)
# ax.imshow(img.transpose(1,0,1))
plt.gca().invert_xaxis()
plt.gca().invert_yaxis()
plt.show()


