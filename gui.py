# -*- coding: utf-8 -*-

import os
import sys
import libtiff
import numpy as np
from scipy import stats
import matplotlib
matplotlib.use('Qt5Agg')
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from matplotlib.patches import Circle
import matplotlib.pyplot as plt

from PyQt5 import QtWidgets, QtCore
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QScrollBar, QMainWindow, QTreeWidgetItem, QFileDialog, QHeaderView, QTreeWidget
from ui.mainwindow import Ui_MainWindow

from tools import com
# Tools.com
import Thread

class MainWindow(QMainWindow, Ui_MainWindow):
    """
    Class documentation goes here.
    """
    datalist  = []
    framelist = []
    coords = []
    coords_tmp = []

    def __init__(self, parent=None):
        """
        Constructor
        @param parent reference to the parent widget
        @type QWidget
        """
        super(MainWindow, self).__init__(parent)
        self.setupUi(self)

        self.treeWidget.setColumnWidth(0, 240)
        # self.treeWidget.resizeColumnToContents(0)
        # self.treeWidget.resizeColumnToContents(0)
        # self.treeWidget.resizeColumnToContents(1)
        # self.treeWidget.header().setSectionResizeMode(0, QHeaderView.Stretch)
        # self.treeWidget.header().setSectionResizeMode(1, QHeaderView.Stretch)

        self.figure = Figure(figsize=(384,384), dpi=100)
        self.figure.subplots_adjust(top=1, bottom=0, left=0, \
                                    right=1, hspace=0, wspace=0)

        self.canvas = FigureCanvas(self.figure)
        self.horizontalLayout_2.addWidget(self.canvas)
        self.figure1 = Figure(figsize=(384,384), dpi=100)
        self.figure1.subplots_adjust(top=1, bottom=0, left=0, \
                                    right=1, hspace=0, wspace=0)

        self.canvas1 = FigureCanvas(self.figure1)
        self.horizontalLayout_3.addWidget(self.canvas1)

        self.horizontalScrollBar.valueChanged.connect(self.updatedisplay)
        self.horizontalScrollBar_2.valueChanged.connect(self.updatedisplay)

        self.checkBox.stateChanged.connect(self.sectordiv)

    def sectordiv(self):
        cpx = self.centerpts[0]
        cpy = 4096 - self.centerpts[1]
        line, = self.axes.plot([cpx], [cpy])
        linebuilder = LineBuilder(line)

    def updatedisplay(self, value):
        tmin = self.horizontalScrollBar.value()
        tmax = self.horizontalScrollBar_2.value()
        # self.axes.clear()
        self.axes.imshow(self.data, cmap='Greys_r', vmin=tmin, vmax=tmax)
        self.axes.set_xticks([])
        self.axes.set_yticks([])
        self.axes.set_yticklabels([])
        self.axes.set_xticklabels([])
        self.canvas.draw()
        self.canvas.flush_events()

    def create_datasets(self, path, dataname):
        data = QTreeWidgetItem(self.treeWidget)
        # data.setExpanded(True)
        datadict = {'data':data, 'dataname':dataname,'framecount':0}

        num, datas = self.load_datainfo(path, dataname)
        print("datas[0]: ", datas[0])
        for i in range(num):
            frame = QTreeWidgetItem()
            # frame.setExpanded(True)
            framename = datas[i]
            framedict = {'frame':frame, 'framename':framename}
            self.framelist.append(framedict)
            frame.setText(0, framename)
            data.addChild(frame)

        datadict['framecount'] = num
        data.setText(0, dataname)
        self.datalist.append(datadict)
        return os.path.join(path, datas[0])

    def load_datainfo(self, path, dataname):
        data = [ x for x in os.listdir(path) if os.path.splitext(dataname)[0][:-4] in x \
                                and os.path.splitext(x)[-1] == ".tif"]
        return len(data), data

    def onclick(self, event):
        global ix, iy
        ix, iy = event.xdata, event.ydata
        if self.checkBox.isChecked():
            return
        else:
            self.coords.append([ix, iy])
            # print('x = %d, y = %d'%(ix, iy))
            c = Circle((ix, iy), 25, fill=False, color='g')
            self.axes.add_patch(c)

            self.canvas.draw()
            self.canvas.flush_events()
            return [ix, iy]

    @pyqtSlot()
    def on_pushButton_clicked(self):
        self.axes = self.figure.add_subplot()
        # self.axes.clear()

        filename, _ = QFileDialog.getOpenFileName(self, "Select file", "./")

        self.dataset = filename
        path, dataname = os.path.split(self.dataset)
        frame1 = self.create_datasets(path, dataname)

        tif = libtiff.TIFF.open(frame1)
        self.data = tif.read_image()
        self.data = np.abs(self.data)

        maximum = np.max(self.data)
        minimum = np.min(self.data)
        mean = np.mean(self.data)
        sigma = np.std(self.data)
        print("maximum: ", maximum)
        print("minimum: ", minimum)
        print("mean: ", mean)
        print("sigma: ", sigma)
        self.curmin = max(minimum, mean - 3.0*sigma)
        self.curmax = min(maximum, mean + 3.0*sigma)

        self.horizontalScrollBar.setMinimum(minimum)
        self.horizontalScrollBar_2.setMaximum(maximum)
        self.horizontalScrollBar.setMinimum(minimum)
        self.horizontalScrollBar_2.setMaximum(maximum)
        self.horizontalScrollBar.setValue(self.curmin)
        self.horizontalScrollBar_2.setValue(self.curmax)

        self.axes.imshow(self.data, cmap='Greys_r', vmin=self.curmin, vmax=self.curmax)
        self.axes.set_xticks([])
        self.axes.set_yticks([])
        self.axes.set_yticklabels([])
        self.axes.set_xticklabels([])

        self.figure.canvas.mpl_connect('button_press_event', self.onclick)
        self.canvas.draw()

    @pyqtSlot()
    def on_pushButton_2_clicked(self):
        self.centerpts = com.center(np.flipud(self.data), self.coords)
        cpsx = self.centerpts[0]
        cpsy = 4096 - self.centerpts[1]
        c = Circle((cpsx, cpsy), 36, fill=False, color='b')
        self.axes.add_patch(c)
        self.canvas.draw()
        print("centerx: ", self.centerpts[0], " centery: ", self.centerpts[1])

    @pyqtSlot()
    def on_pushButton_3_clicked(self):
        radius = 24
        if len(self.coords_tmp) == 0:
            self.coords_tmp = np.loadtxt("/cs2/shuangbo/tmp/coords.txt")

        for xi, yi in self.coords_tmp:
            yi = 4096 - yi
            c = Circle((xi, yi), radius, fill=False, color='r')
            self.axes.add_patch(c)
        self.canvas.draw()

    @pyqtSlot()
    def on_pushButton_4_clicked(self):

        for co in self.coords:
            self.coords_tmp.append(com.com(np.flipud(self.data), co))
        coords_tmp = np.array(self.coords_tmp)
        np.savetxt("/cs2/shuangbo/tmp/coords.txt", self.coords_tmp)

    @pyqtSlot()
    def on_pushButton_5_clicked(self):
        self.thread = Thread.Thread(self.dataset, self.centerpts)

        self.pushButton_5.setEnabled(False)
        self.axes1 = self.figure1.add_subplot()
        self.axes1.clear()
        self.thread.signal.connect(self.Update)
        self.thread.finish.connect(self.buttonEnable)
        self.thread.start()

    def buttonEnable(self):
        self.pushButton_5.setEnabled(True)

    def Update(self, data, intens, iml, pl):
        self.axes.clear()
        self.axes1.clear()
        self.axes.imshow(data, cmap='Greys_r', vmin=self.curmin, vmax=self.curmax)
        self.axes.set_xticks([])
        self.axes.set_yticks([])
        self.axes.set_yticklabels([])
        self.axes.set_xticklabels([])

        self.axes1.set_xlim(0, iml)
        for i in range(pl):
            self.axes1.plot(intens[:,i])
        self.canvas.draw()
        self.canvas1.draw()

class LineBuilder:
    def __init__(self, line):
        self.line = line
        self.xs = list(line.get_xdata())
        self.ys = list(line.get_ydata())
        self.cid = line.figure.canvas.mpl_connect('button_press_event', self)

    def __call__(self, event):
        if event.inaxes!=self.line.axes: return
        self.xs.append(event.xdata)
        self.ys.append(event.ydata)
        if len(self.xs) < 3:
            return
        elif len(self.xs) == 4:
            self.xs.pop(0)
            self.ys.pop(0)
        self.xs[0], self.xs[1] = self.xs[1], self.xs[0]
        self.ys[0], self.ys[1] = self.ys[1], self.ys[0]
        print("xs: ", self.xs)
        print("ys: ", self.ys)
        self.line.set_data(self.xs, self.ys)
        self.line.figure.canvas.draw()

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    ui = MainWindow()
    ui.show()
    sys.exit(app.exec_())
