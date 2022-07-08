# artist.getSimilar
# artist.search --> search artist

import requests
import pandas as pd
import numpy as np
import sys
from secrets import api_key, shared_secret

my_user = "KRYPTOTHEDAWG"

sample_req = "https://ws.audioscrobbler.com/2.0/?method=user.getrecenttracks&user="+my_user+"&api_key="+api_key+"&format=json"
obj = requests.get(sample_req).json()



SongObjList2 = []

class SongObject:

    def __init__(self,index,artist,image,album,track_name,time_played,last_fm_link):
        self.index = index
        self.artist = artist
        self.image = image
        self.album = album
        self.track_name = track_name
        self.time_played = time_played
        self.last_fm_link = last_fm_link
        self.linked_image = "[![img]("+str(image)+")]("+str(last_fm_link)+")"
        
    def list_attr(self):
        print(index,artist,image,album,track_name,time_played,last_fm_link)
        
    def as_dict(self):
        return {'image': self.linked_image, 'track_name': self.track_name, 'artist': self.artist, 'album': self.album,'time_played': self.time_played}

# clean this up for the cron job
for idx,track in enumerate(obj['recenttracks']['track']):
    index = idx
    artist = track["artist"]["#text"]
    image = track["image"][2]["#text"]
    album = track["album"]["#text"]
    track_name = track["name"]
    date = track["date"]["#text"]
    time_played = date if date is not None else "NA"
    last_fm_link = track['url']
    print()
    songInstance = SongObject(index,artist,image,album,track_name,time_played,last_fm_link)
    SongObjList2.append(songInstance)

df = pd.DataFrame([x.as_dict() for x in SongObjList2])

with open("recent_songs.md","w") as f:
    f.write(df.to_markdown())
# f = open("test.md","w")
# f.close()