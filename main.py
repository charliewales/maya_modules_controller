
""" Maya Modules Controller Main
:module: maya_modules_controller.main

*Module description*
"""

# Imports
import logging

from PySide2 import QtGui, QtCore

import maya_modules_controller.core
import maya_modules_controller.ui


# Maya Modules Controller imports
class MayaModulesController(object):
    """ Maya_Modules_Controller initialization setup.

    Setup the tool and its user interface.

    :param parent: The parent arguments can be use to give the UI a parent
                widget. When using this tool inside Maya you can pass
                to the parent argument Maya's window in a wrapped widget.
    :type parent: QtWidget

    **Example:**

    .. code-block:: python
        :linenos:

        maya_window = maya.OpenMayaUI.MQtUtil.mainWindow()
        MayaModulesController(shiboken2.wrapInstance(long(maya_window), QtWidgets.QDialog))
    """

    def __init__(self, parent=None):
        """ Initialize the view and setups the ui. """

        super(MayaModulesController, self).__init__()

        # Protected variables
        self.__modules_list = maya_modules_controller.core.get_list_modules()
        self.__modules_model = QtGui.QStringListModel(self.modules_list)
        self.__proxy_model = self.__qsort_filter_proxy_model()

        # Initialize the UI
        self.ui = self.initialize_ui(parent)
        # Connects signals
        self.ui.delete_button.clicked.connect(self.delete_modules)
        self.ui.line_edit.textChanged.connect(self.filter_modules)

        # Sets string thing model
        self.string_model = self.modules_model
        self.proxy_model.setSourceModel(self.string_model)
        self.ui.list_view.setModel(self.proxy_model)

    def __qsort_filter_proxy_model(self):
        """ Creates and setups a QSortFilterProxyModel that will recieve the
        QStringListModel. """

        _proxy = QtCore.QSortFilterProxyModel()
        _proxy.setFilterCaseSensitivity(QtCore.Qt.CaseInsensitive)
        _proxy.setDynamicSortFilter(True)
        return _proxy

    def close(self):
        """ Closes the user interface. """

        self.ui.destroy()

    def delete_modules(self, modules=None):
        """ Deletes modules.

        If not modules are been passed to the modules argument this functions
        queries the selected modules on the UI list in order to delete them.

        :param modules: List of modules you want to delete.
        :type modules: [string]

        :return: Modules correctly deleted, Modules that failed to be deleted.
        :rtype: *[string], [string]*
        """

        # Queries selected modules on the UI.
        if not modules:
            modules = self.get_selected_modules()

        # Deletes the modules.
        m_sucess, m_failed = maya_modules_controller.core.delete_module(
                                                            modules)

        # If they are failed modules that couln't be removed then remove those
        # from the list remove update.
        for i in m_failed:
            logging.warning('{}: module could not be deleted'.format(i))
            modules.remove(i)

        # Removes modules from the UI list.
        for i in modules:
            index = self.string_model.stringList().index(i)
            self.string_model.removeRow(index)
            logging.info('{}: module deleted'.format(i))

        return m_sucess, m_failed

    def filter_modules(self, text=None):
        """ Filters the proxy_model.

        You can use this to filter the view to only the elements containing the
        given text. If not text is provided it queries the one been taped in
        the line_edit widget

        :param text: String that you want to use as filter.
        :type text: string
        """

        self.proxy_model.setFilterRegExp(text)

    def get_selected_modules(self):
        """ Modules selected from the UI list.

        :return: Selected modules.
        :rtype: *[string]*
        """

        selected_modules = []

        # Gets the string value from the index returned by the view
        for i in self.ui.list_view.selectedIndexes():
            selected_modules.append(i.data())

        return selected_modules

    @staticmethod
    def initialize_ui(parent):
        """ Instance of the MayaModulesControllerUI object. """

        return maya_modules_controller.ui.MayaModulesControllerUI(
            parent=parent)

    @property
    def modules_list(self):
        """ Current Python modules list been used.

        You can use it to apply a new list of modules to the view.
        **Example:**

        .. code-block:: python
            :linenos:

            controller = MayaModulesController()
            controller.modules_list = ['your_module', 'another_module']

        :return: Python modules loaded.
        :rtype: *[string]*
        """

        return self.__modules_list

    @modules_list.setter
    def modules_list(self, modules_list):
        """ modules_list property setter.

        :param modules_list: String list of Python modules.
        :type modules_list: [string]
        """

        logging.info('Refreshing...')
        self.__modules_list = modules_list
        self.modules_model = self.modules_list

    @property
    def modules_model(self):
        """ Instance of the ModulesListModel object.

        This model inherist from the QAbstractListModel.

        :return: Instance of the ModulesListModel class object.
        :rtype: *QAbstractListModel*
        """

        return self.__modules_model

    @modules_model.setter
    def modules_model(self, modules_list):
        """ modules_model property setter.

        :param modules_list: String list of Python modules.
        :type modules_list: [string]
        """

        self.__modules_model = QtGui.QStringListModel(modules_list)
        self.string_model = self.modules_model
        self.proxy_model.setSourceModel(self.modules_model)

    @property
    def proxy_model(self):
        """ Proxy Model is a QSortFilterProxyModel that is applied to the view.

        You can use the proxy_model to set some custom behavior to the view.
        """

        return self.__proxy_model

    def refresh(self):
        """ **Refrehes the modules list.**

        Refresh will check if a filter has been applied to the tool and refresh
        the modules list within that filter.

        If no filter has been applied to the modules list refresh will query
        all modules been loaded back from sys.modules

        .. todo:: Needs to handle a refresh with filter already set.
        """
        self.modules_list = maya_modules_controller.core.get_list_modules()

    def show(self):
        """ Displays the user interface. """

        self.ui.show()
