#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys

from PyQt4 import QtCore, QtGui, uic
from PyQt4.QtCore import QEasingCurve
from PyQt4.QtGui import QToolButton, QPixmap, QBitmap

import res

import ImprovedButton

def main():
    app = QtGui.QApplication(sys.argv)
    w = CMainWindow()
    w.show()
    return app.exec_()
        
class CMainWindow(QtGui.QMainWindow):
        def __init__(self, parent=None):
            QtGui.QMainWindow.__init__(self, parent)
            self.ui = uic.loadUi("main_win.ui", self)
            self.app = QtGui.QApplication.instance()

            self.ui.toolButton.clicked.connect(self.btn_pressed)
            self.ui.toolButton_2.clicked.connect(self.btn2_pressed)

            self.ImprovedPanel.setResizeAnimationType(QEasingCurve.OutBounce)

        def btn_pressed(self):
            self.ui.ImprovedButton.startBounce()

        def btn2_pressed(self):
            self.ui.ImprovedButton.stopBounce()
            
            
if __name__ == "__main__":
     sys.exit(main())
