from colour.plotting import *
from colour.colorimetry import *
import numpy as np

data_path = "output/#3-2/CIE/output_CIE_bottom.txt"
data = np.loadtxt(data_path, unpack=True)
index = np.array(range(0,100,10))
#labels = ('x', 'y', 'z')
dic = {k: v for k, v in (zip(index, np.transpose(data)))}

x_dic = {k:v[0] for k,v in dic.items()}
y_dic = {k:v[1] for k,v in dic.items()}
z_dic = {k:v[2] for k,v in dic.items()}

ds = [x_dic, y_dic, z_dic]
d = {}
for k in x_dic.keys():
  d[k] = tuple(d[k] for d in ds)

sds = MultiSpectralDistributions(d)
plot_chromaticity_diagram_CIE1931()

#plot_chromaticity_diagram_CIE1976UCS(sds)

#plot_sds_in_chromaticity_diagram_CIE1960UCS(sds)
#plot_chromaticity_diagram_CIE1960UCS(sds)