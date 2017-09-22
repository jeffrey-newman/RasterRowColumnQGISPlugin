# -*- coding: utf-8 -*-
"""
/***************************************************************************
 RasterRowColumn
                                 A QGIS plugin
 Get row and column of point on raster
                              -------------------
        begin                : 2017-02-23
        git sha              : $Format:%H$
        copyright            : (C) 2017 by Jeffrey Newman
        email                : jeffrey.newman.au@gmail.com
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
"""
# from PyQt4.QtCore import QSettings, QTranslator, qVersion, QCoreApplication
# from PyQt4.QtGui import QAction, QIcon
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from qgis.core import *
from qgis.gui import *
# Initialize Qt resources from file resources.py
import resources
# Import the code for the dialog
from RasterRowColumn_dialog import RasterRowColumnDialog
import os.path



class RasterRowColumn:
    """QGIS Plugin Implementation."""

    layers = []

    def display_point(self, point, button):
        # report map coordinates from a canvas click
        coords = "{}, {}".format(point.x(), point.y())
        self.dlg.lineEdit.setText(str(coords))
        self.dlg.show()

        selectedLayerIndex = self.dlg.comboBox.currentIndex()
        selectedLayer = self.layers[selectedLayerIndex]
        # layer = self.wcb.currentLayer()

        if selectedLayer is not None:

            width = selectedLayer.width()
            height = selectedLayer.height()

            xsize = selectedLayer.rasterUnitsPerPixelX()
            ysize = selectedLayer.rasterUnitsPerPixelY()

            extent = selectedLayer.extent()

            ymax = extent.yMaximum()
            xmin = extent.xMinimum()

            #row in pixel coordinates
            row = int(((ymax - point.y()) / ysize) + 1)

            #row in pixel coordinates
            column = int(((point.x() - xmin) / xsize) + 1)

            if row <= 0 or column <=0 or row > height or column > width:
                row = "out of extent"
                column = "out of extent"

        else:
            row = "no raster"
            column = "no raster"

        self.dlg.lineEdit_2.setText(str(row))

        self.dlg.lineEdit_3.setText(str(column))

    def __init__(self, iface):
        """Constructor.

        :param iface: An interface instance that will be passed to this class
            which provides the hook by which you can manipulate the QGIS
            application at run time.
        :type iface: QgsInterface
        """
        # Save reference to the QGIS interface
        self.iface = iface
        # Save reference to the QGIS interface
        self.iface = iface
        # refernce to map canvas
        self.canvas = self.iface.mapCanvas()
        # initialize plugin directory
        self.plugin_dir = os.path.dirname(__file__)
        # initialize locale
        locale = QSettings().value('locale/userLocale')[0:2]
        locale_path = os.path.join(
            self.plugin_dir,
            'i18n',
            'RasterRowColumn_{}.qm'.format(locale))

        if os.path.exists(locale_path):
            self.translator = QTranslator()
            self.translator.load(locale_path)

            if qVersion() > '4.3.3':
                QCoreApplication.installTranslator(self.translator)


        # Declare instance attributes
        self.actions = []
        self.menu = self.tr(u'&RasterRowColumn')
        # TODO: We are going to let the user set this up in a future iteration
        self.toolbar = self.iface.addToolBar(u'RasterRowColumn')
        self.toolbar.setObjectName(u'RasterRowColumn')

        # out click tool will emit a QgsPoint on every click
        self.clickTool = QgsMapToolEmitPoint(self.iface.mapCanvas())



    # noinspection PyMethodMayBeStatic
    def tr(self, message):
        """Get the translation for a string using Qt translation API.

        We implement this ourselves since we do not inherit QObject.

        :param message: String for translation.
        :type message: str, QString

        :returns: Translated version of message.
        :rtype: QString
        """
        # noinspection PyTypeChecker,PyArgumentList,PyCallByClass
        return QCoreApplication.translate('RasterRowColumn', message)


    def add_action(
        self,
        icon_path,
        text,
        callback,
        enabled_flag=True,
        add_to_menu=True,
        add_to_toolbar=True,
        status_tip=None,
        whats_this=None,
        parent=None):
        """Add a toolbar icon to the toolbar.

        :param icon_path: Path to the icon for this action. Can be a resource
            path (e.g. ':/plugins/foo/bar.png') or a normal file system path.
        :type icon_path: str

        :param text: Text that should be shown in menu items for this action.
        :type text: str

        :param callback: Function to be called when the action is triggered.
        :type callback: function

        :param enabled_flag: A flag indicating if the action should be enabled
            by default. Defaults to True.
        :type enabled_flag: bool

        :param add_to_menu: Flag indicating whether the action should also
            be added to the menu. Defaults to True.
        :type add_to_menu: bool

        :param add_to_toolbar: Flag indicating whether the action should also
            be added to the toolbar. Defaults to True.
        :type add_to_toolbar: bool

        :param status_tip: Optional text to show in a popup when mouse pointer
            hovers over the action.
        :type status_tip: str

        :param parent: Parent widget for the new action. Defaults None.
        :type parent: QWidget

        :param whats_this: Optional text to show in the status bar when the
            mouse pointer hovers over the action.

        :returns: The action that was created. Note that the action is also
            added to self.actions list.
        :rtype: QAction
        """

        # Create the dialog (after translation) and keep reference
        self.dlg = RasterRowColumnDialog()

        icon = QIcon(icon_path)
        action = QAction(icon, text, parent)
        action.triggered.connect(callback)
        action.setEnabled(enabled_flag)

        if status_tip is not None:
            action.setStatusTip(status_tip)

        if whats_this is not None:
            action.setWhatsThis(whats_this)

        if add_to_toolbar:
            self.toolbar.addAction(action)

        if add_to_menu:
            self.iface.addPluginToMenu(
                self.menu,
                action)

        self.actions.append(action)

        return action

    def initGui(self):
        """Create the menu entries and toolbar icons inside the QGIS GUI."""

        icon_path = ':/plugins/RasterRowColumn/icon.png'
        self.add_action(
            icon_path,
            text=self.tr(u'GetRowColumnOfRaster'),
            callback=self.run,
            parent=self.iface.mainWindow())

        # connect our custom function to a clickTool signal that the canvas was clicked
        result = QObject.connect(self.clickTool, SIGNAL("canvasClicked(const QgsPoint &, Qt::MouseButton)"), self.display_point)
        #QMessageBox.information( self.iface.mainWindow(),"Info", "connect = %s"%str(result) )


    def unload(self):
        """Removes the plugin menu item and icon from QGIS GUI."""
        for action in self.actions:
            self.iface.removePluginMenu(
                self.tr(u'&RasterRowColumn'),
                action)
            self.iface.removeToolBarIcon(action)
        # remove the toolbar
        del self.toolbar


    def run(self):
        """Run method that performs all the real work"""
        self.layers = self.iface.legendInterface().layers()
        self.layer_list = []
        for layer in self.layers:
            self.layer_list.append(layer.name())
        self.dlg.comboBox.addItems(self.layer_list)
        
        self.iface.mapCanvas().setMapTool(self.clickTool)

        # show the dialog
        self.dlg.show()
        # Run the dialog event loop
        result = self.dlg.exec_()
        # See if OK was pressed
        if result:
            # Do something useful here - delete the line containing pass and
            # substitute with your code.
            pass
