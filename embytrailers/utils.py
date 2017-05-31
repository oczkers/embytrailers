# -*- coding: utf-8 -*-

"""
embytrailers.utils
~~~~~~~~~~~~~~~~~~~~~

This module implements the embytrailers basic methods.

"""

import requests


buffer_size = 1024 * 1024  # 1 MB


def download(url, path, buffer_size=buffer_size):
    """Simple download function."""
    # TODO: somekind of progress bar
    try:
        rc = requests.get(url, stream=True)
    except requests.exceptions.ConnectionError as e:
        # print('ERROR: %s' % e)  # TODO: log file
        print('failed.')
        return False

    # TODO: detect non existing directory && existing file
    with open(path, 'wb') as f:
        for buffer in rc.iter_content(buffer_size):
            f.write(buffer)
    print('done.')
    return True
