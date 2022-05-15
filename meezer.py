import urllib
import re
import webbrowser
import requests
import os
from time import sleep

token = 'frAXrr0CbmJUvjVg4ViWNIIvJzT1e6uNwkF7zrR8iKpbrmpk3d'
AppName = 'Meezer'
secretKey = '3d94fbdd82f4a78a5efc7a9dda4ceac4'
AppId = '541342'


def downloadLink(link, path):
    comando = "deemix -p \"" + path + "\" " + link
    os.system(comando)

def login(self):
    AppName = 'Meezer'
    secretKey = '3d94fbdd82f4a78a5efc7a9dda4ceac4'
    AppId = '541342'
    #url = 'https://connect.deezer.com/oauth/auth.php'
    #params = {'app_id': 'py-deezer', 'redirect_uri': 'http://morrolin.com', 'perms': 'basic_access,email,offline_access,manage_library,delete_library,listening_history'}
    fullUrl = 'https://connect.deezer.com/oauth/auth.php?app_id=' + AppId + '&redirect_uri=http://deezer.morrolion.com&perms=basic_access,email,offline_access,manage_library,delete_library,listening_history'
    #requests.get(url,params=params)
    webbrowser.open(fullUrl, new=0, autoraise=True)
    print("get code from url opened after login")

def loginStep2(self):
    code = 'fr9cf11dd787c02bc76117dd5fb8a561' #got from login() response
    AppId = '541342' #got from Deezer devs
    secretKey = '3d94fbdd82f4a78a5efc7a9dda4ceac4' #got from Deezer devs
    output = 'json'
    fullURL = 'https://connect.deezer.com/oauth/access_token.php?app_id=' + AppId + '&secret=' + secretKey + '&code=' + code
    response = requests.get(fullURL)
    print(response)
    print(response.text)

class User(object):
    token = "frAXrr0CbmJUvjVg4ViWNIIvJzT1e6uNwkF7zrR8iKpbrmpk3d"
    downloadPath = "/home/rclone/deezer/"

    def getArtists(self):
        url = 'https://api.deezer.com/user/me/artists?access_token=' + self.token
        result = requests.get(url).json()
        artists = []
        for artist in result['data']:
            artists.append(Artist(artist))
        return artists


    def getAlbums(self):
        url = 'https://api.deezer.com/user/me/albums?access_token=' + self.token
        result = requests.get(url).json()
        albums = []
        for album in result['data']:
            albums.append(Album(album))
        return albums


class Album(object):

    def __init__(self, data):
        self.id = str(data['id'])
        self.title = data['title']
        self.link = data['link']
        self.cover = data['cover_xl']
        try:
            self.genre_id = data['genre_id']
        except:
            pass
        self.release_date = data['release_date']
        self.record_type = data['record_type']
        self.explicit_lyrics = data['explicit_lyrics']
        try:
            self.artist = Artist(data['artist'])
        except:
            pass

    def getYear(self):
        return str(self.release_date).split('-')[0]

    def getPath(self):
        return "[" + self.getYear() + "] " +self.title + "/"

    def getArtist(self):
        url = 'https://api.deezer.com/album/' + self.id
        result = requests.get(url).json()
        #print(result)
        return Artist(result['artist'])

    def download(self):
        try:
            with open('downloaded.txt') as myfile:
                if str(self.id) in myfile.read():
                    print("Album: " + self.title + " already downloaded, skipping...")
                    return
        except:
            pass
        single = ''
        timer = 35
        if self.record_type == 'single':
            single = 'Singles/'
            timer = 10
        path = User.downloadPath + str(self.getArtist().name).upper()[0] + "/" + re.sub(r'[\/:\\\*?\"><\|]', '-', self.getArtist().name) + "/" + single + "[" + self.getYear() + "] " + re.sub(r'[\/:\\\*?\"><\|]', '-', self.title) + "/"
        #path = re.sub(r'[\/:\\\*?\"><\|]', '-', path)
        print(path)
        comando = "deemix -p \"" + path + "\" " + self.link
        os.system(comando)
        #+plexScan = "http://morrolion.com:32400/library/sections/2/refresh?path=" + path + "&X-Plex-Token=Typea5Ncd-aJ8yp8x1VV"
        #print(plexScan)
        plexScan = "http://morrolion.com:32400/library/sections/2/refresh?path=" + urllib.parse.quote_plus(path) + "&X-Plex-Token=Typea5Ncd-aJ8yp8x1VV"
        print(plexScan)
        os.system("echo " + str(self.id) + " >> downloaded.txt")
        requests.get(plexScan)
        sleep(timer)

class Artist(object):

    def __init__(self, data):
        self.id = str(data['id'])
        self.name = data['name']
        try:
            self.link = data['link']
        except:
            pass
        self.picture = data['picture_xl']
        try:
            self.nb_album = data['nb_album']
        except:
            pass

    def getAlbums(self):
        url = 'https://api.deezer.com/artist/' + self.id + '/albums'
        result = requests.get(url).json()
        albums = []
        for album in result['data']:
            albums.append((Album(album)))
        return albums

    def getPath(self):
        return str(self.name).upper()[0] + '/'# + self.name + '/'

    def downloadPicture(self):
        path = User.downloadPath + str(self.name).upper()[0] + "/" + re.sub(r'[\/:\\\*?\"><\|]', '-',self.name) + "/"
        os.system("mkdir -p \"" + path + "\"")
        file = path + "Picture.jpg"
        if os.path.exists(file):
            print("---------> Picture for " + self.name + "Already downloaded")
            return
        print("-----------> Downloading Picture for " + self.name)
        os.system("touch \"" + file + "\"")
        urllib.request.urlretrieve(self.picture, file)