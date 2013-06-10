#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" Plugin QT Designer per CImprovedStackWidget
"""

import sys

from PyQt4 import QtGui, QtDesigner
from PyQt4.QtDesigner import QPyDesignerCustomWidgetPlugin

from ImprovedStackWidget import CImprovedStackWidget

__all__ = [ 'CImprovedStackWidget_plugin' ]

class CImprovedStackWidget_plugin(QPyDesignerCustomWidgetPlugin):

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
        return CImprovedStackWidget(parent)

    def name(self):
        return "CImprovedStackWidget"

    def toolTip(self):
        return "Animated sliding panel"

    def whatsThis(self):
        return "Animated sliding panel"

    def includeFile(self):
        return "ImprovedStackWidget"

    def group(self):
        return "Improved Components"

    def isContainer(self):
        return True

    def domXml(self):
        return ("""
            <ui language="c++">
                <widget class="CImprovedStackWidget" name="SlidingPanel">
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
                            <width>500</width>
                            <height>200</height>
                        </rect>
                    </property>
                    <property name="minimumSize">
                        <rect>
                            <width>500</width>
                            <height>500</height>
                        </rect>
                    </property>
                    <property name="styleSheet">
                        <string>background-color: rgb(184, 184, 184);</string>
                    </property>
                </widget>
                <customwidgets>
                    <customwidget>
                        <class>CImprovedStackWidget</class>
                        <extends>QStackedWidget</extends>
                    </customwidget>
               </customwidgets>
            </ui>""".format(self.toolTip(), self.whatsThis())
        )
