#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Improved QFrame:

- Fading in\out
- Move to position (and come back to original one)
- Hides in 4 directions
- Resize to position (and come back to original one)
- Fold in 2 directions (QT limit of resizing)
- PixmapMask
- Shadow Effect

"""

__author__ = "lory"

from PyQt4 import QtCore, QtGui
from PyQt4.QtGui import QFrame, QGraphicsOpacityEffect, QBitmap, QPixmap, QGraphicsDropShadowEffect, QGraphicsEffect, QColor
from PyQt4.QtCore import QPropertyAnimation, QEasingCurve, QString, QTimer, QRect, QPoint

from enum import Enum


class CImprovedPanel(QFrame):
    def __init__(self, parent=None):
        QFrame.__init__(self, parent)

        #FADING
        self.__opacity_effect = QGraphicsOpacityEffect()
        self.__fading_timer = QTimer(parent)
        self.__fading_timer.timeout.connect(self.__on_fading_timer)
        self.__FADE_TYPE = Enum("IN", "OUT")
        self.__fade_time = 20
        self.__opacity = 1.0
        self.__opacity_fading_coefficient = 0.02
        self.__selected_fade_type = self.__FADE_TYPE.IN
        self.resizeEvent = self.__onResize

        #MOVE
        self.__move_animation_type = QEasingCurve.Linear
        self.__move_time = 350
        self.__is_moving = False

        #RESIZE
        self.__resize_animation_type = QEasingCurve.Linear
        self.__resize_time = 700
        self.__is_resizing = False

        #PIXMAP & MASCHERA
        self.__pmap = QPixmap(self.size())
        self.__pmap_fname = ""
        self.__show_mask_preview = False

        #SHADOW
        self.__shadow_Xoffset = 3.0 #default value
        self.__shadow_Yoffset = 3.0 #default value
        self.__shadow_blur_radius = 8.0 #default value
        self.__shadow_color = QColor(38,38,38,150) #default value

        self.__shadow_effect = QGraphicsDropShadowEffect()
        self.__shadow_effect.setXOffset(self.__shadow_Xoffset)
        self.__shadow_effect.setYOffset(self.__shadow_Yoffset)
        self.__shadow_effect.setBlurRadius(self.__shadow_blur_radius)
        self.__shadow_effect.setColor(self.__shadow_color)
        self._shadow_visible = False


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

    def getMoveTime(self):
        return self.__move_time

    moveTime = QtCore.pyqtProperty("int", getMoveTime, setMoveTime)

    def setResizeTime(self, value):
        """ Sets animation resize time.
        @param value: animation time (duration) (msec)
        @type value: int
        """
        self.__resize_time = value

    def getResizeTime(self):
        return self.__resize_time

    resizeTime = QtCore.pyqtProperty("int", getResizeTime, setResizeTime)

    def moveTo(self, x, y):
        """ Move itself to a given point with the given animation in the given duration.
        @param x: X point coordinate
        @type x: int
        @param y: Y point coordinate
        @type y: int
        """
        if self.__is_moving:
            return
        self.__is_moving = True
        self.__starting_position = QPoint(self.pos())
        self.__moveAnimation = QPropertyAnimation(self, "pos", self)
        self.__moveAnimation.finished.connect(self.__on_finished_moving)
        self.__moveAnimation.setDuration(self.__move_time)
        self.__moveAnimation.setEasingCurve(self.__move_animation_type)
        self.__moveAnimation.setStartValue(self.__starting_position)
        self.__moveAnimation.setEndValue(QPoint(x, y))
        self.__moveAnimation.start()


    def hideLeft(self):
        """ Panel hides sliding on the left. The slide amount is equal to his width - 5px.
        """
        dest_x = self.geometry().x() - self.width() - 5
        dest_y = self.geometry().y()
        self.moveTo(dest_x, dest_y)

    def showFromLeft(self):
        """ Panel shows sliding from the left. The slide amount is equal to his width + 5px.
        """
        dest_x = self.geometry().x() + self.width() + 5
        dest_y = self.geometry().y()
        self.moveTo(dest_x, dest_y)

    def hideRight(self):
        """ Panel hides sliding on the right. The slide amount is equal to his width - 5px.
        """
        dest_x = self.geometry().x() + self.width() + 5
        dest_y = self.geometry().y()
        self.moveTo(dest_x, dest_y)

    def showFromRight(self):
        """ Panel shows sliding from the right. The slide amount is equal to his width + 5px.
        """
        dest_x = self.geometry().x() - self.width() - 5
        dest_y = self.geometry().y()
        self.moveTo(dest_x, dest_y)

    def hideTop(self):
        """ Panel hides sliding on the top. The slide amount is equal to his height - 5px.
        """
        dest_x = self.geometry().x()
        dest_y = self.geometry().y() - self.height() - 5
        self.moveTo(dest_x, dest_y)

    def showFromTop(self):
        """ Panel hides sliding from the top. The slide amount is equal to his height - 5px.
        """
        dest_x = self.geometry().x()
        dest_y = self.geometry().y() + self.height() + 5
        self.moveTo(dest_x, dest_y)

    def hideBottom(self):
        """ Panel hides sliding to the bottom. The slide amount is equal to his height - 5px.
        """
        dest_x = self.geometry().x()
        dest_y = self.geometry().y() + self.height() + 5
        self.moveTo(dest_x, dest_y)

    def showFromBottom(self):
        """ Panel hides sliding from the bottom. The slide amount is equal to his height - 5px.
        """
        dest_x = self.geometry().x()
        dest_y = self.geometry().y() - self.height() - 5
        self.moveTo(dest_x, dest_y)

    def returnToOriginalPoint(self):
        """ Panel returns in its original position. The original position is stored when calling moveTo() method.
        """
        if self.__is_moving:
            return
        self.__is_moving = True
        self.__moveAnimation = QPropertyAnimation(self, "pos", self)
        self.__moveAnimation.finished.connect(self.__on_finished_moving)
        self.__moveAnimation.setDuration(self.__move_time)
        self.__moveAnimation.setEasingCurve(self.__move_animation_type)
        self.__moveAnimation.setStartValue(QPoint(self.pos().x(), self.pos().y()))
        self.__moveAnimation.setEndValue(self.__starting_position)
        self.__moveAnimation.start()

    #FUNZIONI PER RIDIMENSIONAMENTO
    def setResizeAnimationType(self, animation_type):
        """ Sets move animation type.
        @param animation_type: animation type
        @type animation_type: QtEasingCurve
        """
        self.__resize_animation_type = animation_type

    def resizeTo(self, width, height):
        """ Resize itself to a given size with the given animation in the given duration.
        @param width: New width
        @type width: int
        @param height: New height
        @type height: int
        """
        if self.__is_resizing:
            return
        self.__is_resizing = True
        self.__original_size = self.geometry()
        self.__resizeAnimation = QPropertyAnimation(self, "geometry", self)
        self.__resizeAnimation.finished.connect(self.__on_finished_resizing)
        self.__resizeAnimation.setDuration(self.__resize_time)
        self.__resizeAnimation.setEasingCurve(self.__resize_animation_type)
        self.__resizeAnimation.setStartValue(self.__original_size)
        self.__resizeAnimation.setEndValue(QRect(self.pos().x(), self.pos().y(), width, height))
        self.__resizeAnimation.start()

    def foldLeft(self):
        """ Panel hides folding to the left.
        """
        new_width = 0
        new_height = self.height()
        self.resizeTo(new_width, new_height)

    def unfoldLeft(self):
        """ Panel shows folding from the left.
        """
        new_width = self.__original_size.width()
        new_height = self.height()
        self.resizeTo(new_width, new_height)

    def foldTop(self):
        """ Panel hides folding to the top.
        """
        new_width = self.width()
        new_height = 0
        self.resizeTo(new_width, new_height)

    def unfoldTop(self):
        """ Panel shows folding from the top.
        """
        new_width = self.width()
        new_height = self.__original_size.height()
        self.resizeTo(new_width, new_height)

    #FUNZIONI PER PIXMAP & MASCHERA
    def setPixmapFile(self, image_file):
        self.__pmap = image_file
        self.__pmap.scaled(self.size())
        #NB: Il pixmap deve essere BIANCO e NERO. Con heuristicMask il primo pixel in alto a sinistra (0,0) viene
        #usato per decidere il colore trasparente, tutto il resto è visibile.

    def getPixmapFile(self):
        return self.__pmap

    pixmapFile = QtCore.pyqtProperty("QPixmap", getPixmapFile, setPixmapFile)


    def applyMask(self, bool):
        self.__show_mask_preview = bool
        if bool:
            self.setMask(QBitmap(self.__pmap.createHeuristicMask().scaled(self.size())))
        else:
            self.setMask(QBitmap())

    def getMask(self):
        return self.__show_mask_preview

    appliedMask = QtCore.pyqtProperty("bool", fget=getMask, fset=applyMask)

    def __on_finished_moving(self):
        self.__is_moving = False

    def __on_finished_resizing(self):
        self.__is_resizing = False

    def __onResize(self, event):
        self.__pmap.scaled(self.size())
        if self.__show_mask_preview:
            self.setMask(QBitmap(self.__pmap.createHeuristicMask().scaled(self.size())))

        #FUNZIONI PER SHADOW

    def getShadow(self):
        return self._shadow_visible

    def setShadow(self, bool):
        self.setGraphicsEffect(self.__shadow_effect)
        self._shadow_visible = bool
        self.__shadow_effect.setEnabled(bool)

    shadow = QtCore.pyqtProperty("bool", fget=getShadow, fset=setShadow)

    def setShadowXOffset(self, value):
        """ Sets shadow offset on X.
        @param value: offset
        @type value: float
        """
        self.__shadow_Xoffset = value
        self.__shadow_effect.setXOffset(self.__shadow_Xoffset)

    def getShadowXOffset(self):
        return self.__shadow_Xoffset

    shadowXOffset = QtCore.pyqtProperty("double", getShadowXOffset, setShadowXOffset)

    def setShadowYOffset(self, value):
        """ Sets shadow offset on Y.
        @param value: offset
        @type value: float
        """
        self.__shadow_Yoffset = value
        self.__shadow_effect.setYOffset(self.__shadow_Yoffset)

    def getShadowYOffset(self):
        return self.__shadow_Yoffset

    shadowYOffset = QtCore.pyqtProperty("double", getShadowYOffset, setShadowYOffset)


    def setShadowBlur(self, value):
        """ Sets blurred effect on item's shadow.
        @param value: coefficient
        @type value: float
        """
        self.__shadow_blur_radius = value
        self.__shadow_effect.setBlurRadius(self.__shadow_blur_radius)

    def getShadowBlur(self):
        return self.__shadow_blur_radius


    shadowBlur = QtCore.pyqtProperty("double", getShadowBlur, setShadowBlur)


    def setShadowColor(self, color):
        """ Sets shadow's color.
        @param color: value
        @type color: color
        """
        self.__shadow_color = color
        self.__shadow_effect.setColor(self.__shadow_color)

    def getShadowColor(self):
        return self.__shadow_color

        #shadowColor = QtCore.pyqtProperty("color", getShadowColor, setShadowColor)


