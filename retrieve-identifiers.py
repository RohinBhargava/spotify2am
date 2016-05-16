import csv
import struct
import urllib.parse, urllib.request
import json

def retrieve_itunes_identifier(title, artist, album):
    headers = {

    }
    url = "https://itunes.apple.com/search?term=" + urllib.parse.quote(title) + "&limit=100"
    request = urllib.request.Request(url, None, headers)
    best_match = None
    response = urllib.request.urlopen(request)
    data = json.loads(response.read().decode('utf-8'))
    songs = [result for result in data["results"] if result["wrapperType"] == "track"]

    for song in songs:
        artistBool = False;
        keys = song.keys()
        for i in artist.split(','):
            if (i.lower() in song["artistName"].lower() or song["artistName"].lower() in i.lower()):
                artistBool = True

        if ("isStreamable" in keys):
            if (bool(song["isStreamable"]) and (song["trackName"].lower() in title.split("-")[0].lower() or title.split("-")[0].lower() in song["trackName"].lower()) and artistBool):
                albumNameBool = song["collectionName"].lower() in album.lower() or album.lower() in song["collectionName"].lower()
                if (albumNameBool):
                    if ("trackExplicitness" in keys):
                        if (song["trackExplicitness"] != "cleaned"):
                            best_match = song["trackId"]
                            break
                    else:
                        best_match = song["trackId"]
                        break
                if (best_match == None):
                    best_match = song["trackId"]

    return best_match


itunes_identifiers = []
filehandle = open("toAddManually.txt", 'w')


with open('spotify.csv', encoding='utf-8') as playlist_file:
    playlist_reader = csv.reader(playlist_file)
    next(playlist_reader)

    for row in playlist_reader:
        title, artist, album = row[1], row[2], row[3]
        itunes_identifier = retrieve_itunes_identifier(title, artist, album)

        if itunes_identifier:
            itunes_identifiers.append(itunes_identifier)
            print("{} - {} => {}".format(title, artist, itunes_identifier))
        else:
            print("{} - {} => Not Found".format(title, artist))
            filehandle.write(title + ' ' + artist + '\n')


with open('itunes.csv', 'w', encoding='utf-8') as output_file:
    for itunes_identifier in itunes_identifiers:
        output_file.write(str(itunes_identifier) + "\n")
