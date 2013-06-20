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

        self.__column_width_list = []

    def setColumnsWidth(self, columns_list):
        """ Sets column width.
        @param value: width
        @type value: int
        """
        self.__column_width_list = list(columns_list.split(','))
        self.setColumnCount(len(self.__column_width_list))
        for i in range(0, len(columns_list)):
            self.setColumnWidth(i, int(self.__column_width_list[i]))


    def getColumnsWidth(self):
        n_str = ",".join(map(str, self.__column_width_list))
        return QtCore.QString(n_str)


    setWidths = QtCore.pyqtProperty("QString", fget=getColumnsWidth, fset=setColumnsWidth)

