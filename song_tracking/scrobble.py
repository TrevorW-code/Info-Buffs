import requests
import pandas as pd
import numpy as np

sample_req = "https://ws.audioscrobbler.com/2.0/?method=user.getrecenttracks&user="+USER+"&api_key="+API_SECRET+"&format=json"
obj = requests.get(sample_req)

SongObjList2 = []

class SongObject2:
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
    time_played = track["date"]["#text"]
    last_fm_link = track['url']
    # something in this is broken
    songInstance = SongObject2(index,artist,image,album,track_name,time_played,last_fm_link)
    SongObjList2.append(songInstance)

df2 = pd.DataFrame([x.as_dict() for x in SongObjList2])

f = open("test.md","w")
f.write(df2.to_markdown())
f.close()
