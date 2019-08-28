from Tools import bgsim

import os
import libtiff
import numpy as np

dataset = '/home/shuangbo/mount1/paraffin/20190424/paraffin_0.24e-0000.tif'
path, dataname = os.path.split(dataset)
dataname = os.path.splitext(dataname)[0][:-4]

imglist = [x for x in os.listdir(path) if dataname in x \
           and os.path.splitext(x)[-1] == ".tif"]
imglist.sort(key=lambda d: int(os.path.splitext(d)[0][-4:]))

center = [2079.55, 2012.77]
azum = [2.369, 3.71]

for im in imglist:
    filename = os.path.splitext(im)[0]
    outname = filename + '_bgsub.tif'
    infile = os.path.join(path, im)
    outfile = os.path.join(path, outname)
    tif = libtiff.TIFF.open(infile)
    data = tif.read_image()
    data = np.flipud(data)
    data = data.astype(np.float32)
    bg = bgsim.subtract(data, center, azum)
    datasbg = data - bg
    datasbg = np.flipud(datasbg)
    datasbg = datasbg.astype(np.int16)
    wtif = libtiff.TIFF.open(outfile, mode='w')
    wtif.write_image(datasbg)
    wtif.flush()
    print("image ", im, " is done!")