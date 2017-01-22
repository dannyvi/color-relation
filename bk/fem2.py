#!/usr/local/bin/python3.4
#-*-coding:utf-8-*-

from PyQt5 import QtCore,QtWidgets,QtGui,QtOpenGL
from dimension.npcolorconvert import npjch2rgb
import numpy as np
from femmasop import Ocword,Ocseq,colorSeq,placeSeq

class expandItem(QtWidgets.QGraphicsItem):
    def __init__(self,color_seq,place_seq,unit,mat,size,argstring):
        super(expandItem,self).__init__()
        self.rgb_seq = npjch2rgb(color_seq)
        self.place_seq = place_seq
        self.unit = unit
        self.mat = mat
        self.size = size
        self.arg_string = argstring
        self.setPos(0,0)
        self.setFlag(QtWidgets.QGraphicsItem.ItemIsMovable)
        #self.rgb_seq = npjch2rgb(self.color_seq)

    def boundingRect(self):
        return QtCore.QRectF(0,0,self.size*self.unit[0]*self.mat[0],\
                             self.size*self.unit[1]*self.mat[1])

    def paint(self,painter,option,widget):
        self.drawpix(painter)

    def drawpix(self,painter):
        painter.setPen(QtCore.Qt.NoPen)
        def pa(rgbseq,placeseq):
            def sp(r,g,b,x,y):
                painter.setBrush(QtGui.QBrush(QtGui.QColor(r,g,b,255)))
                painter.drawRect(x,y,self.size,self.size)
                return
            rr,gg,bb = rgbseq[:,0],rgbseq[:,1],rgbseq[:,2]
            xx,yy = placeseq[:,0],placeseq[:,1]
            return np.frompyfunc(sp,5,1).__call__(rr,gg,bb,xx,yy)
        pa(self.rgb_seq,self.place_seq*self.size)

    def makeImage(self):
        pixmap = QtGui.QPixmap(QtCore.QSize(self.size*self.unit[0]*self.mat[0],\
                                            self.size*self.unit[1]*self.mat[1]))
        painter = QtGui.QPainter(pixmap)
        painter.setRenderHint(QtGui.QPainter.Antialiasing)

        self.drawpix(painter)
        painter.end()
        directory = "/Users/yudan/Documents/mypicworks/form2/test"  #.png")
        f = open("/Users/yudan/Documents/mypicworks/form2/n.num","r")
        num = str(int(f.readline())+1)
        name = directory+num+".png"
        f.close()
        f = open("/Users/yudan/Documents/mypicworks/form2/n.num","w")
        f.write(num)
        f.close()
        pixmap.save(name)
        f2 = open("/Users/yudan/Documents/mypicworks/form2/log","a")
        f2.write(self.arg_string)
        f2.write(name)
        f2.write('\n')
        f2.close()
        print('mode_A make Image')

class infoItem(QtWidgets.QGraphicsItem):
    def __init__(self,cols,color_seq,place_seq,unit,mat,size,index,argstring):
        super(infoItem,self).__init__()
        self.oc_seq    = color_seq.origin
        self.color_seq = cols#color_seq.getJCH() #getScaledJCH([10,50,270],10)
        self.textA_seq = color_seq.getBiasJCH(20,0,0)
        self.textB_seq = color_seq.getBiasJCH(50,0,0)
        self.textC_seq = color_seq.getBiasJCH(20,50,0)
        self.textD_seq = color_seq.getBiasJCH(20,50,180)
        self.rgb_seq = npjch2rgb(self.color_seq)
        self.tA_seq  = npjch2rgb(self.textA_seq)
        self.tB_seq  = npjch2rgb(self.textB_seq)
        self.tC_seq  = npjch2rgb(self.textC_seq)
        self.tD_seq  = npjch2rgb(self.textD_seq)
        self.place_seq = place_seq
        self.unit      = unit
        self.mat       = mat
        self.size      = size
        self.index     = index
        self.t_asans   = self.oc_seq.asans()
        self.arg_string = argstring
        self.setPos(0,0)
        #self.rgb_seq   = npjch2rgb(self.color_seq)
#   def setSize(self,size):
#        self.size = size
    def boundingRect(self):
        return QtCore.QRectF(0,0,self.size*self.unit[0]*4,\
                             self.size*self.unit[1]*2)

    def paint(self,painter,option,widget):
        self.drawpix(painter)

    def drawpix(self,painter):
        in0 = self.unit[0]*self.unit[1]*self.index
        in1 = self.unit[0]*self.unit[1]*(self.index+1)
        for i in range(self.unit[0]*self.unit[1]):
            c = self.rgb_seq[in0+i,:]
            for j in range(4):
                painter.setPen(QtCore.Qt.NoPen)
                painter.setBrush(QtGui.QBrush(QtGui.QColor(c[0],c[1],c[2],255)))
                painter.drawRect(self.place_seq[in0+i,0]*self.size+\
                                 self.size*(self.unit[0]+0.2)*j,\
                                 self.place_seq[in0+i,1]*self.size,\
                                 self.size,self.size)
                painter.drawRect(i%self.unit[0]*self.size+\
                                 self.size*(self.unit[0]+0.2)*j,\
                                 i//self.unit[1]*self.size +\
                                 self.size*(self.unit[1]+0.2),\
                                 self.size,self.size)
                #for k in range(4):
                if j==1:
                    font = QtGui.QFont()
                    font.setPointSize(self.size//4)
                    painter.setFont(font)
                    painter.setBrush(QtCore.Qt.NoBrush)
                    c1 = self.tA_seq[in0+i]
                    p = QtGui.QPen(QtGui.QColor(c1[0],c1[1],c1[2],255))
                    painter.setPen(p)
                    painter.drawText((self.place_seq[in0+i,0]+\
                                      (self.unit[0]+0.2)*j)*self.size,\
                                     self.place_seq[in0+i,1]*self.size,\
                                     self.size/2,self.size/2,\
                                     QtCore.Qt.AlignHCenter,\
                                     self.t_asans[in0+i,0])
                    painter.drawText((i%self.unit[0]+\
                                      (self.unit[0]+0.2)*j)*self.size,\
                                     (i//self.unit[1]+self.unit[1]+0.2)*self.size,\
                                     self.size/2,self.size/2,\
                                     QtCore.Qt.AlignHCenter,\
                                     self.t_asans[in0+i,0])
                    c1 = self.tB_seq[in0+i]
                    p = QtGui.QPen(QtGui.QColor(c1[0],c1[1],c1[2],255))
                    painter.setPen(p)
                    painter.drawText((self.place_seq[in0+i,0]+0.5+\
                                      (self.unit[0]+0.2)*j)*self.size,\
                                     self.place_seq[in0+i,1]*self.size,\
                                     self.size/2,self.size/2,\
                                     QtCore.Qt.AlignHCenter,\
                                     self.t_asans[in0+i,1])
                    painter.drawText((i%self.unit[0]+\
                                      (self.unit[0]+0.7)*j)*self.size,\
                                     (i//self.unit[1]+self.unit[1]+0.2)*self.size,\
                                     self.size/2,self.size/2,\
                                     QtCore.Qt.AlignHCenter,\
                                     self.t_asans[in0+i,1])
                    c1 = self.tC_seq[in0+i]
                    p = QtGui.QPen(QtGui.QColor(c1[0],c1[1],c1[2],255))
                    painter.setPen(p)
                    painter.drawText((self.place_seq[in0+i,0]+\
                                      (self.unit[0]+0.2)*j)*self.size,\
                                     (self.place_seq[in0+i,1]+0.5)*self.size,\
                                     self.size/2,self.size/2,\
                                     QtCore.Qt.AlignHCenter,\
                                     self.t_asans[in0+i,2])
                    painter.drawText((i%self.unit[0]+\
                                      (self.unit[0]+0.2)*j)*self.size,\
                                     (i//self.unit[1]+self.unit[1]+0.7)*self.size,\
                                     self.size/2,self.size/2,\
                                     QtCore.Qt.AlignHCenter,\
                                     self.t_asans[in0+i,2])
                    c1 = self.tD_seq[in0+i]
                    p = QtGui.QPen(QtGui.QColor(c1[0],c1[1],c1[2],255))
                    painter.setPen(p)
                    painter.drawText((self.place_seq[in0+i,0]+0.5+\
                                      (self.unit[0]+0.2)*j)*self.size,\
                                     (self.place_seq[in0+i,1]+0.5)*self.size,\
                                     self.size/2,self.size/2,\
                                     QtCore.Qt.AlignHCenter,\
                                     self.t_asans[in0+i,3])
                    painter.drawText((i%self.unit[0]+\
                                      (self.unit[0]+0.7)*j)*self.size,\
                                     (i//self.unit[1]+self.unit[1]+0.7)*self.size,\
                                     self.size/2,self.size/2,\
                                     QtCore.Qt.AlignHCenter,\
                                     self.t_asans[in0+i,3])

                if j==2:
                    font = QtGui.QFont()
                    font.setPointSize(self.size//5)
                    painter.setFont(font)
                    painter.setBrush(QtCore.Qt.NoBrush)
                    c1 = self.tB_seq[in0+i]
                    p = QtGui.QPen(QtGui.QColor(c1[0],c1[1],c1[2],255))
                    painter.setPen(p)
                    painter.drawText((self.place_seq[in0+i,0]+0.5+\
                                      (self.unit[0]+0.2)*j)*self.size,\
                                     self.place_seq[in0+i,1]*self.size,\
                                     self.size/2,self.size/2,\
                                     QtCore.Qt.AlignHCenter,\
                                     str(int(self.color_seq[in0+i,0])) )
                    painter.drawText((i%self.unit[0]+0.5+\
                                      (self.unit[0]+0.2)*j)*self.size,\
                                     (i//self.unit[1]+self.unit[1]+0.2)*self.size,\
                                     self.size/2,self.size/2,\
                                     QtCore.Qt.AlignHCenter,\
                                     str(int(self.color_seq[in0+i,0])) )
                                     #self.t_asans[in0+i,1])
                    c1 = self.tC_seq[in0+i]
                    p = QtGui.QPen(QtGui.QColor(c1[0],c1[1],c1[2],255))
                    painter.setPen(p)
                    painter.drawText((self.place_seq[in0+i,0]+\
                                      (self.unit[0]+0.2)*j)*self.size,\
                                     (self.place_seq[in0+i,1]+0.5)*self.size,\
                                     self.size/2,self.size/2,\
                                     QtCore.Qt.AlignHCenter,\
                                     #self.t_asans[in0+i,2])
                                     str(int(self.color_seq[in0+i,1])) )
                    painter.drawText((i%self.unit[0]+\
                                      (self.unit[0]+0.2)*j)*self.size,\
                                     (i//self.unit[1]+self.unit[1]+0.7)*self.size,\
                                     self.size/2,self.size/2,\
                                     QtCore.Qt.AlignHCenter,\
                                     #self.t_asans[in0+i,2])
                                     str(int(self.color_seq[in0+i,1])) )
                    c1 = self.tD_seq[in0+i]
                    p = QtGui.QPen(QtGui.QColor(c1[0],c1[1],c1[2],255))
                    painter.setPen(p)
                    painter.drawText((self.place_seq[in0+i,0]+0.5+\
                                      (self.unit[0]+0.2)*j)*self.size,\
                                     (self.place_seq[in0+i,1]+0.5)*self.size,\
                                     self.size/2,self.size/2,\
                                     QtCore.Qt.AlignHCenter,\
                                     #self.t_asans[in0+i,3])
                                     str(int(self.color_seq[in0+i,2])) )
                    painter.drawText((i%self.unit[0]+0.5+\
                                      (self.unit[0]+0.2)*j)*self.size,\
                                     (i//self.unit[1]+self.unit[1]+0.7)*self.size,\
                                     self.size/2,self.size/2,\
                                     QtCore.Qt.AlignHCenter,\
                                     #self.t_asans[in0+i,3])
                                     str(int(self.color_seq[in0+i,2])) )

                if j==3:
                    font = QtGui.QFont()
                    font.setPointSize(self.size//4)
                    painter.setFont(font)
                    painter.setBrush(QtCore.Qt.NoBrush)
                    c1 = self.tB_seq[in0+i]
                    p = QtGui.QPen(QtGui.QColor(c1[0],c1[1],c1[2],255))
                    painter.setPen(p)
                    painter.drawText((self.place_seq[in0+i,0]+0.5+\
                                      (self.unit[0]+0.2)*j)*self.size,\
                                     self.place_seq[in0+i,1]*self.size,\
                                     self.size/2,self.size/2,\
                                     QtCore.Qt.AlignHCenter,\
                                     str(i) )
                    painter.drawText((i%self.unit[0]+0.5+\
                                      (self.unit[0]+0.2)*j)*self.size,\
                                     (i//self.unit[1]+self.unit[1]+0.2)*self.size,\
                                     self.size/2,self.size/2,\
                                     QtCore.Qt.AlignHCenter,\
                                     str(i) )
                                     #self.t_asans[in0+i,1])

    def makeImage(self):
        pixmap = QtGui.QPixmap(QtCore.QSize(self.size*self.unit[0]*4.1,\
                                            self.size*self.unit[1]*2.1))
        painter = QtGui.QPainter(pixmap)
        painter.setRenderHint(QtGui.QPainter.Antialiasing)

        self.drawpix(painter)
        painter.end()
        directory = "/Users/yudan/Documents/mypicworks/form2/test"  #.png")
        f = open("/Users/yudan/Documents/mypicworks/form2/n.num","r")
        num = str(int(f.readline())+1)
        name = directory+num+".png"
        f.close()
        f = open("/Users/yudan/Documents/mypicworks/form2/n.num","w")
        f.write(num)
        f.close()
        pixmap.save(name)
        f2 = open("/Users/yudan/Documents/mypicworks/form2/log","a")
        f2.write(self.arg_string)
        f2.write(name)
        f2.write('\n')
        print('mode_B make Image')




class OcScene(QtWidgets.QGraphicsScene):
    def __init__(self,seed=Ocword(),unit=(3,3),mat=(4,4),interv=0,size=40):
        super(OcScene,self).__init__()
        self.setBackgroundBrush(QtCore.Qt.black)
        self.oc_seed = Ocword(seed)#[[2,2],[1,3],[4,6],[7,9]])#Ocword(seed)
        #self.oc_seed = Ocword([[0,0],[4,8],[7,7],[9,11]])#Ocword(seed)
        self.unit_square = unit
        self.unit_mat    = mat
        self.unit_size   =size
        self.u_interv    = interv
        carry = [0,10,12,60]
        m = np.random.randint
        self.oc_seq_genmethod = [[m(0,10),carry[m(0,4)]],\
                                 [m(0,10),carry[m(0,4)]],\
                                 [m(0,10),carry[m(0,4)]],\
                                 [m(0,10),carry[m(0,4)]]]
        #self.oc_seq_genmethod = [[0,60],[1,60],[1,60],[1,0]]

        #self.c_seq_fr    =      [2,0,2]
        self.c_seq_fr    =      [m(0,3),\
                                 m(0,3),\
                                 m(0,3)]
        self.c_seq_t1    =      [3,60,61,0]
        self.c_seq_t2    =      [3,60,61,1/12]
        self.c_seq_t3    =      [3,60,61,1/9]
        #self.c_seq_inscale=     [1,1,1]
        self.c_seq_inscale=     [np.random.randint(0,10),\
                                 np.random.randint(0,10),\
                                 np.random.randint(0,10)]

        self.area_arg =[[[20,26],[40,45],[55,60]],\
                        [[165,170],[196,207],[280,285]],\
                        [[50,90]]]
        #[[[40,50],[60,70]],[[160,170],[200,210]],[[0,20],[50,70]]]
        #[[[10,30],[35,60],[70,80]],
                        # [[0,10],[90,110]],
                        # [[0,30],[60,90]]]

        self.place_ver = 1

        jch_info = ["天干法","地支法","甲子法"]
        self.oc_seq = Ocseq(self.oc_seed,\
                            unit[0]*unit[1]*mat[0]*mat[1],\
                            self.oc_seq_genmethod)
        self.color_seq = colorSeq(self.oc_seq,self.c_seq_fr,self.c_seq_t1,\
                                  self.c_seq_t2,self.c_seq_t3,self.c_seq_inscale)
        self.place_seq = placeSeq(self.oc_seq)

        self.color_method = self.color_seq.getAreaJCH

        self.arg_string = "\n种子:\n"+self.oc_seed.__repr__()+\
                          "队列生成法:"+str(self.oc_seq_genmethod)+"\n"+\
                          "色彩参数：\n" + "明度:" +jch_info[self.c_seq_fr[0]]+"\n"+\
                          "纯度:" + jch_info[self.c_seq_fr[1]] + "\n" +\
                          "色相:" + jch_info[self.c_seq_fr[2]] + "\n" +\
                          str(self.c_seq_t1)+\
                          str(self.c_seq_t2)+str(self.c_seq_t3)+"\n"+\
                          "间距:"+str(self.c_seq_inscale)+"\n"+\
                          "取色法:"+repr(self.color_method)+"\n"+\
                          "队形参数:" + "\n"+\
                          "方阵大小:"+str(self.unit_square) + \
                          "矩阵个数:"+str(self.unit_mat)+\
                          "\nver:"+\
                          str(self.place_ver)+"\n"

        #c_li = self.color_method()
        c_li = self.color_method(self.area_arg[0],\
                                 self.area_arg[1],\
                                 self.area_arg[2])
        #self.color_seq.getJCH()
        #self.color_seq.getAreaJCH(self.area_arg[0],\
        #                                 self.area_arg[1],\
        #                                 self.area_arg[2])

        self.modeA_item = expandItem(c_li,\
            #self.color_seq.getAreaJCH(self.area_arg[0],\
                                     #                          self.area_arg[1],\
                                     #                          self.area_arg[2]),\
                                     #getJCH(),\
                                     #getScaledJCH([10,50,270],10),\
                                     self.place_seq.genQueue(\
                                        uleng=self.unit_square[0],\
                                         ver=self.place_ver,\
                                         mat=self.unit_mat,\
                                         interv=self.u_interv),\
                                     self.unit_square,\
                                     self.unit_mat,\
                                     self.unit_size,\
                                     self.arg_string)
        self.addItem(self.modeA_item)
        self.modeA_item.setPos(0,0)
        self.modeB_item = infoItem(c_li,\
                                   self.color_seq,\
                                   self.place_seq.genQueue(\
                                       uleng=self.unit_square[0],\
                                       ver=self.place_ver,\
                                                           mat=self.unit_mat,\
                                                           interv=self.u_interv),\
                                   self.unit_square,\
                                   self.unit_mat,
                                   self.unit_size,
                                   0,self.arg_string)
        self.addItem(self.modeB_item)
        self.modeB_item.setPos(0,0)
        self.modeB_item.setVisible(False)
   # def __init__(self,color_seq,place_seq,unit,mat,size,index):

   # def sceneRect(self):
   #     if self.mode1_item.isVisible():
   #         return QtCore.QRectF(0,0,self.size*self.unit[0]*self.mat[0],\
   #                              self.size*self.unit[1]*self.mat[1])
        #    return QtCore.QRectF(0,0,self.size*self.unit[0]*4,\
        #                         self.size*self.unit[1]*2)
            #return
    def setSeed(self,oc):
        self.oc_seed = Ocword(oc)

    def setUnit(self,unit):
        self.unit_square = unit

    def setMat(self,mat):
        self.unit_mat = mat

    def setSeqMethod(self,method):
        self.oc_seq_genmethod = method

    def setSize(self,size):
        self.unit_size = size



class OcView(QtWidgets.QGraphicsView):
    def __init__(self):
        super(OcView,self).__init__()
        self.move(0,0)
        self.resize(1380,720)
        self.setWindowTitle("colorshow")
        sc = OcScene()#mat=(10,10),size=40,interv=0)#QtWidgets.QGraphicsScene()#moScene()
        self.setScene(sc)

        widget = QtOpenGL.QGLWidget(QtOpenGL.QGLFormat(QtOpenGL.QGL.SampleBuffers|QtOpenGL.QGL.Rgba))
        widget.makeCurrent()
        self.setViewport(widget)

        self.setViewportUpdateMode(QtWidgets.QGraphicsView.FullViewportUpdate);
        self.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.setAlignment(QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)


    def keyPressEvent(self,event):
        if self.scene().focusItem() is None:
            self.dispatchKey(event)
        super(OcView,self).keyPressEvent(event)

    def dispatchKey(self,event):
        if event.key()==QtCore.Qt.Key_Q:
            sys.exit()
        if event.key()==QtCore.Qt.Key_1:
            self.scene().modeB_item.setVisible(False)
            self.scene().modeA_item.setVisible(True)
            #self.mapFromScene(QtCore.QPoint(0,0))#translate(0,0)
        if event.key()==QtCore.Qt.Key_2:
            self.scene().modeA_item.setVisible(False)
            self.scene().modeB_item.setVisible(True)
            #self.scene().setSceneRect(0,0,10,10)
            #self.setTransform(self.transform().reset())
            #self.mapFromScene(QtCore.QPoint(0,0))#translate(0,0)
            #self.scroll(10,30)
        if event.key()==QtCore.Qt.Key_S:
            if self.scene().modeB_item.isVisible():
                self.scene().modeB_item.makeImage()
            if self.scene().modeA_item.isVisible():
                self.scene().modeA_item.makeImage()

if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    v   = OcView()
    v.show()

    sys.exit(app.exec_())
