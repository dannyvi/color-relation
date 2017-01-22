#!/usr/local/bin/python3.4
#-*-coding:utf-8-*-

from PyQt5 import QtCore,QtGui,QtWidgets
import numpy as np
import sys,os
from colorindex import jch_rgb_index
from base_relations import image_path
from PIL import Image

def define_map_colors():
    base = np.zeros((5,20,2),dtype='int')
    for i in range(5):
        base[i,:,0]=i*10+30
    for i in range(20):
        base[:,i,1]=i*18
    j = base[:,:,0].reshape(-1).copy()
    h = base[:,:,1].reshape(-1).copy()
    index = jch_rgb_index[j,50,h]
    full_index = np.zeros((4,100,3),dtype='uint8')
    for i in range(4):
        full_index[i] = index
    return full_index.reshape(400,3)

def define_map_colors2():
    base = np.zeros((100,3),dtype='int')
    base[:,0] = np.arange(100)
    base[:,1] = 100
    base[:,2] = np.arange(100)*3
    index = jch_rgb_index[base[:,0],base[:,1],base[:,2]]
    full_index = np.zeros((4,100,3),dtype='uint')
    for i in range(4):
        full_index[i] = index
    return full_index.reshape(400,3)

index_1 = define_map_colors()
index_2 = define_map_colors2()

contour_index = [index_1,index_2]

SE_J,SE_C,SE_H = [0,1,2]


def showPic():
    i = contour_index[0].reshape(4,100,3).repeat(10,0).repeat(10,1).astype('uint8')
    pic = Image.fromarray(i)
    pic.show()

class valueBar(QtWidgets.QGraphicsObject):
    selectionChanged = QtCore.pyqtSignal(int)
    valueChanged = QtCore.pyqtSignal(int)
    mapindexChanged = QtCore.pyqtSignal(int)
    def __init__(self):
        super(valueBar,self).__init__()
        self.selection = 0
        self.intervalue = 1
        self.limitation = [[1,100],[1,115],[1,360]]

        p = QtGui.QPalette()
        p.setColor(QtGui.QPalette.Window,QtGui.QColor(253,253,253))
        #frm          = QtGui.QFrame()
        self.check_1 = QtWidgets.QCheckBox("明度")
        self.check_2 = QtWidgets.QCheckBox("纯度")
        self.check_3 = QtWidgets.QCheckBox("色相")
        self.check_1.setFixedWidth(60)
        self.check_2.setFixedWidth(60)
        self.check_3.setFixedWidth(60)
        self.check_1.setCheckState(QtCore.Qt.Checked)
        self.check_1.stateChanged.connect(lambda x:self.emitSelection(x)(SE_J))
        self.check_2.stateChanged.connect(lambda x:self.emitSelection(x)(SE_C))
        self.check_3.stateChanged.connect(lambda x:self.emitSelection(x)(SE_H))
        #self.check_1.setPalette(p)
        #self.check_2.setPalette(p)
        #self.check_3.setPalette(p)

        self.group   = QtWidgets.QButtonGroup()
        self.group.setExclusive(True)
        self.group.addButton(self.check_1)
        self.group.addButton(self.check_2)
        self.group.addButton(self.check_3)

        label = QtWidgets.QLabel("      间距:")
        label.setFixedWidth(50)
        self.valueinput = QtWidgets.QLineEdit("1")
        self.valueinput.setFixedWidth(30)
        self.valueinput.setMaxLength(3)
        self.valueinput.returnPressed.connect(self.emitInterv)

        self.indexmap = QtWidgets.QComboBox()
        self.indexmap.addItem("色轮")
        self.indexmap.addItem("线性")
        self.indexmap.setFixedWidth(65)
        self.indexmap.activated.connect(self.setContourIndex)

        layout = QtWidgets.QHBoxLayout()
        layout.setSpacing(5)
        layout.addWidget(self.check_1)
        layout.addWidget(self.check_2)
        layout.addWidget(self.check_3)
        layout.addWidget(label)
        layout.addWidget(self.valueinput)
        layout.addWidget(self.indexmap)
        layout.setContentsMargins(5,5,5,5)

        w = QtWidgets.QWidget()
        w.setFixedSize(330,30)
        w.setLayout(layout)
        w.setPalette(p)

        b = QtWidgets.QGraphicsProxyWidget(self)
        b.setWidget(w)
        b.setPos(0,0)

    def boundingRect(self):
        return QtCore.QRectF(0,0,100,100)


    def paint(self,painter,option,widget):
        pass

    @QtCore.pyqtSlot(int)
    def emitSelection(self,state):
        def send(selection):
            if selection in [SE_J,SE_C,SE_H]:
                if selection != self.selection:
                    self.selection = selection
                    self.selectionChanged.emit(selection)
        def nomean(selection):
            pass
        if state == QtCore.Qt.Checked:
            return send
        else: return nomean

    @QtCore.pyqtSlot()
    def emitInterv(self):
        try:
        #if 1:
            t = int(self.valueinput.text())#int(text)
            if t !=self.intervalue and \
               t>=self.limitation[self.selection][0] and \
               t<=self.limitation[self.selection][1]:
                self.valueChanged.emit(t)
            else:
                self.valueinput.setText("1")

        except:
            self.valueinput.setText("1")
            #pass

    @QtCore.pyqtSlot(int)
    def setContourIndex(self,selection):
        self.mapindexChanged.emit(selection)


class ImgScene(QtWidgets.QGraphicsScene):
    def __init__(self,jch,shape):
        super(ImgScene,self).__init__()
        self.setSceneRect(0,0,max(shape[1],780),shape[0]+30)
        self.gg = QtWidgets.QGraphicsPixmapItem()
        self.gg.setPos(0,30)
        self.addItem(self.gg)

        a = valueBar()
        self.addItem(a)
        a.setPos(0,0)
        a.selectionChanged.connect(self.resetSelection)
        a.valueChanged.connect(self.resetInterv)
        a.mapindexChanged.connect(self.resetMapIndex)

        self.jch = jch
        self.shape = shape
        self.rgb = jch_rgb_index[self.jch[:,0],self.jch[:,1],self.jch[:,2]]

        self.interval = 10
        self.selection = SE_J
        self.contmap = 0

        self.renderPix()

    @QtCore.pyqtSlot(int)
    def resetSelection(self,n):
        self.selection = n
        self.renderPix()

    @QtCore.pyqtSlot(int)
    def resetInterv(self,n):
        self.interval = n
        self.renderPix()
        #print(n)

    @QtCore.pyqtSlot(int)
    def resetMapIndex(self,selection):
        self.contmap = selection
        self.renderPix()

    def renderPix(self):
        seq = (self.jch[:,self.selection]/self.interval).astype('int')*self.interval
        rgb = contour_index[self.contmap][seq].reshape(-1,3).astype('uint32').copy()
    #i = contour_index.reshape(4,100,3).repeat(10,0).repeat(10,1).astype('uint8')
        #rgb = contour_index.reshape(4,100,3).repeat(5,0).repeat(5,1).astype('uint32').reshape(-1,3)
        self.packedrgb=(255<<24|rgb[:,0]<<16|rgb[:,1]<<8|rgb[:,2]).flatten().tobytes()
        #im = QtGui.QImage(packedrgb,500,20,QtGui.QImage.Format_RGB32)#self.shape[1],self.shape[0],QtGui.QImage.Format_RGB32)
        im = QtGui.QImage(self.packedrgb,self.shape[1],self.shape[0],QtGui.QImage.Format_RGB32)
        self.gg.setPixmap(QtGui.QPixmap(im))

class ImgView(QtWidgets.QGraphicsView):
    def __init__(self,jch,shape):
        super(ImgView,self).__init__()
        self.move(20,20)
        self.resize(max(shape[1],780),shape[0]+30)

        self.setMinimumSize(780,500)
        self.setWindowTitle("Image analyze")
        a = ImgScene(jch,shape)
        self.setScene(a)

def showcontour(jch,shape):

    #global app
    #app=QtWidgets.QApplication.instance()#(sys.argv)
    #if not app:
    from backends import create_qApp,exe_qApp
    create_qApp()
    #app = QtWidgets.QApplication(sys.argv)
    #app.aboutToQuit.connect(app.deleteLater)
    v=ImgView(jch,shape)
    v.show()
    exe_qApp()
    #sys.exit(app.exec_())
    #else:
    #    v=ImgView(jch,shape)
    #    v.show()

    #sys.exit(app.exec())
    #while not app.exec_():
    #    del(app)
    #    return 0

if __name__=="__main__":
    from Imga import tst
    b = None
    if len(sys.argv)>1:
        b = tst(sys.argv[1])
    else:
        b = tst("a.jpg")
    showcontour(b.jch,b.shape)
    #showPic()
