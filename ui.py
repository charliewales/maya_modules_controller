
""" Maya Module Controller UI
:module: maya_modules_controller.ui

*Contains the ui Qt widgets*

The UI has a line text edit to type (search/filter) modules as well as a list
view widget that will display the modules. A push button widget at the end will
be use to trigger the delete modules.
"""

# Imports
from PySide2 import QtWidgets


class MayaModulesControllerUI(QtWidgets.QDialog):
    """ Maya_Modules_Controller UI.

    Setup the tool user interface. Creates a QListView that can holds the list
    of python modules been loaded.

    :param parent: Parent application
    :type parent: QtWodget

    :param window_title: Title for the user interface window.
                         Default Maya Modules Controller
    :type window_title: string
    """

    def __init__(self, parent=None, window_title='Maya Modules Controller'):
        """ Launches the UI widget creation """

        super(MayaModulesControllerUI, self).__init__(parent)

        # Sets window title
        self.setWindowTitle(window_title)

        # Creates widgets
        self.create_widgets()

    def create_widgets(self):
        """ Creates the nessesary widgets.

        Creates a grid layout widget that will lay the line edit, list view
        and push button widgets.
        """

        # Creates layout and applies it to the QDialog
        self.layout_widget = QtWidgets.QGridLayout()
        self.setLayout(self.layout_widget)

        # Line edit widget
        self.line_edit = QtWidgets.QLineEdit()
        self.line_edit.setPlaceholderText('search your module...')

        # List view widget
        self.list_view = QtWidgets.QListView()
        self.list_view.setSelectionMode(
            QtWidgets.QAbstractItemView.ExtendedSelection)
        self.list_view.setUpdatesEnabled(True)

        # Button widget
        self.delete_button = QtWidgets.QPushButton('Delete')

        # Adds widgets to the layout
        for widget in [self.line_edit, self.list_view,
                       self.delete_button]:
            self.layout_widget.addWidget(widget)
