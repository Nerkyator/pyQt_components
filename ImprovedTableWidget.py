#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Improved QTableWidget:

- Colum width from Qt Designer

"""

__author__ = "lory"

from PyQt4 import QtCore, QtGui
from PyQt4.QtGui import QTableWidget

class CImprovedTableWidget(QTableWidget):
    def __init__(self, parent=None):
        QTableWidget.__init__(self, parent)

        self.__selected_colum = 0

    def __selectColumn(self, col_number):
        self.__selected_colum = col_number
        self.getSelectedColumnWidth()

    def __getSelectedColumn(self):
        return self.__selected_colum

    selectedColumn = QtCore.pyqtProperty("int", fget=__getSelectedColumn, fset=__selectColumn)

    def setSelectedColumnWidth(self, value):
        """ Sets column width.
        @param value: width
        @type value: int
        """
        self.setColumnWidth(self.__selected_colum, value)

    def getSelectedColumnWidth(self):
        return self.columnWidth(self.__selected_colum)


    setWidth = QtCore.pyqtProperty("int", fget=getSelectedColumnWidth, fset=setSelectedColumnWidth)

