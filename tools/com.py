import numpy as np
import heapq
from itertools import combinations

import pdb

def dist(x):
	return np.sqrt((x[1][1]-x[0][1])**2+(x[1][0]-x[0][0])**2)

def com(data, coord):
	# pdb.set_trace()
	cox = coord[0]
	coy = coord[1]
	coy = -coy + 4096

	kernel = [144, 96, 48]
	for i in range(7):
		# size = int(kernel[i])
		# half = size / 2
		# tm = np.arange(size) + 1
		# tx = np.tile(tm, (size, 1))
		# ty = np.transpose(tx)
		# kernel = np.dstack((tx, ty))
		# crop = data[int(coy-half):int(coy+half), int(cox-half):int(cox+half)]
		# com1x = np.sum(kernel[:,:,0] * crop) / np.sum(crop)
		# com1y = np.sum(kernel[:,:,1] * crop) / np.sum(crop)
		# cox = cox - half + com1x
		# coy = coy - half + com1y
		if i == 0:
			tm = np.arange(192) + 1
			tx = np.tile(tm, (192, 1))
			ty = np.transpose(tx)
			kernel = np.dstack((tx, ty))
			crop = data[int(coy-96):int(coy+96), int(cox-96):int(cox+96)]
			com1x = np.sum(kernel[:,:,0] * crop) / np.sum(crop)
			com1y = np.sum(kernel[:,:,1] * crop) / np.sum(crop)
			cox = cox - 96 + com1x
			coy = coy - 96 + com1y
		elif i == 1:
			tm = np.arange(128) + 1
			tx = np.tile(tm, (128, 1))
			ty = np.transpose(tx)
			kernel = np.dstack((tx, ty))
			crop = data[int(coy-64):int(coy+64), int(cox-64):int(cox+64)]
			com1x = np.sum(kernel[:,:,0] * crop) / np.sum(crop)
			com1y = np.sum(kernel[:,:,1] * crop) / np.sum(crop)
			cox = cox - 64 + com1x
			coy = coy - 64 + com1y
		else:
			tm = np.arange(64) + 1
			tx = np.tile(tm, (64, 1))
			ty = np.transpose(tx)
			kernel = np.dstack((tx, ty))
			crop = data[int(coy-32):int(coy+32), int(cox-32):int(cox+32)]
			com1x = np.sum(kernel[:,:,0] * crop) / np.sum(crop)
			com1y = np.sum(kernel[:,:,1] * crop) / np.sum(crop)
			cox = cox - 32 + com1x
			coy = coy - 32 + com1y

	return [cox, coy]

def center(data, coords):
	# pdb.set_trace()
	co1 = coords[0]
	co2 = coords[1]
	co3 = coords[2]
	co4 = coords[3]
	co5 = coords[4]
	co6 = coords[5]
	rco1 = com(data, co1)
	rco2 = com(data, co2)
	rco3 = com(data, co3)
	rco4 = com(data, co4)
	rco5 = com(data, co5)
	rco6 = com(data, co6)

	tmp = [rco1, rco2, rco3, rco4, rco5, rco6]
	pair = np.array(list(combinations(tmp, 2)))

	# for i, p in enumerate(pair):
	# 	dist =  np.sqrt((p[1][1]-p[0][1])**2+(p[1][0]-p[0][0])**2)
	# 	lst.append([i, dist])

	# lst = np.array(lst)
	# lst = lst[lst[:,1].argsort()]
	# index = lst[:,0][-3:]

	dst = list(map(dist, pair))
	index = list(map(dst.index, heapq.nlargest(3, dst)))
	# pdb.set_trace()
	mpair1 = pair[int(index[0])]
	mpair2 = pair[int(index[1])]
	mpair3 = pair[int(index[2])]
	center1 = (mpair1[1] + mpair1[0]) / 2
	center2 = (mpair2[1] + mpair2[0]) / 2
	center3 = (mpair3[1] + mpair3[0]) / 2

	centerx = (center1[0] + center2[0] + center3[0]) / 3
	centery = (center1[1] + center2[1] + center3[1]) / 3

	return [centerx, centery]

if __name__ == '__main__':
	center()
