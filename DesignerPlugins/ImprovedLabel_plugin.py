#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Plugin QT Designer per ImprovedLabel.py
"""


from PyQt4 import QtGui, QtDesigner
from PyQt4.QtDesigner import QPyDesignerCustomWidgetPlugin

from ImprovedLabel import CImprovedLabel

__all__ = ['CImprovedLabel']

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
        return CImprovedLabel(parent)

    def name(self):
        return "CImprovedLabel"

    def toolTip(self):
        return "--"

    def whatsThis(self):
        return "--"

    def includeFile(self):
        return "ImprovedLabel"

    def group(self):
        return "Improved Components"

    def isContainer(self):
        return False

    def domXml(self):
        return ("""
            <ui language="c++">
                <widget class="CImprovedLabel" name="ImprovedLabel">
                    <property name="toolTip">
                        <string>{0}</string>
                    </property>
                    <property name="whatsThis">
                        <string>{1}</string>
                    </property>
                    <property name="text">
                        <string>Improved Label</string>
                    </property>
                </widget>
                <customwidgets>
                    <customwidget>
                        <class>CImprovedLabel</class>
                        <extends>QLabel</extends>
                    </customwidget>
               </customwidgets>
            </ui>""".format(self.toolTip(), self.whatsThis())
        )
        