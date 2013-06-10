#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" Plugin QT Designer per WaspCore.Qt.GUI.SlidingCheck.CSlidingCheck
"""

__author__ = "J3G\lleasi"
__svnid__ = "$Id: SlidingCheck_plugin.py 3172 2011-03-23 13:50:56Z gcorbelli $"
__revision__ = "$Revision: 3172 $"

from PyQt4 import QtGui, QtDesigner
from PyQt4.QtDesigner import QPyDesignerCustomWidgetPlugin
from PyQt4.QtGui import QIcon

from GreenSwitch import CGreenSwitch

__all__ = [ 'CGreenSwitch_plugin' ]

class CGreenSwitch_plugin(QPyDesignerCustomWidgetPlugin):
    
    def __init__(self, parent=None):
        QPyDesignerCustomWidgetPlugin.__init__(self)
        self.setObjectName("ASD")
        self.initialized = False

    def initialize(self, QDesignerFormEditorInterface):
        if self.initialized:
            return
        self.initialized = True

    def isInitialized(self):
        return self.initialized
    
    def createWidget(self, parent):
        return CGreenSwitch(parent)
    
    def name(self):
        return "CGreenSwitch"
    
    def toolTip(self):
        return "Eyecandy green switch"
    
    def whatsThis(self):
        return "Eyecandy green switch"
    
    def includeFile(self):
        return "GreenSwitch"

    def icon(self):
        return QIcon(':/images/desingerIcons/green_switch.png')
    
    def group(self):
        return "Improved Components"
    
    def isContainer(self):
        return False
    
    def domXml(self):
        return ("""
            <ui language="c++">
                <widget class="CGreenSwitch" name="Green Switch">
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
                            <width>85</width>
                            <height>50</height>
                        </rect>
                    </property>
                    <property name="maximum">
                        <number>99</number>
                    </property>
                    <property name="minimum">
                        <number>0</number>
                    </property>
                </widget>
                <customwidgets>
                    <customwidget>
                        <class>CGreenSwitch</class>
                        <extends>QSlider</extends>
                    </customwidget>
               </customwidgets>
            </ui>""".format(self.toolTip(), self.whatsThis())
        )
