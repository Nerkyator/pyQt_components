from PyQt4 import QtCore, QtGui
from PyQt4.QtGui import QRadioButton, QFont

from improved_components_resources import components_resources


class CLightBlueRadio(QRadioButton):
    '''
    classdocs
    '''
    styleSheet = """
QRadioButton::indicator::checked{
height:40px;
width:40px;
    border-image: url(:/images/radiobuttons/radio_on_1.png);
}

QRadioButton::indicator::unchecked{
height:40px;
width:40px;
    border-image: url(:/images/radiobuttons/radio_off_1.png);
}
    """
    def __init__(self, parent=None):
        '''
        Constructor
        '''
        QRadioButton.__init__(self, parent)
        self.setStyleSheet(self.styleSheet)
        font = QFont( "Arial", 18)
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