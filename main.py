import meezer

#PD = Meezer()

#below used to get Token
#PD.login()
#PD.loginStep2()

#PD.getMyArtists()
User = meezer.User()
albums = User.getAlbums()
for album in albums:
    print(album.title)
#print(ar.downloadPicture())
#meezer.downloadLink("https://www.deezer.com/mx/album/103185862","./test/")

#als = ar.getAlbums()
#print(str(len(als)))
#for al in als:
#    al.download()



"""
downloadPath = './music/'

for artist in artists:
    albums = artist.getAlbums()
    for album in albums:
        try:
            with open('downloaded.txt') as myfile:
                if str(album.id) in myfile.read():
                    print("Album: " + album.title + " already downloaded, skipping...")
                    continue
        except:
            pass

        single = ''
        if album.record_type == 'single':
            single = 'Singles/'

        pathD = str(album.getArtist().name).upper()[0] + "/" + album.getArtist().name + "/" + single + "[" + album.getYear() + "] " + album.title + "/"
        # print(pathD)
        # print(album.link)
        comando = "deemix -p \"" + downloadPath + pathD + "\" " + album.link
        print(comando)
        scan = downloadPath + pathD  # + "[" + album.getYear() + "] " + album.title
        print("scan: " + scan)
        os.system(comando)
        os.system("echo " + str(album.id) + " >> downloaded.txt")
        plexScan = "http://morrolion.com:32400/library/sections/2/refresh?path=" + scan + "&X-Plex-Token=Typea5Ncd-aJ8yp8x1VV"
        print(plexScan)
        plexScan = "http://morrolion.com:32400/library/sections/2/refresh?path=" + urllib.parse.quote_plus(
            scan) + "&X-Plex-Token=Typea5Ncd-aJ8yp8x1VV"
        print(plexScan)
        # break
        requests.get(plexScan)
        sleep(timer)
    # break
"""