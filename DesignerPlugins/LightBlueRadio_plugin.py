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

from LightBlueRadio import CLightBlueRadio

__all__ = [ 'CLightBlueRadio_plugin' ]

class CLightBlueRadio_plugin(QPyDesignerCustomWidgetPlugin):
    
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
        return CLightBlueRadio(parent)
    
    def name(self):
        return "CLightBlueRadio"
    
    def toolTip(self):
        return "Eyecandy light blue Radio"
    
    def whatsThis(self):
        return "Eyecandy light blue Radio"
    
    def includeFile(self):
        return "LightBlueRadio"
    
    def group(self):
        return "Improved Components"

    def icon(self):
        return QIcon(':/images/desingerIcons/light_blue_radio.png')
    
    def isContainer(self):
        return False
    
    def domXml(self):
        return ("""
            <ui language="c++">
                <widget class="CLightBlueRadio" name="Light Blue Radio">
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
                        <class>CLightBlueRadio</class>
                        <extends>QRadioButton</extends>
                    </customwidget>
               </customwidgets>
            </ui>""".format(self.toolTip(), self.whatsThis())
        )
