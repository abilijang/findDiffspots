# -*- coding: utf-8 -*-

from PyQt5.QtCore import QThread, pyqtSignal

import os
import libtiff
import numpy as np
from numpy import *
from itertools import groupby
import pdb

class Thread(QThread):
    signal = pyqtSignal(ndarray, ndarray, int, int)
    finish = pyqtSignal()

    def __init__(self, dataset, centerpts, parent=None):
        super(Thread, self).__init__(parent)
        self.dataset = dataset
        self.centerpts = centerpts
        self.path, dataname = os.path.split(self.dataset)
        dataname = os.path.splitext(dataname)[0][:-4]

        self.imglist = [x for x in os.listdir(self.path) if dataname in x \
                   and os.path.splitext(x)[-1] == ".tif"]
        self.imglist.sort(key=lambda d: int(os.path.splitext(d)[0][-4:]))

        self.coords = np.loadtxt("/cs2/shuangbo/tmp/coords.txt")
        dsts = list(map(lambda x: np.linalg.norm(x - self.centerpts), np.array(self.coords)))

        interval = []
        for k, g in groupby(sorted(dsts), key=lambda x: x // 20):
            interval.append([k * 20, (k + 1) * 20 - 1])
        self.div = []
        for iv in interval:
            tmp = []
            for i, dst in enumerate(dsts):
                if dst < iv[1] and dst >= iv[0]:
                    tmp.append(i)
            self.div.append(tmp)
        # pdb.set_trace()
        self.div = [ x for x in self.div if x != [] ]
        self.intens = np.zeros([len(self.imglist), len(self.div)])

    def run(self):
        for j in range(len(self.imglist)):
            image = os.path.join(self.path, self.imglist[j])
            tif = libtiff.TIFF.open(image)
            data = tif.read_image()
            dataup = np.flipud(data)
            coldel = []
            for i in range(len(self.div)):
                if len(self.div[i]) != 0:
                # pdb.set_trace()
                    idiv = self.div[i]
                    inten = 0
                    for index in idiv:
                        coord = self.coords[index]
                        cox = coord[0]
                        coy = coord[1]
                        crop = dataup[int(coy - 48):int(coy + 48), int(cox - 48):int(cox + 48)]
                        inten = inten + np.sum(crop)
                    inten = inten / len(idiv)
                    self.intens[j, i] = inten
                else:
                    pass
            self.signal.emit(data, self.intens[:(j + 1), :], len(self.imglist), len(self.div))
        self.finish.emit()