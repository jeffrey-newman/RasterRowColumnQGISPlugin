# -*- coding: utf-8 -*-
"""
/***************************************************************************
 RasterRowColumn
                                 A QGIS plugin
 Get row and column of point on raster
                             -------------------
        begin                : 2017-02-23
        copyright            : (C) 2017 by Jeffrey Newman
        email                : jeffrey.newman.au@gmail.com
        git sha              : $Format:%H$
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
 This script initializes the plugin, making it known to QGIS.
"""


# noinspection PyPep8Naming
def classFactory(iface):  # pylint: disable=invalid-name
    """Load RasterRowColumn class from file RasterRowColumn.

    :param iface: A QGIS interface instance.
    :type iface: QgsInterface
    """
    #
    from .RasterRowColumn import RasterRowColumn
    return RasterRowColumn(iface)
