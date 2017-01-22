#!/usr/local/bin/python3.4
#-*-coding:utf-8-*-

from PyQt5 import QtCore,QtGui,QtWidgets
import numpy as np
import sys,os
from colorindex import jch_rgb_index
from base_relations import image_path
from PIL import Image


class valueModifier(QtWidgets.QWidget):
    jrChanged = QtCore.pyqtSignal(int,int)
    jvChanged    = QtCore.pyqtSignal(int,int,int)
    crChanged = QtCore.pyqtSignal(int,int)
    cvChanged    = QtCore.pyqtSignal(int,int,int)
    hrChanged = QtCore.pyqtSignal(int,int)
    hvChanged    = QtCore.pyqtSignal(int,int,int)
    #Type = QtWidgets.QGraphicsProxyWidget.UserType
    def __init__(self):
        super(valueModifier,self).__init__()
        self.jmin = 0
        self.jmax = 100
        self.cmin = 0
        self.cmax = 114
        self.hmin = 0
        self.hmax = 360
        p = QtGui.QPalette()
        p.setColor(QtGui.QPalette.Window,QtGui.QColor(250,250,250))
        #for i in ("明度范围:","纯度范围","色相范围"):
        a = QtWidgets.QLabel("明度范围:")#QTextEdit() #Label("A")
        #a.setAutoFillBackground(True)
        a.setFixedWidth(60)
        a.setPalette(p)

        b = QtWidgets.QLabel("纯度范围:")
        b.setFixedWidth(60)
        b.setPalette(p)

        c = QtWidgets.QLabel("纯度范围:")
        c.setFixedWidth(60)
        c.setPalette(p)

        self.jminf = QtWidgets.QLineEdit("0")
        self.jminf.setFixedWidth(30)
        self.jminf.setMaxLength(3)
        self.jmaxf = QtWidgets.QLineEdit("0")
        self.jmaxf.setFixedWidth(30)
        self.jmaxf.setMaxLength(3)
        #self.minvalue.returnPressed.connect(self.minValueChanged)
        #self.maxvalue.returnPressed.connect(self.maxValueChanged)
        self.cminf = QtWidgets.QLineEdit("0")
        self.cminf.setFixedWidth(30)
        self.cminf.setMaxLength(3)
        self.cmaxf = QtWidgets.QLineEdit("0")
        self.cmaxf.setFixedWidth(30)
        self.cmaxf.setMaxLength(3)

        self.hminf = QtWidgets.QLineEdit("0")
        self.hminf.setFixedWidth(30)
        self.hminf.setMaxLength(3)
        self.hmaxf = QtWidgets.QLineEdit("0")
        self.hmaxf.setFixedWidth(30)
        self.hmaxf.setMaxLength(3)

        d = QtWidgets.QLabel("颜色:")
        d.setFixedWidth(30)
        e = QtWidgets.QLabel("颜色:")
        e.setFixedWidth(30)
        f = QtWidgets.QLabel("颜色:")
        f.setFixedWidth(30)

        self.mskjcolor = QtWidgets.QLineEdit("ffffff")
        self.mskjcolor.setFixedWidth(60)
        self.mskjcolor.setMaxLength(6)
        #self.mskjcolor.returnPressed.connect(self.colorChanged)
        self.mskccolor = QtWidgets.QLineEdit("ffffff")
        self.mskccolor.setFixedWidth(60)
        self.mskccolor.setMaxLength(6)

        self.mskhcolor = QtWidgets.QLineEdit("ffffff")
        self.mskhcolor.setFixedWidth(60)
        self.mskhcolor.setMaxLength(6)

        l = QtWidgets.QHBoxLayout()
        l.setContentsMargins(5,5,5,5)
        l.setSpacing(0)

        l.addWidget(a)
        l.addWidget(self.jminf)
        l.addWidget(self.jmaxf)
        l.addWidget(d)
        l.addWidget(self.mskjcolor)

        l.addWidget(b)
        l.addWidget(self.cminf)
        l.addWidget(self.cmaxf)
        l.addWidget(e)
        l.addWidget(self.mskccolor)

        l.addWidget(c)
        l.addWidget(self.hminf)
        l.addWidget(self.hmaxf)
        l.addWidget(f)
        l.addWidget(self.mskhcolor)

        #w = QtWidgets.QWidget()
        self.setFixedSize(780,30)
        self.setLayout(l)
        self.setPalette(p)
        #b = QtWidgets.QGraphicsProxyWidget(self)
        #self.setWidget(w)
        #self.setPos(0,0)

#    @QtCore.pyqtSlot()
#    def minValueChanged(self):
#        value = self.minvalue.text()
#        if value.isdigit():
#            v = int(value)
#            if v>=self.tmin:
#                if v<=int(self.maxvalue.text()):
#                    self.ValueChanged.emit(v,int(self.maxvalue.text()))
#                else:
#                    v = int(self.maxvalue.text())
#                    self.minvalue.setText(str(v))
#                    self.ValueChanged.emit(v,v)
#            else:
#                self.minvalue.setText(str(self.tmin))
#                self.ValueChanged.emit(self.tmin,int(self.maxvalue.text()))
#        else:
#            self.minvalue.setText(str(self.tmin))
#            self.ValueChanged.emit(self.tmin,int(self.maxvalue.text()))
#
#    @QtCore.pyqtSlot()
#    def maxValueChanged(self):
#        value = self.maxvalue.text()
#        if value.isdigit():
#            v = int(value)
#            if v<=self.tmax:
#                if v>=int(self.minvalue.text()):
#                    self.ValueChanged.emit(int(self.minvalue.text()),v)
#                else:
#                    v = int(self.minvalue.text())
#                    self.maxvalue.setText(str(v))
#                    self.ValueChanged.emit(v,v)
#            else:
#                self.maxvalue.setText(str(self.tmax))
#                self.ValueChanged.emit(self.tmin,int(self.maxvalue.text()))
#
#        else:
#            self.maxvalue.setText(str(self.tmax))
#            self.ValueChanged.emit(self.tmin,int(self.maxvalue.text()))
#    #def setValue(a,b):
#    @QtCore.pyqtSlot()
#    def colorChanged(self):
#        value = self.mskcolor.text()
#        #if value.isalnum():
#        if len(value)!=6:
#            self.mskcolor.setText("000000")
#            self.mskcolor.selectAll()
#        try:
#            v = int(value,16)
#            self.CvChanged.emit(v>>16%256,(v>>8)%256,v%256)
#        except:
#            self.mskcolor.setText("000000")
#            self.mskcolor.selectAll()

    #def type(self):
    #    return self.Type

    def boundingRect(self):
        return QtCore.QRectF(0,0,100,100)
        #pass

    def paint(self,painter,option,widget):
        pass

class ImgScene(QtWidgets.QGraphicsScene):
    def __init__(self):
        super(ImgScene,self).__init__()
        #self.setSceneRect(0,0,max(shape[1],780),shape[0]+30)
        #self.gg = None

        #panel = valueModifier()
        #self.pan = self.addWidget(panel)
        #self.pan.setPos(0,0)
#        k = valueModifier("明度",0,100)
#        l = valueModifier("纯度",0,114)
#        m = valueModifier("色相",0,359)
#        self.addItem(k)
#        self.addItem(l)
#        self.addItem(m)
#        k.setPos(0,0)
#        l.setPos(260,0)
#        m.setPos(520,0)

        #self.maskvalue = ((0,0),(0,0),(0,0))
        #self.maskcolor = ((255,0,255),(255,255,0),(0,0,255))
        #pix = QtGui.QPixmap(image_path+"a.jpg")
        #pf  = QtWidgets.QGraphicsPixmapItem(pix)
        #self.addItem(pf)
        #pf.setPos(0,30)
        #self.jch = jch
        #self.shape = shape
        #self.rgb = jch_rgb_index[self.jch[:,0],self.jch[:,1],self.jch[:,2]]

        #print(self.jch)
        #im = Image.fromarray(self.rgb.reshape(self.shape))
        #im.show()

        #self.showpicwithmask()

    def showpicwithmask(self):
        #if self.gg in self.items():
        #    self.removeItem(self.gg)
        rgb = self.rgb.copy().astype('uint32')
        #m1,m2,m3 = self.maskvalue
        #mask1 = np.all([self.jch[:,0]>m1[0],self.jch[:,0]<m1[1]],axis=0)
        #mask2 = np.all([self.jch[:,1]>m2[0],self.jch[:,1]<m2[1]],axis=0)
        #mask3 = np.all([self.jch[:,2]>m3[0],self.jch[:,2]<m3[1]],axis=0)
        #rgb[mask1] = self.maskcolor[0]
        #rgb[mask2] = self.maskcolor[1]
        #rgb[mask3] = self.maskcolor[2]
        #packedrgb = np.zeros(rgb.shape[:-1],dtype="uint32")
        #rgb = rgb.reshape(self.shape).astype('uint32')
        #print(rgb,rgb.shape,rgb.dtype)
        packedrgb=(255<<24|rgb[:,0]<<16|rgb[:,1]<<8|rgb[:,2]).flatten()
        #print(packedrgb>>24)
        im = QtGui.QImage(packedrgb,self.shape[1],self.shape[0],QtGui.QImage.Format_RGB32)
        #im.save('kkkkk.png')
        #return im
        self.gg  = QtWidgets.QGraphicsPixmapItem(QtGui.QPixmap(im))
        self.gg.setPos(0,30)
        self.addItem(self.gg)
        #print(im.format())
        #self.gg = QtGui.QPixmap(im)#,QtCore.Qt.KeepAspectRatio)
        #self.gg  = QtWidgets.QGraphicsPixmapItem(QtGui.QPixmap(im))
        #self.gg.setPos(0,30)
        #self.addItem(self.gg)



class ImgView(QtWidgets.QGraphicsView):
    def __init__(self):#,jch,shape):
        super(ImgView,self).__init__()
        self.move(20,20)
        #self.resize(max(shape[1],780),shape[0]+30)
        #self.setMinimumSize(930,500)
        self.setWindowTitle("Image analyze")
        self.sc = QtWidgets.QGraphicsScene()#jch,shape)
        self.setScene(self.sc)

def showmask(jch,shape):
    app=QtWidgets.QApplication(sys.argv)
    v=ImgView()#jch,shape)
    v.show()
    #app.exec_()
    return sys.exit(app.exec_())

#def showmaskp(jch,shape):
#    p = Process(target=showmask,args=(jch,shape))
#    p.start()
#    p.join()

if __name__=="__main__":
    app=QtWidgets.QApplication(sys.argv)
    v=ImgView()
    v.show()
    #pass
    sys.exit(app.exec_())
