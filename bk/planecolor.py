#!/usr/local/bin/python3.4
#-*-coding:utf-8-*-

from PyQt5 import QtCore,QtWidgets,QtGui
from recolor import recColors
#from cons64 import constructMagie2,constructMagie
from dimension.npcolorconvert import npjch2rgb
#from femmascolor2 import femmas
import numpy as np

class planeBlock(QtWidgets.QGraphicsItem):
    def __init__(self,color=[0,0,0],size=20,parent=None):
        super(planeBlock,self).__init__(parent)
        self.color=color
        self.size= size
        self.setFlag(QtWidgets.QGraphicsItem.ItemIsMovable)

    def boundingRect(self):
        return QtCore.QRectF(0,0,self.size,self.size)

    def paint(self,painter,option,widget):
        painter.setPen(QtCore.Qt.NoPen)
        c = QtGui.QColor(self.color[0],self.color[1],self.color[2],255)
        painter.setBrush(QtGui.QBrush(c))
        path = QtGui.QPainterPath()
        path.addRect(0,0,self.size,self.size)
        painter.drawPath(path)

    def setColor(self,color):
        self.color = color

    def setSize(self,size):
        self.size = size

class planeScene(QtWidgets.QGraphicsScene):
    def __init__(self):
        super(planeScene,self).__init__()
        self.setBackgroundBrush(QtCore.Qt.gray)

    def arrangeBlock(self,size):
        #a = femmas([[0,0],[0,0],[0,0],[0,0]],[[0,0],[0,0],[0,0],[0,0]])
        ra = np.random.randint
        s = recColors(center=[ra(0,100),ra(0,100),ra(0,360)],\
                      rule = [[ra(0,100),ra(0,100),ra(0,360)],\
                              [ra(0,100),ra(0,100),ra(0,360)],\
                              [ra(0,100),ra(0,100),ra(0,360)],\
                              [ra(0,100),ra(0,100),ra(0,360)]],\
                      scale = np.random.random(),time=3)
        #a.linColor(64)
        #s2 = constructMagie(8,2)
        #print(s)
        J = s[:,0]
        C = s[:,1]
        H = s[:,2]

        colorrgb = npjch2rgb(np.array([J,C,H]).T)
        print(colorrgb)
        #print(colorrgb)
        pos_list = [[1,1],[6,3],[3,6],[8,8],[6,7],[1,5],[8,4],[3,2],\
                    [6,5],[1,7],[8,2],[3,4],[1,3],[6,1],[3,8],[8,6],\
                    [7,6],[4,8],[5,1],[2,3],[4,4],[7,2],[2,7],[5,5],\
                    [4,2],[7,4],[2,5],[5,7],[7,8],[4,6],[5,3],[2,1],\
                    [5,6],[2,8],[7,1],[4,3],[2,4],[5,2],[4,7],[7,5],\
                    [2,2],[5,4],[4,5],[7,7],[5,8],[2,6],[7,3],[4,1],\
                    [3,1],[8,3],[1,6],[6,8],[8,7],[3,5],[6,4],[1,2],\
                    [8,5],[3,7],[6,2],[1,4],[3,3],[8,1],[1,8],[6,6]]
        #block_list = []
        #size = 10
        #s2 = constructMagie2(8,2)
        #a2 = #femmas([[0,0],[0,0],[0,2],[0,0]],[[0,0],[0,0],[0,0],[0,0]])
        #s2 = recColors()#a2.linColor(64)
        s2 = s
        #recColors(center=[ra(0,100),ra(0,100),ra(0,360)],\
             #         rule = [[ra(0,100),ra(0,100),ra(0,360)],\
             #                 [ra(0,100),ra(0,100),ra(0,360)],\
             #                 [ra(0,100),ra(0,100),ra(0,360)],\
             #                 [ra(0,100),ra(0,100),ra(0,360)]],\
             #         scale = np.random.random(),time=3)
        #s2 = constructMagie(8,2)
        #print(s)
        J2 = s2[:,0]
        C2 = s2[:,1]
        H2 = s2[:,2]

        colorrgb2 = npjch2rgb(np.array([J2,C2,H2]).T)
        for i in range(len(colorrgb)):
            block = planeBlock(colorrgb[i],size)
            self.addItem(block)
            block.setPos(20+pos_list[i][0]*size,20+pos_list[i][1]*size)
            block2 = planeBlock(colorrgb2[i],size)
            self.addItem(block2)
            block2.setPos(20+10*size+i%8*size,20+size+i//8*size)
            #if i<32:
            #    block.setPos(20+i*size,size)
            #else:
            #    block.setPos(20+31*size-(i-32)*size,size*2)

class planeView(QtWidgets.QGraphicsView):
    def __init__(self):
        super(planeView,self).__init__()
        self.move(20,20)
        self.resize(1100,650)
        self.setMinimumSize(1100,650)
        self.setWindowTitle("color planes")
        sc = planeScene()#QtWidgets.QGraphicsScene()#moScene()
        sc.arrangeBlock(50)
        #block = planeBlock([12,45,255])
        #sc.addItem(block)
        #block.setPos(20,20)
        self.setScene(sc)
        self.scene().setSceneRect(0,0,2100,1650)
        #widget = QtOpenGL.QGLWidget(QtOpenGL.QGLFormat(QtOpenGL.QGL.SampleBuffers|QtOpenGL.QGL.Rgba))
        #widget.makeCurrent()
        #self.setViewport(widget)
        self.setViewportUpdateMode(QtWidgets.QGraphicsView.FullViewportUpdate);
        #self.setFrameStyle(QtWidgets.QFrame.NoFrame)
        self.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        #self.setViewportUpdateMode(QtWidgets.QGraphicsView.FullViewportUpdate)
        #self.setTransformationAnchor(QtWidgets.QGraphicsView.AnchorUnderMouse)
        #self.setResizeAnchor(QtWidgets.QGraphicsView.AnchorViewCenter)

    def keyPressEvent(self,event):
        if self.scene().focusItem() is None:
            self.dispatchKey(event)
        super(planeView,self).keyPressEvent(event)

    def dispatchKey(self,event):
        if event.key()==QtCore.Qt.Key_Q:
            sys.exit()


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    v   = planeView()
    v.show()

    sys.exit(app.exec_())
