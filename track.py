import os
from dotenv import load_dotenv
import dotenv
import requests
import pandas as pd
import datetime
import time 

load_dotenv("C:\\Users\\şerefcanmemiş\\Documents\\Projects\\spoti\\.env")
token = os.getenv("TOKEN")

def recently_played_track(token,limit=50):
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
    
    values_list = []
    for track in last_tracks:
        track_name = track.get("track").get("name")
        track_artist = track.get("track").get("album").get("artists")[0].get("name")
        track_artist_id = track.get("track").get("album").get("artists")[0].get("id")
        track_popularity = track.get("track").get("popularity",0)
        
        release = track.get("track").get("album").get("release_date")
        try:
            track_release = datetime.datetime.strptime(release,"%Y-%m-%d").date()
        except ValueError:
            try:
                track_release = datetime.datetime.strptime(release,"%Y").date()
            except ValueError:
                track_release = None
        values_list.append((track_name,track_artist,track_artist_id,track_popularity,track_release,datetime.datetime.now()))
        time.sleep(0.0007)
        
    return values_list[::-1]
recently_played_track(token=token,limit=50)

liste=['3Sz7ZnJQBIHsXLUSo0OQtM', '35WVTyRnKAoaGExqgktVyb', '5jTtGLk1mGFMY5lQOvJYUj', '2sSGPbdZJkaSE2AbcGOACx']

def artists_togenres(token,artist_ids):
    
    artist_url = f"https://api.spotify.com/v1/artists/"
    params = {"ids":",".join(artist_ids)}
    header = {
        "Authorization":f"Bearer {token}"
    }
    response = requests.get(artist_url,headers=header,params=params)
    if response.status_code !=200:
        print(response.text)
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
