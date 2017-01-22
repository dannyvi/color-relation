#!/usr/local/bin/python3.4
#-*-coding:utf-8-*-

from PyQt5 import QtCore,QtWidgets,QtGui,QtOpenGL
from dimension.npcolorconvert import npjch2rgb
import numpy as np
from recolor import rColorSeq,multIterColorSeq,genRule


class FScene(QtWidgets.QGraphicsScene):
    def __init__(self):
        super(FScene,self).__init__()
        self.setBackgroundBrush(QtCore.Qt.white)

        size = 20
        ri = np.random.randint
        rf = np.random.random
        #self.arg_center = (rf(3)-[0.5,0,0])/1.1 + [0.5,0,0]
        #self.arg_rule   = rf(ri(3,7)*3).reshape(-1,3)
        #self.arg_scale  = rf()
        #self.arg_time   = ri(1,4)*2

        #self.arg_center = np.array([0.5,0.08,54/360])
        #self.arg_rule   = np.array([[0.97,0.4,56/360],\
        #                            [0.17,0.78,316/360],\
        #                            [0.50,0.41,326/360],\
        #                            [0.78,0.09,27/360]])
                                    #[0.68,0.14,20/360]])
        #self.arg_scale  = 0.06437888820435045
        #self.arg_time   = 2

        rulelen = ri(2,3)
        rulemin,rulemax = [2,5]
        self.arg_center = (rf(3)-[0.5,0,0])/1.1 + [0.5,0,0]
        self.arg_rule   = genRule(rulelen,rulemin,rulemax)
        self.arg_scale  = rf(rulelen)
        self.arg_time   = ri(1,3)*2

        self.colors = multIterColorSeq(center = self.arg_center,\
                                rule   = self.arg_rule,\
                                scale  = self.arg_scale,\
                                time   = self.arg_time)
        rgb         = npjch2rgb(self.colors).astype('uint32')
        le = int(np.sqrt(len(self.colors)))
        arr2 = rgb.reshape(le,le,3).repeat(size,0).repeat(size,1)
        x = np.random.permutation(len(rgb))
        r1 = rgb.copy()[x]
        arr1 = r1.reshape(le,le,3).\
            repeat(size,0).repeat(size,1)
        self.seq2 = (255<<24|arr2[:,:,0]<<16|arr2[:,:,1]<<8|arr2[:,:,2]).flatten()
        self.seq1 = (255<<24|arr1[:,:,0]<<16|arr1[:,:,1]<<8|arr1[:,:,2]).flatten()

        self.image1=QtGui.QImage(self.seq1,size*le,size*le,\
                                 QtGui.QImage.Format_RGB32)
        self.pic1 = QtWidgets.QGraphicsPixmapItem(QtGui.QPixmap(self.image1))
        self.pic1.setPos(0,0)

        self.addItem(self.pic1)

        self.image2=QtGui.QImage(self.seq2,size*le,size*le,\
                                 QtGui.QImage.Format_RGB32)
        self.pic2 = QtWidgets.QGraphicsPixmapItem(QtGui.QPixmap(self.image2))
        self.pic2.setPos(0,0)
        self.pic2.setVisible(False)
        self.addItem(self.pic2)

        #print(len(x))

        srule ="\n".join(list(map(lambda x: \
                                  str((x*[100,100,360]).\
                                      astype('int')).replace("\n","").\
                                  replace("[","").replace("]"," "),\
                   self.arg_rule)))
        #str(list(map(lambda x: (x*[100,100,360]).astype('int'),\
                #             self.arg_rule))).replace("\n","").replace("[","").replace("]"," ")+\
        self.arg_string = "\ncenter: " + \
                          str((self.arg_center*[100,100,360]).astype('int')).\
                          replace("\n","").replace("[","").replace("]","")+\
                          "\nrule:\n" +\
                          srule+\
                          "\nscale:  " +\
                          str(self.arg_scale) +\
                          "\ntime:   " + str(self.arg_time) + "\n"+\
                          str(x.reshape(le,le)) +"\n"

                          #str((self.arg_rule*[100,100,360]).astype('int')).\
                          #replace("\n","").replace("[","").replace("]"," ")+\

    def makeImage(self,pic,argstr):
        di        = "/Users/yudan/Documents/mypicworks/form/gh140_192/"  #.png")
        directory = di+"gh140_192_"
        f = open(di+"n.num","r")
        num = str(int(f.readline())+1)
        name = directory+num+".png"
        f.close()
        f = open(di+"n.num","w")
        f.write(num)
        f.close()
        pic.save(name)
        f2 = open(di+"log","a")
        f2.write(argstr)
        f2.write(name)
        f2.write('\n')
        f2.close()
        print('make Image')

    def make100Pic(self):
        size = 20
        for i in range(100):

            ri = np.random.randint
            rf = np.random.random
        #    arg_center = (rf(3)-[0.5,0,0])/1.1 + [0.5,0,0]
        #    arg_rule   = rf(ri(3,7)*3).reshape(-1,3)
        #    arg_scale  = rf()
        #    arg_time   = ri(1,4)*2
        #    colors = rColorSeq(center = arg_center,\
        #                            rule   = arg_rule,\
        #                            scale  = arg_scale,\
        #                            time   = arg_time)
        #    rgb         = npjch2rgb(colors).astype('uint32')
        #    le = np.sqrt(len(colors))
        #    a = rgb.reshape(le,le,3).repeat(50,0).repeat(50,1)
        #    x = np.random.permutation(len(rgb))
        #    r2 = rgb.copy()[x]

        #    b = r2.reshape(le,le,3).\
        #        repeat(50,0).repeat(50,1)#

        #    a1 = (255<<24 | a[:,:,0] << 16 | a[:,:,1]<<8 | a[:,:,2]).flatten()
        #    b1 = (255<<24 | b[:,:,0] << 16 | b[:,:,1]<<8 | b[:,:,2]).flatten()

        # #   arg_string = "\ncenter: " + \
        #                  str((arg_center*[100,100,360]).astype('int')).\
        #                  replace("\n","").replace("[","").replace("]","")+\
        #                  "\nrule:   " +\
        #                  str((arg_rule*[100,100,360]).astype('int')).\
        #                  replace("\n","").replace("[","").replace("]"," ")+\
        #                  "\nscale:  " +\
        #                  str(arg_scale) +\
        #                  "\ntime:   " + str(arg_time) + "\n"+\
        #                  str(x.reshape(le,le)) +"\n"

        #    im2         = QtGui.QImage(b1,50*le,50*le,QtGui.QImage.Format_RGB32)
        #    imm  = QtGui.QImage(a1,50*le,50*le,QtGui.QImage.Format_RGB32)
            rulelen = ri(1,3)
            rulemin,rulemax = [2,6]

            arg_center = (rf(3)-[0.5,0,0])/5 + [0.5,0,0]
            arg_rule   = genRule(rulelen,rulemin,rulemax)
            arg_scale  = rf(rulelen)
            arg_time   = ri(1,3)*2

            colors = multIterColorSeq(center = arg_center,\
                                rule   = arg_rule,\
                                scale  = arg_scale,\
                                time   = arg_time)
            rgb         = npjch2rgb(colors).astype('uint32')
            le = int(np.sqrt(len(colors)))
            arr2 = rgb.reshape(le,le,3).repeat(size,0).repeat(size,1)
            x = np.random.permutation(len(rgb))
            r1 = rgb.copy()[x]
            arr1 = r1.reshape(le,le,3).repeat(size,0).repeat(size,1)
            seq2 = (255<<24|arr2[:,:,0]<<16|arr2[:,:,1]<<8|arr2[:,:,2]).flatten()
            seq1 = (255<<24|arr1[:,:,0]<<16|arr1[:,:,1]<<8|arr1[:,:,2]).flatten()

            image1=QtGui.QImage(seq1,size*le,size*le,\
                                 QtGui.QImage.Format_RGB32)
            image2=QtGui.QImage(seq2,size*le,size*le,\
                                 QtGui.QImage.Format_RGB32)
            srule ="\n".join(list(map(lambda x: \
                                  str((x*[100,100,360]).\
                                      astype('int')).replace("\n","").\
                                  replace("[","").replace("]"," "),arg_rule)))
            arg_string = "\ncenter: " + \
                         str((arg_center*[100,100,360]).astype('int')).\
                          replace("\n","").replace("[","").replace("]","")+\
                          "\nrule:\n" +\
                          srule+\
                          "\nscale:  " +\
                          str(arg_scale) +\
                          "\ntime:   " + str(arg_time) + "\n"+\
                          str(x.reshape(le,le)) +"\n"
            self.makeImage(image1,arg_string)
            self.makeImage(image2,arg_string)

    def makeRcolorImage(self):
        size = 50
        for i in range(100):

            ri = np.random.randint
            rf = np.random.random
            arg_center = np.array([rf()/10+0.5,0.0,ri(0,360)/360])
            #np.array([rf()/10+0.5,rf()/10,ri(0,360)/360])
            #np.array([0.47,0.11,71/360])
            #(rf(3)-[0.5,0,0])/1.1 + [0.5,0,0]
            arg_rule   = np.array([[rf(),rf(),ri(141,192)/360],\
                                   [rf(),rf(),ri(140,192)/360],\
                                   [rf(),rf(),ri(0,360)/360]
                               ])
            #np.array([[0.80,0.46,171/360],\
                         #          [0.84,0.58,299/360],\
                         #          [0.73,0.65,292/360]])
            #rf(ri(4,5)*3).reshape(-1,3)
            arg_scale  = rf()
            arg_time   = ri(1,2)*2
            colors = rColorSeq(center = arg_center,\
                                    rule   = arg_rule,\
                                    scale  = arg_scale,\
                                    time   = arg_time)
            rgb         = npjch2rgb(colors).astype('uint32')
            le = np.sqrt(len(colors))
            a = rgb.reshape(le,le,3).repeat(50,0).repeat(50,1)
            x = np.random.permutation(len(rgb))
            r2 = rgb.copy()[x]

            b = r2.reshape(le,le,3).\
                repeat(50,0).repeat(50,1)#

            a1 = (255<<24 | a[:,:,0] << 16 | a[:,:,1]<<8 | a[:,:,2]).flatten()
            b1 = (255<<24 | b[:,:,0] << 16 | b[:,:,1]<<8 | b[:,:,2]).flatten()

            arg_string = "\ncenter: " + \
                          str((arg_center*[100,100,360]).astype('int')).\
                          replace("\n","").replace("[","").replace("]","")+\
                          "\nrule:   " +\
                          str((arg_rule*[100,100,360]).astype('int')).\
                          replace("\n","").replace("[","").replace("]"," ")+\
                          "\nscale:  " +\
                          str(arg_scale) +\
                          "\ntime:   " + str(arg_time) + "\n"+\
                          str(x.reshape(le,le)) +"\n"

            image1  = QtGui.QImage(b1,50*le,50*le,QtGui.QImage.Format_RGB32)
            image2  = QtGui.QImage(a1,50*le,50*le,QtGui.QImage.Format_RGB32)
            self.makeImage(image1,arg_string)
            self.makeImage(image2,arg_string)

    def keyPressEvent(self,event):
        self.dispatchKey(event)
        super(FScene,self).keyPressEvent(event)

    def dispatchKey(self,event):
        if event.key()==QtCore.Qt.Key_1:
            self.pic2.setVisible(False)
            self.pic1.setVisible(True)
        if event.key()==QtCore.Qt.Key_2:
            self.pic1.setVisible(False)
            self.pic2.setVisible(True)
        if event.key()==QtCore.Qt.Key_S:
            if self.pic1.isVisible():
                self.makeImage(self.image1,self.arg_string)
            if self.pic2.isVisible():
                self.makeImage(self.image2,self.arg_string)
        if event.key() == QtCore.Qt.Key_P:
            self.make100Pic()
        if event.key() == QtCore.Qt.Key_O:
            self.makeRcolorImage()

class FView(QtWidgets.QGraphicsView):
    def __init__(self):
        super(FView,self).__init__()
        self.move(0,0)
        self.resize(1380,720)
        self.setWindowTitle("colorshow")
        sc = FScene()#mat=(10,10),size=40,interv=0)#QtWidgets.QGraphicsScene()#moScene()
        self.setScene(sc)

        widget = QtOpenGL.QGLWidget(QtOpenGL.QGLFormat(QtOpenGL.QGL.SampleBuffers|QtOpenGL.QGL.Rgba))
        widget.makeCurrent()
        self.setViewport(widget)

        self.setViewportUpdateMode(QtWidgets.QGraphicsView.FullViewportUpdate);
        self.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.setAlignment(QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)


    def keyPressEvent(self,event):
        #if self.scene().focusItem() is None:
        self.dispatchKey(event)
        super(FView,self).keyPressEvent(event)

    def dispatchKey(self,event):
        if event.key()==QtCore.Qt.Key_Q:
            sys.exit()
        #if event.key()==QtCore.Qt.Key_1:
        #    #pass
        #    self.scene().pic1.setVisible(False)
        #    self.scene().pic2.setVisible(True)
        #if event.key()==QtCore.Qt.Key_2:
        #    #pass
        #    self.scene().pic2.setVisible(False)
        #    self.scene().pic1.setVisible(True)
        #if event.key()==QtCore.Qt.Key_S:
        #    if self.scene().pic1.isVisible():
        #        self.scene().makeImage(self.scene().im2)
        #    if self.scene().pic2.isVisible():
        #        self.scene().makeImage(self.scene().imm)
            #pass

if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    v   = FView()
    v.show()

    sys.exit(app.exec_())
