#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Plugin QT Designer per ImprovedLabel.py
"""


from PyQt4 import QtGui, QtDesigner
from PyQt4.QtDesigner import QPyDesignerCustomWidgetPlugin

from ImprovedLineEdit import CImprovedLineEdit

__all__ = ['CImprovedLineEdit']

class ImprovedLabel_plugin(QPyDesignerCustomWidgetPlugin):

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
        return CImprovedLineEdit(parent)

    def name(self):
        return "CImprovedLineEdit"

    def toolTip(self):
        return "--"

    def whatsThis(self):
        return "--"

    def includeFile(self):
        return "ImprovedLineEdit"

    def group(self):
        return "Improved Components"

    def isContainer(self):
        return False

    def domXml(self):
        return ("""
            <ui language="c++">
                <widget class="CImprovedLineEdit" name="ImprovedLineEdit">
                    <property name="toolTip">
                        <string>{0}</string>
                    </property>
                    <property name="whatsThis">
                        <string>{1}</string>
                    </property>
                    <property name="text">
                        <string>Improved LineEdit</string>
                    </property>
                </widget>
                <customwidgets>
                    <customwidget>
                        <class>CImprovedLineEdit</class>
                        <extends>QLineEdit</extends>
                    </customwidget>
               </customwidgets>
            </ui>""".format(self.toolTip(), self.whatsThis())
        )
        