import os
from dotenv import load_dotenv
import dotenv
import requests
import pandas as pd
import datetime
import time 

load_dotenv("C:\\Users\\şerefcanmemiş\\Documents\\Projects\\spoti\\.env")
token = os.getenv("TOKEN")

def recently_played_track(token,limit):
    url = "https://api.spotify.com/v1/me/player/recently-played"
    header = {
        "Authorization":f"Bearer {token}",
    }
    params = {
        "market":"TR",
        "limit":limit
    }
    response = requests.get(url=url,headers=header,params=params)
    
    if response.status_code !=200:
        print(response.text)
    last_tracks = response.json().get("items")
    last_tracks = last_tracks[::-1]
    
    #artist_ids = set()
    #for track in last_tracks:
    #    track_artist_id = track.get("track").get("album").get("artists")[0].get("id")
    #    artist_ids.add(track_artist_id)
        
    # artist_genres_map = artists_togenres(token=token,artist_ids=list(artist_ids))
    
    values_list = []
    for track in last_tracks:
        track_name = track.get("track").get("name")
        track_artist = track.get("track").get("album").get("artists")[0].get("name")
        track_artist_id = track.get("track").get("album").get("artists")[0].get("id")
        track_popularity = track.get("track").get("popularity",0)
        release = track.get("track").get("album").get("release_date")
        #track_genres = artist_genres_map.get(track_artist_id)

        try:
            track_release = datetime.datetime.strptime(release,"%Y-%m-%d").date()
        except ValueError:
            try:
                track_release = datetime.datetime.strptime(release,"%Y").date()
            except ValueError:
                track_release = None
        values_list.append((track_name,track_artist,track_artist_id,track_popularity,track_release,datetime.datetime.now()))
        time.sleep(0.0002)
        
    return values_list[::-1]
recently_played_track(token=token,limit=50)

liste=["1g4J8P1JWwanNyyXckRX5W","4q2SZIdLq6YTc9cZLCclWc","4q2SZIdLq6YTc9cZLCclWc"]

def artists_togenres(token,artist_ids):
    
    artist_url = f"https://api.spotify.com/v1/artists/"
    params = {"ids":",".join(artist_ids)}
    header = {
        "Authorization":f"Bearer {token}"
    }
    response = requests.get(artist_url,headers=header,params=params)
    # name = response.json().get("name")
    # print(f"current artist name: {name}")
    artists_data = response.json().get("artists")
    return {artist.get("id"):artist.get("genres") for artist in artists_data}
artists_togenres(token=token,artist_ids=liste)


def search_track(token,genres,limit):
    url = "https://api.spotify.com/v1/search"
    header = {
        "Authorization":f"Bearer {token}"
    }
    all_tracks = [] 
    for genre in genres:
        params = {
            "q":f"genre:{genre}",
            "type":"track",
            "market":"TR",
            "limit":limit
        }
        response = requests.get(url=url,headers=header,params=params)
        if response.status_code !=200:
            print(response.text)
            continue
        results = response.json().get("tracks", {}).get("items", [])
        all_tracks.extend(results)  # Merge all results
    return all_tracks

#search_track(token=token,genres=['turkish hip hop', 'turkish pop'],limit=5)
def artists_genres_store(self,artist_ids):
    self.mycursor.execute("SELECT DISTINCT artist_id FROM spotify_track")
    rows = self.mycursor.fetchall()
    db_ids = set(row[0] for row in rows)
    unique_artist_ids = [artist_id for artist_id in artist_ids if artist_id not in db_ids]
        
    artist_url = f"https://api.spotify.com/v1/artists/"
    params = {"ids":",".join(unique_artist_ids)}
    header = {
            "Authorization":f"Bearer {self.token}"
        }
    response = requests.get(artist_url,headers=header,params=params)
    print(unique_artist_ids)
    artists_data = response.json().get("artists")
        
    if len(unique_artist_ids > 0):
        for artist in artists_data:
            artist_id = artist.get("id")
            artist_genres = artist.get("genres",[])
                
            for genre in artist_genres:
                self.mycursor.execute("""
                        INSERT INTO spotify_artist_genres (artist_id, genre) 
                        VALUES (%s, %s)
                    """, (artist_id, genre))
                
            # Veritabanına işlemi kaydediyoruz
            self.conn.commit()