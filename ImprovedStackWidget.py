#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Improved QStackedWidget:

"""

__author__ = "lory"

from PyQt4 import QtCore, QtGui
from PyQt4.QtGui import QStackedWidget
from PyQt4.QtCore import QPropertyAnimation, QEasingCurve, QString, QTimer, QRect, QPoint

from enum import Enum


class CImprovedStackWidget(QStackedWidget):
    __SLIDE_TYPE = Enum("TOP2BOTTOM",
                        "BOTTOM2TOP",
                        "RIGHT2LEFT",
                        "LEFT2RIGHT",
                        "AUTOMATIC")

    animationOk = QtCore.pyqtSignal()

    def __init__(self, parent=None):
        """ Inizializza il componente"""
        QStackedWidget.__init__(self, parent)
        self.__m_vertical=False
        self.__m_speed=500
        self.__m_animationtype = QEasingCurve.OutQuint #QEasingCurve.OutBack
        self.__m_now=0
        self.__m_next=0
        self.__m_pnow=QPoint(0,0)
        self.__m_active = False
        self.__direction = self.__SLIDE_TYPE.RIGHT2LEFT
        self.__animgroup = QtCore.QParallelAnimationGroup()
        self.__animgroup.finished.connect(self.__animationDone)
        self.__animnext = QPropertyAnimation(None, "pos")
        self.__animnow = QPropertyAnimation(None, "pos")
        #self.setMinimumSize(300, 300)
        self.setStyleSheet("background-color: rgb(184, 184, 184);")

    def setVerticalMode(self, bool):
        """ Setta la modalità slide in verticale
        @param bool: Impostata a true o false, determina se lo slide è verticale o orizzontale.
        @type bool: Boolean
        """
        self.__m_vertical = bool

    def setSpeed(self, speed_value):
        """ Setta la velocità di slide tra una pagine e l'altra.
        @param speed_value: Velocità in msec.
        @type speed_value: int
        """
        self.__m_speed = speed_value

    def getSpeed(self):
        return self.__m_speed

    slidingSpeed = QtCore.pyqtProperty("int", getSpeed, setSpeed)

    def setAnimation(self, animation_type):
        """ Setta il la tipologia di animazione da utilizzare per gli slide.
        @param animation_type: Tipo di animazione.
        @type animation_type: QEasingCurve
        """
        self.__m_animationtype = animation_type

    def slideNext(self):
        """Sposta alla finestra successiva"""
        now = self.currentIndex()
        self.slideIdx(now + 1)

    def slidePrev(self):
        """Sposta alla finestra precedente"""
        now = self.currentIndex()
        self.slideIdx(now - 1)

    def slideIdx(self, idx):
        """ Sposta la visualizzazione alla finestra indicata.
        @param idx: Indice finestra da visualizzare
        @type idx: int
        """

        if(idx > self.count()-1):
            if(self.__m_vertical):
                self.__direction = self.__SLIDE_TYPE.TOP2BOTTOM
            else:
                self.__direction = self.__SLIDE_TYPE.RIGHT2LEFT
            idx = (idx) % self.count()

        elif (idx<0):
            if(self.__m_vertical):
                self.__direction = self.__SLIDE_TYPE.BOTTOM2TOP
            else:
                self.__direction = self.__SLIDE_TYPE.LEFT2RIGHT
            idx = (idx + self.count()) % self.count()

        self.slideInWgt(self.widget(idx))

    def slideInWgt(self, widget):
        if self.__m_active:
            return    #se l'animazione e' attiva, nn faccio nulla.
        else:
            self.__m_active = True
        now = self.currentIndex()
        next = self.indexOf(widget)


        if(now==next):
            self.__m_active = False
            return
        elif(now < next):
            if(self.__m_vertical):
                dhint = self.__SLIDE_TYPE.TOP2BOTTOM
            else:
                dhint = self.__SLIDE_TYPE.RIGHT2LEFT

        else:
            if(self.__m_vertical):
                dhint = self.__SLIDE_TYPE.BOTTOM2TOP
            else:
                dhint = self.__SLIDE_TYPE.LEFT2RIGHT

        #=======================================================================
        # if(self.__direction == self.AUTOMATIC):
        #    self.__direction = dhint
        #=======================================================================
        self.__direction = dhint
        offsetX = self.frameRect().width()
        offsetY = self.frameRect().height()

        self.widget(next).setGeometry ( 0,  0, offsetX, offsetY )

        if (self.__direction==self.__SLIDE_TYPE.BOTTOM2TOP):
            offsetX=0
            offsetY=-offsetY
        elif (self.__direction==self.__SLIDE_TYPE.TOP2BOTTOM):
            offsetX=0
        elif (self.__direction==self.__SLIDE_TYPE.RIGHT2LEFT):
            offsetX=-offsetX
            offsetY=0
        elif (self.__direction==self.__SLIDE_TYPE.LEFT2RIGHT):
            offsetY=0


        pnext = self.widget(next).pos()
        pnow  = self.widget(now).pos()
        self.__m_pnow = pnow

        self.widget(next).move(pnext.x() - offsetX, pnext.y() - offsetY)
        self.widget(next).show()

        self.__animnow.setTargetObject(self.widget(now))
        self.__animnow.setDuration(self.__m_speed)
        self.__animnow.setEasingCurve(self.__m_animationtype)
        self.__animnow.setStartValue(QPoint(pnow.x(), pnow.y()))
        self.__animnow.setEndValue(QPoint(offsetX+pnow.x(), offsetY+pnow.y()))

        self.__animnext.setTargetObject(self.widget(next))
        self.__animnext.setDuration(self.__m_speed)
        self.__animnext.setEasingCurve(self.__m_animationtype)
        self.__animnext.setStartValue(QPoint(-offsetX+pnext.x(), offsetY+pnext.y()))
        self.__animnext.setEndValue(QPoint(pnext.x(), pnext.y()))

        self.__animgroup.addAnimation(self.__animnow)
        self.__animgroup.addAnimation(self.__animnext)

        self.__m_next=next
        self.__m_now=now
        self.__m_active=True
        self.__animgroup.start()

    def __animationDone(self):
        self.setCurrentIndex(self.__m_next)

        self.widget(self.__m_now).hide()

        self.widget(self.__m_now).move(self.__m_pnow)
        self.__m_active=False

        self.animationOk.emit()
