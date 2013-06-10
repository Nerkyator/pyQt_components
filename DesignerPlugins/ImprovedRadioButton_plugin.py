#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" Plugin QT Designer per ImprovedRadioButton_plugin.py
"""

from PyQt4 import QtGui, QtDesigner
from PyQt4.QtDesigner import QPyDesignerCustomWidgetPlugin
from PyQt4.QtGui import QIcon

from ImprovedRadioButton import CImprovedRadioButton

__all__ = [ 'CImprovedRadioButton_plugin' ]

class CImprovedRadioButton_plugin(QPyDesignerCustomWidgetPlugin):

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
        return CImprovedRadioButton(parent)

    def name(self):
        return "CImprovedRadioButton"

    def toolTip(self):
        return "Improved Radio Button"

    def whatsThis(self):
        return "Improved Radio Button"

    def includeFile(self):
        return "ImprovedRadioButton"

    def group(self):
        return "Improved Components"

    def isContainer(self):
        return False

    def domXml(self):
        return ("""
            <ui language="c++">
                <widget class="CImprovedRadioButton" name="Improved Radio Button">
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
                            <width>210</width>
                            <height>40</height>
                        </rect>
                    </property>
                </widget>
                <customwidgets>
                    <customwidget>
                        <class>CImprovedRadioButton</class>
                        <extends>QRadioButton</extends>
                    </customwidget>
               </customwidgets>
            </ui>""".format(self.toolTip(), self.whatsThis())
        )
