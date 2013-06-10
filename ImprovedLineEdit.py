#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Improved QLineEdit:

- Number only
- Attention needed

"""

__author__ = "lory"

from PyQt4 import QtCore, QtGui
from PyQt4.QtGui import QLineEdit, QIntValidator, QDoubleValidator

class CImprovedLineEdit(QLineEdit):
    __DEF_STYLE = """
        border-style: solid;
        border-width: 1px;
        border-radius: 5px;
        border-color: rgb(125,125,125)
    """


    __ATT_STYLE = """
        border-style: solid;
        border-width: 1px;
        border-radius: 5px;
        border-color: rgb(125,125,125);
        background-color: rgba(255, 134, 134, 150);
    """
    def __init__(self, parent=None):
        QLineEdit.__init__(self, parent)
        self.setText(self.accessibleName())
        self.setFont(QtGui.QFont("Arial", 16))
        self.setStyleSheet(self.__DEF_STYLE)

        #SOLO NUMERI
        self.__only_numbers = False

        #ERRORI PRESENTI (RICHIAMA ATTENZIONE)
        self.__need_attention = False

    def setOnlyNumbers(self, bool):
        """ Sets lineEdit to accept only digits.
        @param bool: only digits
        @type bool: bool
        """
        self.__only_numbers = bool
        if bool:
            self.setValidator(QDoubleValidator())
        else:
            self.setValidator(None)

    def getOnlyNumbers(self):
        return self.__only_numbers

    onlyNumbers = QtCore.pyqtProperty("bool", fget=getOnlyNumbers, fset=setOnlyNumbers)

    def getNeedAttention(self):
        return self.__need_attention

    def setNeedAttention(self, bool):
        """ Stylize lineEdit to have user attention.
        @param bool: attention needed
        @type bool: bool
        """
        self.__need_attention = bool
        if bool:
            self.setStyleSheet(self.__ATT_STYLE)
        else:
            self.setStyleSheet(self.__DEF_STYLE)

    needAttention = QtCore.pyqtProperty("bool", fget=getNeedAttention, fset=setNeedAttention)


