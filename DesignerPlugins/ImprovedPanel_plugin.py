#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = "J3G\lleasi"
__svnid__ = "$Id: ImprovedPanel_plugin.py 3165 2011-03-23 13:47:48Z gcorbelli $"
__revision__ = "$Revision: 3165 $"

from PyQt4 import QtGui, QtDesigner
from PyQt4.QtDesigner import QPyDesignerCustomWidgetPlugin
from PyQt4.QtGui import QIcon, QPixmap
from PyQt4.QtCore import QSize

from ImprovedPanel import CImprovedPanel

__all__ = [ 'CImprovedPanel_plugin' ]

class CImprovedPanel_plugin(QPyDesignerCustomWidgetPlugin):

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
        return CImprovedPanel(parent)

    def name(self):
        return "CImprovedPanel"

    def toolTip(self):
        return "Pannello animato"

    def whatsThis(self):
        return "Pannello animato"

    def includeFile(self):
        return "ImprovedPanel"

    def group(self):
        return "Improved Components"

    def icon(self):
        return QIcon()

    def isContainer(self):
        return True

    def domXml(self):
        return ("""
            <ui language="c++">
                <widget class="CImprovedPanel" name="ImprovedPanel">
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
                        <class>CImprovedPanel</class>
                        <extends>QFrame</extends>
                    </customwidget>
               </customwidgets>
            </ui>""".format(self.toolTip(), self.whatsThis())
        )
