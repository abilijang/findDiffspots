import os
from itertools import groupby
import numpy as np
import libtiff
import pdb

coords = np.loadtxt("/cs2/shuangbo/tmp/coords.txt")
center = [2078.6, 2005.7]
dsts = list(map(lambda x:np.linalg.norm(x - center), np.array(coords)))
path = '/home/shuangbo/mount1/paraffin/20190424/paraffin_0.48e'
path, dataname = os.path.split(path)

# pdb.set_trace()
interval = []
for k, g in groupby(sorted(dsts), key=lambda x: x//20):
	interval.append([k*20, (k+1)*20-1])

div = []
for iv in interval:
	tmp = []
	for i, dst in enumerate(dsts):
		if dst < iv[1] and dst >= iv[0]:
			tmp.append(i)
	div.append(tmp)

# for i in range(len(div)):
# 	idiv = div[i]
# 	intens = 0
# 	for index in idiv:
# 		coord = coords[index]
# 		cox = coord[0]
# 		coy = coord[1]
# 		crop = data[int(coy-48):int(coy+48), int(cox-48):int(cox+48)]
# 		intens = intens + np.sum(crop)
# 	intens = intens / len(idiv)

imglist = [ x for x in os.listdir(path) if dataname in x \
						and os.path.splitext(x)[-1] == ".tif" ]
imglist.sort(key=lambda d:int(os.path.splitext(d)[0][-4:])) 

intens = np.zeros([len(imglist), len(div)])
for j in range(len(imglist)):
	print(imglist[j]," done!")
	image = os.path.join(path, imglist[j])
	tif = libtiff.TIFF.open(image)
	data = tif.read_image()
	data = np.flipud(data)
	for i in range(len(div)):
		# pdb.set_trace()
		idiv = div[i]
		inten = 0
		for index in idiv:
			coord = coords[index]
			cox = coord[0]
			coy = coord[1]
			crop = data[int(coy-48):int(coy+48), int(cox-48):int(cox+48)]
			inten = inten + np.sum(crop)
		inten = inten / len(idiv)
		# pdb.set_trace()
		intens[j, i] = inten

np.savetxt("/cs2/shuangbo/tmp/intens.txt", intens)

