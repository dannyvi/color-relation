#!/usr/local/bin/python3.4
#-*-coding:utf-8-*-

from PyQt5 import QtCore,QtGui,QtWidgets
import numpy as np
import sys,os
from PIL import Image
from sImga import fromimage
from colorindex import sjch2rgb



class ImgScene(QtWidgets.QGraphicsScene):
    def __init__(self):
        super(ImgScene,self).__init__()
        self.setSceneRect(0,0,200,200)
        button = QtWidgets.QPushButton("打开")
        button.setFixedHeight(30)
        button.setFixedWidth(60)
        proxybutton = self.addWidget(button)
        proxybutton.setPos(0,0)
        button.pressed.connect(self.loadFile)

    def loadFile(self):
        self.openfile = QtWidgets.QFileDialog()
        self.openfile.setAcceptMode(QtWidgets.QFileDialog.AcceptOpen)
        self.openfile.setFileMode(QtWidgets.QFileDialog.ExistingFile)
        self.openfile.accepted.connect(self.loadFileAccepted)
        self.openfile.show()

    def loadFileAccepted(self):
        self.openfilename = self.openfile.selectedFiles()[0]
        #try:
        if 1:
            pic = Image.open(self.openfilename)
            img = fromimage(pic)
            img.jch[:,0]=50.0
            rgb = sjch2rgb(img.jch).reshape(img.shape)
            pic2 = Image.fromarray(rgb)
            pic2.show()
        #except:
        #    print("somethingwrong")
            #pass


class ImgView(QtWidgets.QGraphicsView):
    def __init__(self):
        super(ImgView,self).__init__()
        self.move(20,20)
        self.resize(200,200)

        self.setMinimumSize(200,200)
        self.setWindowTitle("Image analyze")
        a = ImgScene()
        self.setScene(a)


if __name__=="__main__":

    app = QtWidgets.QApplication(sys.argv)
    v = ImgView()
    v.show()
    sys.exit(app.exec_())
