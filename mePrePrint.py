__author__ = 'martin'

#!/usr/bin/env python
"""mePrePrint: generate a combined PDF document from input files; to be used for green archiving

Usage:
    meTypeset.py generate <input_cover> <input_article> <output_file> [options]

Options:
    -t, --type <type>                               The type of article (preprint, aam, postprint)
    -a, --author <author name>                      The name of the author as it should appear
    -c, --citation <citation<                       The citation information as it should appear
    -h, --help                                      Show this screen.
    -r, --article_title <article_title>             The article's title
    -o, --copyright <copyright>                     The copyright of the article
    -y, --year <year>                               The year of publication
"""

from debug import Debuggable
from docopt import docopt
import tempfile
import os
import shutil, errno
from debug import Debug

__author__ = "Martin Paul Eve"
__email__ = "martin@martineve.com"


class MePrePrint (Debuggable):
    def __init__(self):
        # read  command line arguments
        self.args = docopt(__doc__, version='meTypeset 0.1')

        # initialize debugger
        self.debug = Debug()
        Debuggable.__init__(self, 'mePrePrint')

    @staticmethod
    def copy(src, dst):
        try:
            shutil.copytree(src, dst)
        except OSError as exc:
            if exc.errno == errno.ENOTDIR:
                shutil.copy(src, dst)
            else: raise

    def create_coversheet(self):
        tempfile.mkdtemp()
        my_dir = os.path.dirname(os.path.realpath(__file__))

        self.copy(os.path.join(my_dir, 'resources/extracted'))



    def run(self):
        self.create_coversheet()


def main():
    MePrePrint().run()

if __name__ == '__main__':
    main()
