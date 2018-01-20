
""" Maya Modules Controller Core

*This file contains all main functionalities of the tool.*

:module: maya_modules_controller.core
"""

# Imports
import sys


def delete_module(delete_modules):
    """ Deletes module argument from sys.modules.

    :param delete_modules: Python module to delete
    :type delete_modules: string list
    :return: Modules correctly deleted, Modules that failed to be deleted.
    :rtype: *[string], [string]*

    **Example:**

    .. code-block:: python
        :linenos:

        modules = ['rigging', 'my_awesome_tool_module']
        success, failed = delete_module(module=modules)
    """

    # Stores modules that where correctly deleted
    modules_deleted = []

    # Stores modules that failed to be handle
    failed_modules = []

    # Loop on the module list
    for i in delete_modules:
        for module in sys.modules.keys():
            if module.startswith(i):
                try:
                    del sys.modules[module]
                    modules_deleted.append(i)

                except KeyError:
                    failed_modules.append(i)

    return modules_deleted, failed_modules


def get_list_modules():
    """ List of Python modules loaded on you session.

    :return: Python modules list from sys.modules
    :rtype: *[string]*
    """

    modules = []

    for module in sys.modules.keys():
        # The following check serves as a filter for modules that are not
        # bounded to a specific python file
        if sys.modules[module]:
            modules.append(module)

    return modules
