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
        self.debug.enable_debug()
        Debuggable.__init__(self, 'mePrePrint')

        # get arguments
        self.doc_type = self.args['--type']
        self.title = self.args['--article_title']

    @staticmethod
    def copy(src, dst):
        try:
            shutil.copytree(src, dst)
        except OSError as exc:
            if exc.errno == errno.ENOTDIR:
                shutil.copy(src, dst)
            else: raise

    @staticmethod
    def do_replace(in_string, replace_text, substitute):
        return in_string.replace(replace_text, substitute)

    def create_coversheet(self):
        # copy the coversheet to a temporary directory
        destination = tempfile.mkdtemp()
        self.debug.print_debug(self, u'Copying coversheet to {0}'.format(destination))
        my_dir = os.path.dirname(os.path.realpath(__file__))
        self.copy(os.path.join(my_dir, u'resources/extracted'), os.path.join(destination, u'coversheet'))

        # open the document XML
        with open (u'{0}'.format(os.path.join(destination, u'coversheet/word/document.xml')), 'r') as doc_file:
            contents = doc_file.read()

            contents = self.do_replace(contents, '{ARTICLE_TITLE}', self.title)


        # remove the temporary file
        self.debug.print_debug(self, u'Removing temporary directory {0}'.format(destination))
        shutil.rmtree(destination)

    def run(self):
        self.create_coversheet()


def main():
    MePrePrint().run()

if __name__ == '__main__':
    main()
