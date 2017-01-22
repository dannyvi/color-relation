#!/usr/local/bin/python3.4
#-*-coding:utf-8-*-

from PyQt5 import QtCore,QtGui,QtWidgets
import numpy as np
import sys,os
from colorindex import jch_rgb_index
from base_relations import image_path
from PIL import Image


class valueModifier(QtWidgets.QGraphicsObject):
    ValueChanged = QtCore.pyqtSignal(int,int)
    CvChanged    = QtCore.pyqtSignal(int,int,int)
    def __init__(self,name,tmin,tmax):
        super(valueModifier,self).__init__()
        self.tmin = tmin
        self.tmax = tmax
        p = QtGui.QPalette()
        p.setColor(QtGui.QPalette.Window,QtGui.QColor(250,250,250))
        a = QtWidgets.QLabel(name+"范围:")#QTextEdit() #Label("A")
        a.setAutoFillBackground(True)
        a.setFixedWidth(60)
        a.setPalette(p)
        #d = QtWidgets.QSlider(QtCore.Qt.Horizontal)

        self.minvalue = QtWidgets.QLineEdit("0")
        self.minvalue.setFixedWidth(30)
        self.minvalue.setMaxLength(3)
        self.maxvalue = QtWidgets.QLineEdit("0")
        self.maxvalue.setFixedWidth(30)
        self.maxvalue.setMaxLength(3)
        self.minvalue.returnPressed.connect(self.minValueChanged)
        self.maxvalue.returnPressed.connect(self.maxValueChanged)
        f = QtWidgets.QLabel("颜色:")
        f.setFixedWidth(30)
        self.mskcolor = QtWidgets.QLineEdit("ffffff")
        self.mskcolor.setFixedWidth(60)
        self.mskcolor.setMaxLength(6)
        self.mskcolor.returnPressed.connect(self.colorChanged)

        self.prop = QtWidgets.QLabel(" 0%")

        l = QtWidgets.QHBoxLayout()
        l.setSpacing(0)
        l.addWidget(a)
        l.addWidget(self.minvalue)
        l.addWidget(self.maxvalue)
        l.addWidget(f)
        l.addWidget(self.mskcolor)
        l.addWidget(self.prop)
        l.setContentsMargins(5,5,5,5)
        w = QtWidgets.QWidget()
        w.setFixedSize(270,30)
        w.setLayout(l)
        w.setPalette(p)
        b = QtWidgets.QGraphicsProxyWidget(self)
        b.setWidget(w)
        b.setPos(0,0)

    @QtCore.pyqtSlot()
    def minValueChanged(self):
        value = self.minvalue.text()
        if value.isdigit():
            v = int(value)
            if v>=self.tmin:
                if v<=int(self.maxvalue.text()):
                    self.ValueChanged.emit(v,int(self.maxvalue.text()))
                else:
                    v = int(self.maxvalue.text())
                    self.minvalue.setText(str(v))
                    self.ValueChanged.emit(v,v)
            else:
                self.minvalue.setText(str(self.tmin))
                self.ValueChanged.emit(self.tmin,int(self.maxvalue.text()))
        else:
            self.minvalue.setText(str(self.tmin))
            self.ValueChanged.emit(self.tmin,int(self.maxvalue.text()))

    @QtCore.pyqtSlot()
    def maxValueChanged(self):
        value = self.maxvalue.text()
        if value.isdigit():
            v = int(value)
            if v<=self.tmax:
                if v>=int(self.minvalue.text()):
                    self.ValueChanged.emit(int(self.minvalue.text()),v)
                else:
                    v = int(self.minvalue.text())
                    self.maxvalue.setText(str(v))
                    self.ValueChanged.emit(v,v)
            else:
                self.maxvalue.setText(str(self.tmax))
                self.ValueChanged.emit(self.tmin,int(self.maxvalue.text()))

        else:
            self.maxvalue.setText(str(self.tmax))
            self.ValueChanged.emit(self.tmin,int(self.maxvalue.text()))

    @QtCore.pyqtSlot()
    def colorChanged(self):
        value = self.mskcolor.text()

        if len(value)!=6:
            self.mskcolor.setText("000000")
            self.mskcolor.selectAll()
        try:
            v = int(value,16)
            self.CvChanged.emit(v>>16%256,(v>>8)%256,v%256)
        except:
            self.mskcolor.setText("000000")
            self.mskcolor.selectAll()

    def boundingRect(self):
        return QtCore.QRectF(0,0,100,100)


    def paint(self,painter,option,widget):
        pass

class ImgScene(QtWidgets.QGraphicsScene):
    def __init__(self,jch,shape):
        super(ImgScene,self).__init__()
        self.setSceneRect(0,0,max(shape[1],780),shape[0]+30)
        #self.gg = None
        self.gg = QtWidgets.QGraphicsPixmapItem()
        self.gg.setPos(0,30)
        self.addItem(self.gg)

        self.k = valueModifier("明度",0,100)
        self.l = valueModifier("纯度",0,114)
        self.m = valueModifier("色相",0,359)
        self.addItem(self.k)
        self.addItem(self.l)
        self.addItem(self.m)
        self.k.setPos(0,0)
        self.l.setPos(260,0)
        self.m.setPos(520,0)
        self.k.mskcolor.setText("ff00ff")
        self.l.mskcolor.setText("ffff00")
        self.m.mskcolor.setText("0000ff")

        self.maskvalue = [[0,0],[0,0],[0,0]]
        self.maskcolor = [[255,0,255],[255,255,0],[0,0,255]]
        self.jch = jch
        self.shape = shape
        self.rgb = jch_rgb_index[self.jch[:,0],self.jch[:,1],self.jch[:,2]]

        self.k.ValueChanged.connect(self.altj)
        self.l.ValueChanged.connect(self.altc)
        self.m.ValueChanged.connect(self.alth)
        self.k.CvChanged.connect(self.altjc)
        self.l.CvChanged.connect(self.altcc)
        self.m.CvChanged.connect(self.althc)

        self.showpicwithmask()

    def altj(self,a,b):
        self.maskvalue[0] = (a,b)
        self.showpicwithmask()
    def altc(self,a,b):
        self.maskvalue[1] = (a,b)
        self.showpicwithmask()
    def alth(self,a,b):
        self.maskvalue[2] = (a,b)
        self.showpicwithmask()
    def altjc(self,a,b,c):
        self.maskcolor[0] = (a,b,c)
        self.showpicwithmask()
    def altcc(self,a,b,c):
        self.maskcolor[1] = (a,b,c)
        self.showpicwithmask()
    def althc(self,a,b,c):
        self.maskcolor[2] = (a,b,c)
        self.showpicwithmask()

    def showpicwithmask(self):
        #if self.gg in self.items():
        #    self.removeItem(self.gg)
        m1,m2,m3 = self.maskvalue
        mask1 = np.all([self.jch[:,0]>m1[0],self.jch[:,0]<m1[1]],axis=0)
        mask2 = np.all([self.jch[:,1]>m2[0],self.jch[:,1]<m2[1]],axis=0)
        mask3 = np.all([self.jch[:,2]>m3[0],self.jch[:,2]<m3[1]],axis=0)
        rgb = self.rgb.astype('uint32').copy()

        rgb[mask1] = self.maskcolor[0]
        rgb[mask2] = self.maskcolor[1]
        rgb[mask3] = self.maskcolor[2]

        v1 = str(int(mask1.sum() * 100 / len(mask1)))+"%"
        v2 = str(int(mask2.sum() * 100 / len(mask1)))+"%"
        v3 = str(int(mask3.sum() * 100 / len(mask1)))+"%"

        self.packedrgb=(255<<24|rgb[:,0]<<16|rgb[:,1]<<8|rgb[:,2]).flatten().tobytes()


        im = QtGui.QImage(self.packedrgb,self.shape[1],self.shape[0],QtGui.QImage.Format_RGB32)


        #self.gg  = QtWidgets.QGraphicsPixmapItem(QtGui.QPixmap(im))
        self.gg.setPixmap(QtGui.QPixmap(im))
        self.k.prop.setText(v1)
        self.l.prop.setText(v2)
        self.m.prop.setText(v3)
        #self.addItem(self.gg)


class ImgView(QtWidgets.QGraphicsView):
    def __init__(self,jch,shape):
        super(ImgView,self).__init__()
        self.move(20,20)
        self.resize(max(shape[1],780),shape[0]+30)

        self.setMinimumSize(780,500)
        self.setWindowTitle("Image analyze")
        a = ImgScene(jch,shape)
        self.setScene(a)

def showmask(jch,shape):

    #global app
    #app=QtWidgets.QApplication.instance()#(sys.argv)
    #if not app:
    #app = QtWidgets.QApplication(sys.argv)
    #app.aboutToQuit.connect(app.deleteLater)
    from backends import create_qApp,exe_qApp
    create_qApp()
    v=ImgView(jch,shape)
    v.show()
    exe_qApp()
    #sys.exit(app.exec_())
    #app.exec_()
    #del(app)
    #global app
    #app=QtWidgets.QApplication(sys.argv)
    #else:
    #    v=ImgView(jch,shape)
    #    v.show()
    #while not app.exec_():
    #    del(app)
    #    return 0

if __name__=="__main__":
    from Imga import tst
    b = None
    #print(sys.argv)
    if len(sys.argv)>1:
        b = tst(sys.argv[1])
    else:
        b = tst("a.jpg")
    showmask(b.jch,b.shape)

    #app=QtWidgets.QApplication(sys.argv)
    #v=ImgView(b.jch.copy(),b.shape)
    #v.show()
    #sys.exit(app.exec_())
    #sys.exit(showmask(b.jch,b.shape))
