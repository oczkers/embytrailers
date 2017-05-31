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

import os
from docopt import docopt

from .core import Core
from .utils import download


replace = (  # TODO: docopt
    # ('R:\\movies\\', 'D:\\'),
    # ('\\OPENWRT\\', 'N:\\dlna\\movies\\'),
)


def __main__():
    # TODO: --all trailers
    args = docopt(__doc__)
    username = args['<username>']
    app_id = args['<app_id>']
    print(args)
    et = Core(app_id=app_id, username=username)
    movies = et.getMovies(et.user_id)
    for m in movies['Items']:
        # TODO(?): check 'LocationType' and ommit remote
        if m['LocalTrailerCount'] == 0 and 'OPENWRT' not in m['Path']:  # DEBUG
            # TODO: detect exisiting file and propose rescanning library
            url = et.dbGetTrailerUrl(tmdb=m['ProviderIds'].get('Tmdb'),
                                     imdb=m['ProviderIds'].get('Imdb'))
            if url:
                path_base = os.path.splitext(m['Path'])[0]
                path_ext = os.path.splitext(url)[1]
                for r in replace:  # change destination directory
                    path_base.replace(r[0], r[1])
                path = '%s-trailer%s' % (path_base, path_ext)
                print('Downloading: %s...   ' % m['Name'], end='', flush=True)
                download(url, path)


if __name__ == "__main__":
    __main__()
