#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Improved QLabel:

- Blinking
- Fading in\out
- Scrolling (left)
- Move to position (and come back to original one)

"""

__author__ = "lory"

from PyQt4 import QtCore, QtGui
from PyQt4.QtGui import QLabel, QGraphicsOpacityEffect
from PyQt4.QtCore import QPropertyAnimation, QEasingCurve, QString, QTimer, QRect, QPoint

from enum import Enum


class CImprovedLabel(QLabel):
    def __init__(self, parent=None, caption=None):
        QLabel.__init__(self, parent)
        self.setText(self.accessibleName())
        self.setFont(QtGui.QFont("Arial", 12))
        self.__separator = chr(004)   #Used as separator while scrolling text

        #BLINK
        self.__blink_timer = QTimer(parent)
        self.__blink_timer.timeout.connect(self.__on_blink_timer)
        self.__blink_timer_interval = 1000

        #FADING
        self.__opacity_effect = QGraphicsOpacityEffect()
        self.__fading_timer = QTimer(parent)
        self.__fading_timer.timeout.connect(self.__on_fading_timer)
        self.__FADE_TYPE = Enum("IN", "OUT")
        self.__fade_time = 20
        self.__opacity = 1.0
        self.__opacity_fading_coefficient = 0.02
        self.__selected_fade_type = self.__FADE_TYPE.IN

        #SCROLLING
        self.__scrolling_timer = QTimer(parent)
        self.__scrolling_timer.timeout.connect(self.__on_scrolling_timer)
        self.__scroll_time = 1000
        self.__original_text = ""

        #MOVE
        self.__move_animation_type = QEasingCurve.Linear
        self.__move_time = 350



    ## FUNZIONI PER BLINK
    def __on_blink_timer(self):
        self.setVisible(not (self.isVisible()))

    def setBlinking(self, blink):
        """ Sets if the label have to blink or not.
        @param blink: blinking or not
        @type blink: bool
        """
        if blink:
            self.__blink_timer.setInterval(self.__blink_timer_interval)
            self.__blink_timer.start()
        else:
            self.__blink_timer.stop()
            self.setVisible(True)

    def setBlinkInterval(self, value):
        """ Sets blink interval.
        @param value: blink interval (msec)
        @type value: int
        """
        self.__blink_timer_interval = value

    def getBlinkInterval(self):
        return self.__blink_timer_interval

    blinkInterval = QtCore.pyqtProperty("int", getBlinkInterval, setBlinkInterval)

    ##FUNZIONI PER FADING
    def fadeIn(self):
        """
         Labels fades in from completely invisible to completely visible.
        """
        self.__opacity = 0.0
        self.__selected_fade_type = self.__FADE_TYPE.IN
        self.__fading_timer.start(self.__fade_time)

    def fadeOut(self):
        """
         Labels fades out from completely visible to completely invisible.
        """
        self.__selected_fade_type = self.__FADE_TYPE.OUT
        self.__fading_timer.start(self.__fade_time)

    def setFadeTime(self, value):
        """ Sets fading time. Everytime interval is reached, alpha is increased (or decreased) by __opacity_fading_coefficient.
        @param value: fade time (msec)
        @type value: int
        """
        self.__fade_time = value

    def getFadeTime(self):
        return self.__fade_time

    fadeInterval = QtCore.pyqtProperty("int", getFadeTime, setFadeTime)

    def setFadeCoefficient(self, value):
        """ Sets fading coefficient. Alpha is increased (or decreased) by this value.
        @param value: coefficient (min 0.0 - max 1.0)
        @type value: float
        """
        self.__opacity_fading_coefficient = value

    def getFadeCoefficient(self):
        return self.__opacity_fading_coefficient

    fadeCoefficient = QtCore.pyqtProperty("double", getFadeCoefficient, setFadeCoefficient)

    def __on_fading_timer(self):
        if self.__selected_fade_type == self.__FADE_TYPE.OUT:
            if self.__opacity > 0:
                self.__opacity -= self.__opacity_fading_coefficient
                self.__opacity_effect.setOpacity(self.__opacity)
                self.setGraphicsEffect(self.__opacity_effect)
            else:
                self.__fading_timer.stop()

        if self.__selected_fade_type == self.__FADE_TYPE.IN:
            if self.__opacity <= 1.0:
                self.__opacity += self.__opacity_fading_coefficient
                self.__opacity_effect.setOpacity(self.__opacity)
                self.setGraphicsEffect(self.__opacity_effect)
            else:
                self.__fading_timer.stop()

    #FUNZIONI PER SCROLLING
    def __move_text_left(self):
        if self.__separator not in self.text():
            self.setText(self.text() + "    " + self.__separator + "    ")
        left = str(self.text())[:1]
        right = str(self.text())[1:]
        self.setText(right + left)

    def __on_scrolling_timer(self):
        self.__move_text_left()

    def scrollingText(self, scroll):
        """ Sets if the label have to scroll or not.
        @param scroll: scrolling right to left or not
        @type scroll: bool
        """
        self.__scrolling_timer.setInterval(self.__scroll_time)
        if scroll:
            self.__original_text = self.text()
            self.__scrolling_timer.start()
        else:
            self.__scrolling_timer.stop()
            self.setText(self.__original_text)

    def setScrollingTime(self, value):
        """ Sets scrolling time. Everytime interval is reached, string is scrolled to left by one char.
        @param value: scrolling time (msec)
        @type value: int
        """
        self.__scroll_time = value

    ## FUNZIONI PER SPOSTAMENTO VERSO PUNTO (ANIMATO)
    def setMoveAnimationType(self, animation_type):
        """ Sets move animation type.
        @param animation_type: animation type
        @type animation_type: QtEasingCurve
        """
        self.__move_animation_type = animation_type

    def getMoveAnimationType(self):
        return self.__move_animation_type


    #asd = QtCore.pyqtProperty("QEasingCurve", getMoveAnimationType, setMoveAnimationType)
    #sembra nn essere supportato per ora (06/05/2013)

    def setMoveTime(self, value):
        """ Sets animation moving time.
        @param value: animation time (duration) (msec)
        @type value: int
        """
        self.__move_time = value

    def moveTo(self, x, y):
        """ Move itself to a given point with the given animation in the given duration.
        @param x: X point coordinate
        @type x: int
        @param y: Y point coordinate
        @type y: int
        """
        self.__starting_position = QPoint(self.pos())
        self.__moveAnimation = QPropertyAnimation(self, "pos", self)
        self.__moveAnimation.setDuration(self.__move_time)
        self.__moveAnimation.setEasingCurve(self.__move_animation_type)
        self.__moveAnimation.setStartValue(self.__starting_position)
        self.__moveAnimation.setEndValue(QPoint(x, y))
        self.__moveAnimation.start()

    def returnToOriginalPoint(self):
        """ Label returns to its original position. The original position is stored when calling moveTo() method.
        """
        self.__moveAnimation = QPropertyAnimation(self, "pos", self)
        self.__moveAnimation.setDuration(self.__move_time)
        self.__moveAnimation.setEasingCurve(self.__move_animation_type)
        self.__moveAnimation.setStartValue(QPoint(self.pos().x(), self.pos().y()))
        self.__moveAnimation.setEndValue(self.__starting_position)
        self.__moveAnimation.start()

    def mousePressEvent(self, event):
        self.clicked.emit()