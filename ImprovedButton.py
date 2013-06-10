# -*- coding: utf-8 -*-
__author__ = 'lory'

from PyQt4 import QtCore, QtGui
from PyQt4.QtGui import QToolButton, QLabel, QIcon, QFont, QGraphicsOpacityEffect, QPixmap, QBitmap
from PyQt4.QtCore import QPropertyAnimation, QEasingCurve, QString, QTimer, QRect, QPoint, QSize

from enum import Enum
from improved_components_resources import components_resources

"""
Improved QToolButton:

- Blinking
- Fading in\out
- Grow\shrink
- Bounce
- PixmapMask
- iOS style indicator

"""


class CImprovedButton(QToolButton):
    def __init__(self, parent=None):
        QToolButton.__init__(self, parent)

        #TESTO ALTERNATIVO
        #Spesso se il pulsante ha icona troppo grossa e quando per ragioni di spazio o altro non si può spostare
        #o ridimensionare il pulsante stesso, la label ha posizioni assurde e schifose. Aggiungerne una "+ controllabile"
        #è l'unico modo..
        self.__fixed_label = QLabel("alternative label", self)
        self.__fixed_label.move(0, self.geometry().height() - 35)
        self.__fixed_label.resize(self.geometry().width(), self.__fixed_label.geometry().height())
        self.__fixed_label.setAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)
        self.__font = QtGui.QFont("Arial", 10)
        self.__fixed_label.setFont(self.__font)
        self.__fixed_label.show()

        #INDICATORE STILE iOS
        self.__indicator = QLabel("0", self)
        self.__indicator.setStyleSheet("border-image: url(':/images/backgrounds/indicator.png'); padding-right:1px; color: white;")
        self.__indicator.geometry().setWidth(25)
        self.__indicator.geometry().setHeight(20)
        self.__indicator.setAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)
        self.__indicator.setVisible(False)
        self.setIndicatorPos(QPoint(self.width() - self.__indicator.width(), 0)) #default top-right corner
        #Quando il pulsante viene ridimensionato (designer o meno) devo anche sistemare la label di conseguenza
        self.resizeEvent = self.__onResize
        self.__indicator.resizeEvent = self.__on_indicator_Resize

        self.setToolButtonStyle(QtCore.Qt.ToolButtonIconOnly)

        self.clicked.connect(self.stopAllAnimations)

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

        # ANIMAZIONI GROW
        self.__animationGrow = QPropertyAnimation(self, "iconSize", self)
        self.__animationGrow.setDuration(1000)
        self.__animationGrow.setEasingCurve(QEasingCurve.Linear)
        self.__animationGrow.finished.connect(self.__on_growed)

        self.__animationShrink = QPropertyAnimation(self, "iconSize", self)
        self.__animationShrink.setDuration(1000)
        self.__animationShrink.setEasingCurve(QEasingCurve.Linear)
        self.__animationShrink.finished.connect(self.__on_shrinked)

        self.__defaultIconDimension = 60
        self.__iconGrowsBy = 40
        self.__growing = False

        # ANIMAZIONI BOUNCE
        self.__animationUp = QPropertyAnimation(self, "pos", self)
        self.__animationUp.setDuration(200)
        self.__animationUp.setEasingCurve(QEasingCurve.Linear)
        self.__animationUp.finished.connect(self.__on_top_reached)

        self.__animationBounce = QPropertyAnimation(self, "pos", self)
        self.__animationBounce.setDuration(1000)
        self.__animationBounce.setEasingCurve(QEasingCurve.OutBounce)
        self.__animationBounce.finished.connect(self.__on_bounce_finished)

        self.__bouncing = False
        self.__startPos = QPoint(self.pos().x(), self.pos().y())

        #PIXMAP & MASCHERA
        self.__pmap = QPixmap(self.size())
        self.__pmap_fname = ""
        self.__show_mask_preview = False

    def setDefaultIconSize(self, value):
        """ Sets default icon size when growing stops.
        @param value: size (both width and height)
        @type value: int
        """
        self.__defaultIconDimension = value

    def getDefaultIconSize(self):
        return self.__defaultIconDimension

    defaultIconSize = QtCore.pyqtProperty("int", getDefaultIconSize, setDefaultIconSize)

    def setFixetTextVisibility(self, bool):
        """ Sets if fixed text is visible or not.
        @param bool: visible or not
        @type bool: bool
        """
        self.__fixed_label.setVisible(bool)

    def getFixetTextVisibility(self):
        return self.__fixed_label.isVisible()

    fixetTextVisibility = QtCore.pyqtProperty("bool", fget=getFixetTextVisibility, fset=setFixetTextVisibility)

    def setFixedText(self, txt):
        """ Sets text on the button.
        @param txt: text
        @type txt: string
        """
        self.__fixed_label.setText(txt)

    def getFixedText(self):
        return self.__fixed_label.text()

    fixedText = QtCore.pyqtProperty("QString", getFixedText, setFixedText)

    def setFixedTextPos(self, qpoint):
        """ Sets text position in the button.
        @param qpoint: Position RELATIVE. 0,0 is top left corner of the button.
        @type qpoint: QPoint
        """
        self.__fixed_label.move(qpoint)

    def getFixedTextPos(self):
        return self.__fixed_label.pos()

    fixedTextPos = QtCore.pyqtProperty("QPoint", getFixedTextPos, setFixedTextPos)

    def setFixedTextFont(self, font):
        """ Sets text font.
        @param font: Font for fixed text.
        @type font: QFont
        """
        self.__font = font
        self.__fixed_label.setFont(self.__font)

    def getFixedTextFont(self):
        return self.__font

    fixedTextFont = QtCore.pyqtProperty("QFont", getFixedTextFont, setFixedTextFont)

    #FUNZIONI INDICATORE
    def setIndicatorVisibility(self, bool):
        """ Sets if indicator is visible or not.
        @param bool: visible or not
        @type bool: bool
        """
        self.__indicator.setVisible(bool)

    def getIndicatorVisibility(self):
        return self.__indicator.isVisible()

    indicatorVisibility = QtCore.pyqtProperty("bool", fget=getIndicatorVisibility, fset=setIndicatorVisibility)

    def setIndicatorPos(self, qpoint):
        """ Sets indicator position in the button.
        @param qpoint: Position RELATIVE. 0,0 is top left corner of the button.
        @type qpoint: QPoint
        """
        self.__indicator.move(qpoint)

    def getIndicatorPos(self):
        return self.__indicator.pos()

    indicatorPos = QtCore.pyqtProperty("QPoint", getIndicatorPos, setIndicatorPos)

    def setIndicatorSize(self, size):
        """ Sets indicator size.
        @param size: Size
        @type size: QSize
        """
        self.__indicator.resize(size)

    def getIndicatorSize(self):
        return self.__indicator.size()

    indicatorSize = QtCore.pyqtProperty("QSize", getIndicatorSize, setIndicatorSize)

    def setIndicatorFont(self, font):
        """ Sets indicator text font.
        @param font: Font for indicator text.
        @type font: QFont
        """
        self.__indicator.setFont(font)

    def getIndicatorFont(self):
        return self.__indicator.font()

    indicatorFont = QtCore.pyqtProperty("QFont", getIndicatorFont, setIndicatorFont)


    ## FUNZIONI PER BLINK
    def __on_blink_timer(self):
        self.setVisible(not (self.isVisible()))

    def setBlinking(self, blink):
        """ Sets if the button have to blink or not.
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
        @param blink: blink interval (msec)
        @type blink: int
        """
        self.__blink_timer_interval = value

    def getBlinkInterval(self):
        return self.__blink_timer_interval

    blinkInterval = QtCore.pyqtProperty("int", getBlinkInterval, setBlinkInterval)


    ##FUNZIONI PER FADING
    def fadeIn(self):
        """
         Button fades in from completely invisible to completely visible.
        """
        self.__opacity = 0.0
        self.__selected_fade_type = self.__FADE_TYPE.IN
        self.__fading_timer.start(self.__fade_time)

    def fadeOut(self):
        """
         Button fades out from completely visible to completely invisible.
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

    # FUNZIONI PER GROW\SHRINK
    def __on_growed(self):
        self.__animationShrink.setStartValue(QSize(self.iconSize().width(), self.iconSize().height()))
        self.__animationShrink.setEndValue(
            QSize(self.iconSize().width() - self.__iconGrowsBy, self.iconSize().height() - self.__iconGrowsBy))
        self.__animationShrink.start()

    def __on_shrinked(self):
        self.__animationGrow.setStartValue(QSize(self.iconSize().width(), self.iconSize().height()))
        self.__animationGrow.setEndValue(
            QSize(self.iconSize().width() + self.__iconGrowsBy, self.iconSize().height() + self.__iconGrowsBy))
        self.__animationGrow.start()

    def startGrow(self):
        """
         Button ICON starts to grow and shrink to standard value when maximum size (configured) is reached
        """
        if self.__growing:
            return
        self.__animationGrow.setStartValue(QSize(self.iconSize().width(), self.iconSize().height()))
        self.__animationGrow.setEndValue(
            QSize(self.iconSize().width() + self.__iconGrowsBy, self.iconSize().height() + self.__iconGrowsBy))
        self.__animationGrow.start()
        self.__growing = True

    def stopGrow(self):
        if self.__animationGrow.startValue().toSize() != QSize(0,
                                                               0) and self.__animationShrink.startValue().toSize() != QPoint(
                0, 0):
            self.__animationGrow.stop()
            self.__animationShrink.stop()
            self.setIconSize(QSize(self.__defaultIconDimension, self.__defaultIconDimension))
            self.__growing = False
            
    #FUNZIONI PER BOUNCE
    def startBounce(self):
        """
         Button starts to bounce requiring attention.
        """
        if self.__bouncing:
            return
        self.__startPos = QPoint(self.pos().x(), self.pos().y())
        self.__animationUp.setStartValue(QPoint(self.__startPos.x(), self.__startPos.y()))
        self.__animationUp.setEndValue(QPoint(self.__startPos.x(), self.__startPos.y() - self.geometry().height()))
        self.__animationUp.start()
        self.__bouncing = True
        
    def stopBounce(self):
        if self.__animationUp.startValue().toPoint() != QPoint(0,0) and self.__animationBounce.startValue().toPoint() != QPoint(0,0):
            self.__animationBounce.stop()
            self.__animationUp.stop()
            self.setGeometry(self.__startPos.x(), self.__startPos.y(), self.geometry().width(), self.geometry().height())
            self.__bouncing = False

    def __on_top_reached(self):
        self.__animationBounce.setStartValue(QPoint(self.pos().x(), self.pos().y()))
        self.__animationBounce.setEndValue(QPoint(self.__startPos.x(), self.__startPos.y()))
        self.__animationBounce.start()

    def __on_bounce_finished(self):
        self.__animationUp.start()

    def stopAllAnimations(self):
        self.stopBounce()
        self.stopGrow()

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

    def __onResize(self, event):
        self.__fixed_label.move(0, self.geometry().height() - 35)
        self.__fixed_label.resize(self.geometry().width(), self.__fixed_label.geometry().height())
        self.setIndicatorPos(QPoint(self.width() - self.__indicator.width(), 0))
        self.__pmap.scaled(self.size())
        if self.__show_mask_preview:
            self.setMask(QBitmap(self.__pmap.createHeuristicMask().scaled(self.size())))

    def __on_indicator_Resize(self, event):
        self.setIndicatorPos(QPoint(self.width() - self.__indicator.width(), 0))