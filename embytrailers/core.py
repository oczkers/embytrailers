# -*- coding: utf-8 -*-

"""
embytrailers.core
~~~~~~~~~~~~~~~~~~~~~

This module implements the embytrailers basic methods.

"""

import requests

from .exceptions import EmbytrailersError


username = 'oczko'  # TODO(?): default for every user?
app_id = 'a3c5e476bd7b4573808eb3c13462f420'
host = 'localhost'
port = 8096

replace = (
    # ('R:\\movies\\', 'D:\\'),
    # ('\\OPENWRT\\', 'N:\\dlna\\movies\\'),
)


url_base = 'http://%s:%s/emby' % (host, port)


class Core(object):
    def __init__(self, app_id, username=None, user_id=None, host='localhost', port=8096):
        self.r = requests.Session()
        self.db = self.database()
        if username and not user_id:
            user_id = self.getUserId(username)
        self.user_id = user_id
        self.app_id = app_id
        self.url_base = 'http://%s:%s/emby' % (host, port)
        self.r.headers = {'UserId': self.user_id,
                          'X-MediaBrowser-Token': self.app_id}

    # TODO: def __request__

    def database(self):
        """Returns latest emby trailers database.
        Id is tmdb or imdb if tmdb is not available.
        """
        # TODO: object
        # TODO: find & parse bigger database (imdb maybe?)
        # TODO: separate databases
        # TODO: return all urls
        # TODO: database as separate class
        rc = self.r.get('https://raw.githubusercontent.com/MediaBrowser/Emby.Channels/master/MediaBrowser.Plugins.Trailers/Listings/listingswithmetadata.txt').json()
        db = {}
        for i in rc:
            id = i['ProviderIds'].get('Tmdb') or i['ProviderIds'].get('Imdb')
            db[id] = i['MediaSources'][0]['Path']  # first one has probably allways best quality
        del db[None]  # dirty hack, this method really needs refactorization
        return db

    def getUserId(self, username):
        # TODO: check password etc.
        rc = self.r.get('%s/Users/Public' % url_base).json()
        for u in rc:
            if u['Name'].lower() == username.lower():
                return u['Id']
        raise EmbytrailersError('User %s not found.' % username)

    def getMovies(self, user_id):
        # TODO: getMovies -> getItems(item_type, fileds) etc.
        url_movies = '%s/Users/%s/Items' % (self.url_base, user_id)
        params = {'IncludeItemTypes': 'Movie',
                  'Recursive': True,
                  'StartIndex': 0,
                  'format': 'json',
                  'fields': 'Path,ProviderIds,SortName'}
        movies = self.r.get(url_movies, params=params).json()
        return movies

    def dbGetTrailerUrl(self, tmdb=None, imdb=None):
        """Returns trailer`s url (or None)."""
        # TODO(?): search by name if no tmdb & imdb provided
        return self.db.get(tmdb) or self.db.get(imdb)
