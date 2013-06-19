#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Plugin QT Designer per ImprovedLabel.py
"""


from PyQt4 import QtGui, QtDesigner
from PyQt4.QtDesigner import QPyDesignerCustomWidgetPlugin

from ImprovedTableWidget import CImprovedTableWidget

__all__ = ['CImprovedTableWidget']

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
        return CImprovedTableWidget(parent)

    def name(self):
        return "CImprovedTableWidget"

    def toolTip(self):
        return "--"

    def whatsThis(self):
        return "--"

    def includeFile(self):
        return "ImprovedTableWidget"

    def group(self):
        return "Improved Components"

    def isContainer(self):
        return False

    def domXml(self):
        return ("""
            <ui language="c++">
                <widget class="CImprovedTableWidget" name="ImprovedTableWidget">
                    <property name="toolTip">
                        <string>{0}</string>
                    </property>
                    <property name="whatsThis">
                        <string>{1}</string>
                    </property>
                    <property name="text">
                        <string>Improved TableWidget</string>
                    </property>
                </widget>
                <customwidgets>
                    <customwidget>
                        <class>CImprovedTableWidget</class>
                        <extends>QTableWidget</extends>
                    </customwidget>
               </customwidgets>
            </ui>""".format(self.toolTip(), self.whatsThis())
        )
        