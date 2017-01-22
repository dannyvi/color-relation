#!/usr/local/bin/python3.4
#-*-coding:utf-8-*-

from PyQt5 import QtCore,QtGui,QtWidgets
import sys,os
qApp = None
def create_qApp():
    global qApp

    if qApp is None:
        #if DEBUG:
        #    print("Starting up QApplication")
        app = QtWidgets.QApplication.instance()
        if app is None:
            # check for DISPLAY env variable on X11 build of Qt
            if hasattr(QtGui, "QX11Info"):
                display = os.environ.get('DISPLAY')
                if display is None: #or not re.search(':\d', display):
                    raise RuntimeError('Invalid DISPLAY variable')

            qApp = QtWidgets.QApplication([str(" ")])
            qApp.lastWindowClosed.connect(qApp.quit)
        else:
            qApp = app

def exe_qApp():
    global qApp
    qApp.exec_()
