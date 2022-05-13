import meezer

#PD = Meezer()

#below used to get Token
#PD.login()
#PD.loginStep2()

#PD.getMyArtists()
user = meezer.User()
artists = user.getArtists()
for artist in artists:
    artist.downloadPicture()
    albums = artist.getAlbums()
    for album in albums:
        album.download()

albums = user.getAlbums()
for album in albums:
    print(album.title)
