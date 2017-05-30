import requests
import os


user_id = '11371ecfed2d4f7495bb965d7b33608d'  # TODO: find user_id (somekind of username hash maybe?)
app_id = 'a3c5e476bd7b4573808eb3c13462f420'
host = 'localhost'
port = 8096

replace = (
    # ('R:\\movies\\', 'D:\\'),
    # ('\\OPENWRT\\', 'N:\\dlna\\movies\\'),
)


buffer_size = 1024 * 1024  # 1 MB

headers = {
    # 'content-type': 'application/json',
    # 'Authorization': 'MediaBrowser',
    'UserId': user_id,
    # 'Client': 'EmbyTrailers',
    # 'Device': 'Python Script',
    # 'DeviceId': 'xxx',
    # 'Version': '1.0.0.0',
    'X-MediaBrowser-Token': app_id,
}

url = 'http://%s:%s/emby/Users/%s/Items' % (host, port, user_id)


def database():
    """Returns latest emby trailers database.
    Id is tmdb or imdb if tmdb is not available.
    """
    # TODO: object
    # TODO: find & parse bigger database (imdb maybe?)
    # TODO: separate databases
    # TODO: return all urls
    rc = r.get('https://raw.githubusercontent.com/MediaBrowser/Emby.Channels/master/MediaBrowser.Plugins.Trailers/Listings/listingswithmetadata.txt').json()
    db = {}
    for i in rc:
        id = i['ProviderIds'].get('Tmdb') or i['ProviderIds'].get('Imdb')
        db[id] = i['MediaSources'][0]['Path']  # first one has probably allways best quality
    del db[None]  # dirty hack, this method really needs refactorization
    return db


def getUrl(tmdb=None, imdb=None):
    """Returns trailer`s url (or None)."""
    # TODO(?): search by name if no tmdb & imdb provided
    return db.get(tmdb) or db.get(imdb)


def download(url, path):
    """Simple download function."""
    # TODO: somekind of progress bar
    try:
        rc = r.get(url, stream=True)
    except requests.exceptions.ConnectionError as e:
        # print('ERROR: %s' % e)  # TODO: log file
        print('failed.')
        return False

    with open(path, 'wb') as f:
        for buffer in rc.iter_content(buffer_size):
            f.write(buffer)
    print('done.')
    return True


r = requests.Session()
db = database()
r.headers = headers

params = {'IncludeItemTypes': 'Movie',
          'Recursive': True,
          'StartIndex': 0,
          'format': 'json',
          'fields': 'Path,ProviderIds,SortName'}
movies = r.get(url, params=params).json()
for m in movies['Items']:
    # TODO(?): check 'LocationType' and ommit remote
    if m['LocalTrailerCount'] == 0 and 'OPENWRT' not in m['Path']:  # DEBUG
        # TODO: detect exisiting file and propose rescanning library
        url = getUrl(tmdb=m['ProviderIds'].get('Tmdb'),
                     imdb=m['ProviderIds'].get('Imdb'))
        if url:
            path_base = os.path.splitext(m['Path'])[0]
            path_ext = os.path.splitext(url)[1]
            for r in replace:  # change destination directory
                path_base.replace(r[0], r[1])
            path = '%s-trailer%s' % (path_base, path_ext)
            print('Downloading: %s...   ' % m['Name'], end='', flush=True)
            download(url, path)
