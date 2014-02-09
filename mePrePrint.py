#!/usr/bin/env python
"""mePrePrint: generate a combined PDF document from input files; to be used for green archiving

Usage:
    meTypeset.py generate <input_cover> <input_article> <output_file> [options]

Options:
    -t, --type <type>                               The type of article (preprint, aam, postprint)
    -a, --author <author name>                      The name of the author as it should appear
    -c, --citation <citation>                       The citation information as it should appear
    -h, --help                                      Show this screen.
    -r, --article_title <article_title>             The article's title
    -o, --copyright <copyright>                     The copyright of the article
    -y, --year <year>                               The year of publication
    -u, --url <url>                                 The article URL
"""

from debug import Debuggable
from docopt import docopt
import tempfile
import os
import shutil, errno
from debug import Debug
import zipfile
import subprocess

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
        self.name = self.args['--author']
        self.copyright_year = self.args['--year']
        self.copyright = self.args['--copyright']
        self.citation = self.args['--citation']
        self.url = self.args['--url']

        self.version = 'VERSION'

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

    @staticmethod
    def zip_dir(path, zip_file, final):
        relative = os.path.join(os.path.abspath(os.path.join(path, os.pardir)), final)
        for root, dirs, files in os.walk(path):
            for file_name in files:
                zip_file.write(os.path.join(root, file_name), os.path.relpath(os.path.join(root, file_name),
                                                                              os.path.join(path, relative)))

    def create_coversheet(self, destination):
        # copy the coversheet to a temporary directory
        src = self.args['<input_cover>']
        self.debug.print_debug(self, u'Copying coversheet')
        os.mkdir(os.path.join(destination, u'coversheet'))

        with zipfile.ZipFile(src, "r") as z:
            z.extractall(os.path.join(destination, u'coversheet'))

        # open the document XML
        self.debug.print_debug(self, u'Replacing cover sheet variables')
        with open (u'{0}'.format(os.path.join(destination, u'coversheet/word/document.xml')), 'r+') as doc_file:
            contents = doc_file.read()

            contents = self.do_replace(contents, '{ARTICLE_TITLE}', self.title)
            contents = self.do_replace(contents, '{AUTHOR_NAME}', self.name)
            contents = self.do_replace(contents, '{VERSION}', self.version)
            contents = self.do_replace(contents, '{JOURNAL_CITATION}', self.version)
            contents = self.do_replace(contents, '{URL}', self.url)
            contents = self.do_replace(contents, '{COPYRIGHT}', self.copyright)
            contents = self.do_replace(contents, '{COPYRIGHT_YEAR}', self.copyright_year)

            doc_file.seek(0)
            doc_file.write(contents)
            doc_file.truncate()

        self.debug.print_debug(self, u'Replacing cover sheet hyperlinks')
        with open (u'{0}'.format(os.path.join(destination, u'coversheet/word/_rels/document.xml.rels')),
                   'r+') as doc_file:

            contents = doc_file.read()

            contents = self.do_replace(contents, '{URL}', self.url)

            doc_file.seek(0)
            doc_file.write(contents)
            doc_file.truncate()

        # re-package the file into a docx
        with zipfile.ZipFile(os.path.join(destination, u'final_cover.docx'), "w") as z:
            self.zip_dir(os.path.join(destination, u'coversheet'), z, 'coversheet')

        pdf = os.path.join(destination, u'final_cover.pdf')

        command = 'unoconv -f pdf {0}'.format(os.path.join(destination, u'final_cover.docx'))

        self.debug.print_debug(self, 'Running: {0}'.format(command))

        subprocess.call(command.split(' '))

        # remove the temporary file
        return pdf

    def run(self):
        # create temporary directory
        temp_dir = tempfile.mkdtemp()
        self.debug.print_debug(self, u'Making temporary directory {0}'.format(temp_dir))

        # create the coversheet
        pdf = self.create_coversheet(temp_dir)
        shutil.copy(pdf, self.args['<output_file>'])

        # remove the temporary directory
        self.debug.print_debug(self, u'Removing temporary directory {0}'.format(temp_dir))
        shutil.rmtree(temp_dir)


def main():
    MePrePrint().run()

if __name__ == '__main__':
    main()
