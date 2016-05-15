import csv
import struct
import urllib.parse, urllib.request
import json

def retrieve_itunes_identifier(title, artist):
    headers = {

    }
    url = "https://itunes.apple.com/search?term=" + urllib.parse.quote(title)
    request = urllib.request.Request(url, None, headers)

    try:
        response = urllib.request.urlopen(request)
        data = json.loads(response.read().decode('utf-8'))
        songs = [result for result in data["results"] if result["wrapperType"] == "track"]
        # Attempt to match by title & artist
        for song in songs:
            artistBool = False;
            for i in artist.split(','):
                if (i.lower() in song["artistName"].lower() or song["artistName"].lower() in i.lower()):
                    artistBool = True

            if (bool(song["isStreamable"]) and (song["trackName"].lower() in title.lower() or title.lower() in song["trackName"].lower()) and artistBool):
                if ("trackExplicitness" in song.keys()):
                    if (song["trackExplicitness"] == "explicit"):
                        return song["trackId"]
                else:
                    return song["trackId"]

        # Attempt to match by title if we didn't get a title & artist match
        # for song in songs:
        #     if song["name"].lower() == title.lower():
        #         poop.append((title, artist))
        #         return song["id"]


    except:
        # We don't do any fancy error handling.. Just return None if something went wrong
        return None


itunes_identifiers = []


with open('spotify.csv', encoding='utf-8') as playlist_file:
    playlist_reader = csv.reader(playlist_file)
    next(playlist_reader)

    for row in playlist_reader:
        title, artist = row[1], row[2]
        itunes_identifier = retrieve_itunes_identifier(title, artist)

        if itunes_identifier:
            itunes_identifiers.append(itunes_identifier)
            print("{} - {} => {}".format(title, artist, itunes_identifier))
        else:
            print("{} - {} => Not Found".format(title, artist))


with open('itunes.csv', 'w', encoding='utf-8') as output_file:
    for itunes_identifier in itunes_identifiers:
        output_file.write(str(itunes_identifier) + "\n")