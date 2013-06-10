from PyQt4 import QtCore, QtGui
from PyQt4.QtGui import QRadioButton, QFont

"""
Improved QRadioButton:
- Int value
- Str Value
"""

class CImprovedRadioButton(QRadioButton):
    '''
    classdocs
    '''

    def __init__(self, parent=None):
        '''
        Constructor
        '''
        QRadioButton.__init__(self, parent)
        font = QFont( "Arial", 12)
        self.setFont(font)

        #VARIABILI INTERNE
        self.__intValue = 0
        self.__strValue = ""

    def setStrValue(self, txt):
        """ Sets string value of the radioButton.
        @param txt: text
        @type txt: string
        """
        self.__strValue = txt

    def getStrValue(self):
        return str(self.__strValue)

    stringValue = QtCore.pyqtProperty("QString", getStrValue, setStrValue)

    def setIntValue(self, value):
        """ Sets integer value of the radioButton.
        @param value: integer value
        @type value: int
        """
        self.__intValue = value

    def getIntValue(self):
        return self.__intValue

    intValue = QtCore.pyqtProperty("int", getIntValue, setIntValue)