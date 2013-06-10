#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = "J3G\lleasi"
__svnid__ = "$Id: ImprovedButton_plugin.py 3165 2011-03-23 13:47:48Z gcorbelli $"
__revision__ = "$Revision: 3165 $"

from PyQt4 import QtGui, QtDesigner
from PyQt4.QtDesigner import QPyDesignerCustomWidgetPlugin
from PyQt4.QtGui import QIcon, QPixmap
from PyQt4.QtCore import QSize

from ImprovedButton import CImprovedButton

__all__ = [ 'CImprovedButton_plugin' ]

class CImprovedButton_plugin(QPyDesignerCustomWidgetPlugin):

    def __init__(self, parent=None):
        QPyDesignerCustomWidgetPlugin.__init__(self)
        self.initialized = False

    def initialize(self, QDesignerFormEditorInterface):
        if self.initialized:
            return
        self.initialized = True

    def isInitialized(self):
        return self.initialized

    def createWidget(self, parent):
        return CImprovedButton(parent)

    def name(self):
        return "CImprovedButton"

    def toolTip(self):
        return "Pulsante animato"

    def whatsThis(self):
        return "Pulsante animato"

    def includeFile(self):
        return "ImprovedButton"

    def group(self):
        return "Improved Components"

    def icon(self):
        return QIcon(':/images/desingerIcons/improved_button.png')

    def isContainer(self):
        return False

    def domXml(self):
        return ("""
            <ui language="c++">
                <widget class="CImprovedButton" name="ImprovedButton">
                    <property name="toolTip">
                        <string>{0}</string>
                    </property>
                    <property name="whatsThis">
                        <string>{1}</string>
                    </property>
                    <property name="geometry">
                        <rect>
                            <x>0</x>
                            <y>0</y>
                            <width>140</width>
                            <height>95</height>
                        </rect>
                    </property>
                </widget>
                <customwidgets>
                    <customwidget>
                        <class>CImprovedButton</class>
                        <extends>QToolButton</extends>
                    </customwidget>
               </customwidgets>
            </ui>""".format(self.toolTip(), self.whatsThis())
        )
