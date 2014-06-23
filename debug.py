from __future__ import print_function

__author__ = 'Martin Paul Eve'
__email__ = "martin@martineve.com"

import sys


class Debug(object):
    def __init__(self):
        """
        Initialise this debug instance
        @param gv: a reference to an instance of the meTypeset global configuration class
        """
        self.debug = False
        self.has_run = False

    def enable_debug(self):
        self.debug = True

    def print_debug(self, module, message):
        """
        This method prints debug information to stdout when the global debug flag is set
        @param module: the calling module
        @param message: the debug message to print
        """
        if self.debug:
            print(u'[{0}] {1}'.format(module.get_module_name(), unicode(message)))

    def write_error(self, module, message, error_number):
        """
        This method writes parsing information to the error log
        @param module: the calling module
        @param message: the error message to print
        """

        if not self.has_run:
            module.gv.mk_dir(module.gv.error_folder_path)
            self.has_run = True

        error_file = open(module.gv.error_file_path, 'w')
        print(u'[{0}] {1}\n'.format(error_number, message), file=error_file)
        error_file.close()

    @staticmethod
    def fatal_error(module, message):
        print(u'[FATAL ERROR] [{0}] {1}'.format(module.get_module_name(), message))
        sys.exit(1)


class Debuggable(object):
    def __init__(self, module_name):
        self.module_name = module_name

    def get_module_name(self):
        return unicode(self.module_name, 'utf-8')