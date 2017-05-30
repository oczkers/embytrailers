# -*- coding: utf-8 -*-

"""
embytrailers.cli
~~~~~~~~~~~~~~~~

Usage:
    embytrailers <username> <app_id>

Options:
    -h --help   Show this screen.
    --version   Show version.

"""

from docopt import docopt

from . import core


def main():
    args = docopt(__doc__)
    username = args['<username>']
    app_id = args['<app_id>']
    print(args)
    # core.
