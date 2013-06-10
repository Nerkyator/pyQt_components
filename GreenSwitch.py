# -*- coding: utf-8 -*-
'''
Created on 04/mag/2013

@author: Lory
'''
from PyQt4 import QtCore, QtGui
from PyQt4.QtGui import QSlider, QMouseEvent
from PyQt4.QtCore import QPropertyAnimation, QEasingCurve

from improved_components_resources import components_resources


class CGreenSwitch(QSlider):
    '''
    classdocs
    '''
    styleKnob   =   'QSlider::handle:horizontal {border-image: url(:/images/switches/white_round_knob_3.png); border: 0px solid; width: 32px; margin-left: 3px; margin-bottom: 3px; margin-top: 2px;}'
    styleBkgOFF =   'QSlider::groove:horizontal {border: 1px solid #999999; height: 35px; border-image: url(:/images/switches/off_red_1.png); margin: 1px;};'
    styleBkgON  =   'QSlider::groove:horizontal {border: 1px solid #999999; height: 35px; border-image: url(:/images/switches/on_green_1.png); margin: 1px;};'
    
    clicked = QtCore.pyqtSignal()
    animationOk = QtCore.pyqtSignal()

    def __init__(self, parent=None):
        '''
        Constructor
        '''
        QSlider.__init__(self, parent)
        self.setOrientation(QtCore.Qt.Horizontal)
        self.setAccessibleName("Maiale grosso")
        self.animationType = QEasingCurve.OutExpo
        self.animation = QPropertyAnimation(self, "value")
        self.animation.setDuration(250)
        self.animation.finished.connect(self.animationDone)
        self.resize(85, 50)
        self.clicked.connect(self.changeValue)
        self.setStyleSheet(self.styleKnob + self.styleBkgOFF)
        
    def changeValue(self):
        """Slot utilizzato per cambiare lo stato e la grafica del check."""
        self.animation.setEasingCurve(self.animationType)
        if self.value() == self.maximum():
            self.animation.setStartValue(self.maximum())
            self.animation.setEndValue(self.minimum())
            self.animation.start()
            self.setStyleSheet(self.styleKnob + self.styleBkgOFF)
            return
        else:
            self.animation.setStartValue(self.minimum())
            self.animation.setEndValue(self.maximum())
            self.setStyleSheet(self.styleKnob + self.styleBkgON)
        self.animation.start()
        
    @QtCore.pyqtSignature("setAtMax()")
    def setAtMax(self):
        if self.value() == self.minimum():
            self.animation.setEasingCurve(self.animationType)
            self.animation.setStartValue(self.minimum())
            self.animation.setEndValue(self.maximum())
            self.animation.start()
            self.setStyleSheet(self.styleKnob + self.styleBkgON)
            
    @QtCore.pyqtSignature("setAtMin()")        
    def setAtMin(self):
        if self.value() == self.maximum():
            self.animation.setEasingCurve(self.animationType)
            self.animation.setStartValue(self.maximum())
            self.animation.setEndValue(self.minimum())
            self.animation.start()
            self.setStyleSheet(self.styleKnob + self.styleBkgOFF)
        
    def mousePressEvent(self, event):
        self.clicked.emit()
        
    def isChecked(self):
        return (self.value() == self.maximum())
    
    def wheelEvent(self, event):
        # è uno switch 1\0, quindi devo disabilitare la rotellina del mouse prima che lo slider faccia il lavoro per cui è stato creato..
        return
    
    def animationDone(self):
        self.animationOk.emit()