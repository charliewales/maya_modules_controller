
""" **Maya Modules Controller Tool**

*Modules Controller allows user to quickly remove user specific
modules already loaded.*

:module: 'maya_modules_controller.__init__'
:platform: Unix, Windows


.. note:: You can use this to launch the tool.

.. warning:: This tool is still pretty wip.
.. todo:: * Write tests functions.
          * Add filter feature.
          * Apply CSS style.

:author: Jerome Drese <jeromed@nwavedigital.com>
:date: 26 May 2017
"""

# Imports
import logging
import sys

from PySide2 import QtWidgets
import maya.cmds
import shiboken2

import maya.OpenMayaUI
import maya_modules_controller.main
import maya_modules_controller.ui


# Maya Modules Controller imports
def run(mode):
    """ Runs the tool.

    :param mode: 0: Maya (running inside Maya) / 1: Standalone
    :type mode: int
    """

    logging.info('Maya Modules Controller: Initializing...')

    # Declares empty application variable.
    app = None

    # Support for standalone application
    if mode:
        app = QtWidgets.QApplication(sys.argv)
        # Maya Modules Controller class object
        tool = maya_modules_controller.main.MayaModulesController()
        tool.show()

    if not mode:

        # Gets Maya application widget
        maya_window = maya.OpenMayaUI.MQtUtil.mainWindow()
        # Maya Modules Controller class object
        tool = maya_modules_controller.main.MayaModulesController(
                shiboken2.wrapInstance(long(maya_window), QtWidgets.QDialog))
        tool.show()

        logging.info('Maya Modules Controller: Ready')
        return tool

    # Runs the application for standalone support
    if app:
        logging.info('Maya Modules Controller: Ready')
        sys.exit(app.exec_())


if __name__ == "__main__":

    logging.info('Maya Modules Controller : STANDALONE MODE')

    # Runs the application in standalone mode
    run(1)
