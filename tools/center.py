#!/home/shuangbo/EMAN2/bin/python

import numpy as np
from EMAN2 import *
from itertools import combinations
import pdb

img = EMData()
img.read_image('/home/shuangbo/mount1/paraffin/20190424/paraffin_0.48e-0001.tif')
data = EMNumPy.em2numpy(img)
# co1x = 1883 
# co1y = 1516
# co2x = 2530 
# co2y = 1707 
# co3x = 2721 
# co3y = 2291
# co4x = 2254 
# co4y = 2684
# co5x = 1617 
# co5y = 2461
# co6x = 1437 
# co6y = 1877

co1x = 2169
co2x = 1702
co3x = 1235
co4x = 758
co5x = 991
co6x = 1161
co1y = 583
co2y = 965
co3y = 1368
co4y = 1729
co5y = 2249
co6y = 2832
co1y = -co1y + 4096
co2y = -co2y + 4096
co3y = -co3y + 4096
co4y = -co4y + 4096
co5y = -co5y + 4096
co6y = -co6y + 4096
pdb.set_trace()
tm = np.arange(96) + 1
tx = np.tile(tm, (96, 1))
ty = np.transpose(tx)
kernel = np.dstack((tx, ty))

for i in range(2):
	c1 = np.copy(data[int(co1y-48):int(co1y+48), int(co1x-48):int(co1x+48)])
	c2 = np.copy(data[int(co2y-48):int(co2y+48), int(co2x-48):int(co2x+48)])
	c3 = np.copy(data[int(co3y-48):int(co3y+48), int(co3x-48):int(co3x+48)])
	c4 = np.copy(data[int(co4y-48):int(co4y+48), int(co4x-48):int(co4x+48)])
	c5 = np.copy(data[int(co5y-48):int(co5y+48), int(co5x-48):int(co5x+48)])
	c6 = np.copy(data[int(co6y-48):int(co6y+48), int(co6x-48):int(co6x+48)])
	com1x = np.sum(kernel[:,:,0] * c1) / np.sum(c1)
	com2x = np.sum(kernel[:,:,0] * c2) / np.sum(c2)
	com3x = np.sum(kernel[:,:,0] * c3) / np.sum(c3)
	com4x = np.sum(kernel[:,:,0] * c4) / np.sum(c4)
	com5x = np.sum(kernel[:,:,0] * c5) / np.sum(c5)
	com6x = np.sum(kernel[:,:,0] * c6) / np.sum(c6)

	com1y = np.sum(kernel[:,:,1] * c1) / np.sum(c1)
	com2y = np.sum(kernel[:,:,1] * c2) / np.sum(c2)
	com3y = np.sum(kernel[:,:,1] * c3) / np.sum(c3)
	com4y = np.sum(kernel[:,:,1] * c4) / np.sum(c4)
	com5y = np.sum(kernel[:,:,1] * c5) / np.sum(c5)
	com6y = np.sum(kernel[:,:,1] * c6) / np.sum(c6)

	co1x = co1x - 48 + com1x
	co2x = co2x - 48 + com2x
	co3x = co3x - 48 + com3x
	co4x = co4x - 48 + com4x
	co5x = co5x - 48 + com5x
	co6x = co6x - 48 + com6x

	co1y = co1y - 48 + com1y
	co2y = co2y - 48 + com2y
	co3y = co3y - 48 + com3y
	co4y = co4y - 48 + com4y
	co5y = co5y - 48 + com5y
	co6y = co6y - 48 + com6y

coord = [[co1x, co1y],
		 [co2x, co2y],
		 [co3x, co3y],
		 [co4x, co4y],
		 [co5x, co5y],
		 [co6x, co6y],]

# pair = list(combinations(coord, 2))

# dist = []
# lst = []
# pair = np.array(pair)

# for i, p in enumerate(pair):
# 	dist =  np.sqrt((p[1][1]-p[0][1])**2+(p[1][0]-p[0][0])**2)
# 	lst.append([i, dist])

# lst = np.array(lst)
# lst = lst[lst[:,1].argsort()]
# index = lst[:,0][-3:]

# mpair1 = pair[int(index[0])]
# mpair2 = pair[int(index[1])]
# mpair3 = pair[int(index[2])]

# center1 = (mpair1[1] + mpair1[0]) / 2
# center2 = (mpair2[1] + mpair2[0]) / 2
# center3 = (mpair3[1] + mpair3[0]) / 2

# center = (center1 + center2 + center3) / 3

coord = np.array(coord)
np.savetxt('/cs2/shuangbo/lysozyme_tmp/data1/sum/coord.txt', coord)