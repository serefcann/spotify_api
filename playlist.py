import os
from dotenv import load_dotenv
import dotenv
import requests
import pandas as pd
import time

# kullanicinin yazdigi ture gore(dinledigi sarkiya gore) daha once playliste ekledigi sarkilari getir

load_dotenv("C:\\Users\\şerefcanmemiş\\Documents\\Projects\\spoti\\.env")
token = os.getenv("TOKEN")

nirvana="4JBJ8avzjA2HawsDqlHRD5"
ruya="41g0coWFtnGGGvV7VmzMjg"
lik = "2SX9d8NEMprU9hQbs8u8yT"
album_ids = [nirvana,ruya,lik]

def get_album(album_id,query,token,limit=100):
    header = {
        "Authorization":f"Bearer {token}"
    }
    params = {
        "q":query,
        "market":"TR"
    }
    album_url=f'https://api.spotify.com/v1/playlists/{album_id}/tracks?limit={limit}'
    response = requests.get(url=album_url,headers=header,params=params)
    return response.json().get("items")

album_song=[]
for album in album_ids:
    album_song.append(get_album(album,query="rock",token=token))
    


def song_df(album_song):
    df = pd.DataFrame(columns=(["song_id","song_name","song_popularity","song_artist","artist_id","release_year"]))
    
    for songs in album_song:
        for song in songs:
            song_name = song.get("track").get("name")
            song_id = song.get("track").get("id")
            song_pop = song.get("track").get("popularity")
            song_artist = song.get("track").get("artists")[0].get("name")
            artist_id = song.get("track").get("artists")[0].get("id")
            song_date = song.get("track").get("album").get("release_date")
            release_year = int(song_date[:4])
            save = {
                "song_id":"spotify:track:"+song_id,
                "song_name":song_name,
                "song_popularity":song_pop,
                "song_artist":song_artist,
                "artist_id":artist_id,
                "release_year":release_year
            }
            df.loc[len(df)] = save
    return df
df = song_df(album_song=album_song)
df.dtypes


def currently_playing_track(token):
    url = "https://api.spotify.com/v1/me/player/currently-playing"
    header = {
        "Authorization":f"Bearer {token}",
    }
    params = {
        "market":"TR"
    }
    response = requests.get(url=url,headers=header,params=params)
    
    if response.status_code !=200:
        print(response.text)
    return response.json().get("item")
        
last_track=currently_playing_track(token=token)
last_track_name = last_track.get("name")
last_track_artist = last_track.get("album").get("artists")[0].get("name")
last_track_artist_id = last_track.get("album").get("artists")[0].get("id")


def artist_togenres(token,artist_id):
    artist_url = f"https://api.spotify.com/v1/artists/{artist_id}"
    header = {
        "Authorization":f"Bearer {token}"
    }
    response = requests.get(artist_url,headers=header)
    # name = response.json().get("name")
    # print(f"current artist name: {name}")
    return response.json().get("genres")
artist_togenres(token=token,artist_id=last_track_artist_id)
artist_togenres(token=token,artist_id="4q2SZIdLq6YTc9cZLCclWc")

def genre_match(df):
    current_track_genres = artist_togenres(token=token,artist_id=last_track_artist_id)
    if not current_track_genres:
        print("No genres found for the current track's artist.")
        return None
    print(f"current genre {current_track_genres}")
    
    match_scores = []
    genre_cache = {}
    for i,artist_id in enumerate(df["artist_id"]):
        if artist_id in genre_cache:
            album_track_genres = genre_cache[artist_id]
        else:
            album_track_genres = artist_togenres(token=token,artist_id=artist_id)
            genre_cache[artist_id] = album_track_genres
            
        # print(album_track_genres)
        common = set(current_track_genres) & set(album_track_genres)
        match_count = len(common)
        if match_count > 0:
            weight = (match_count * 2) + (df.iloc[i,2] / 10) + (2025 - df.iloc[i,5])
            match_scores.append((i,weight))
            
    if not match_scores:
        print("There is no matching")
        return
    match_scores.sort(key=lambda x: x[1])
    sorted_indexes= [idx for idx,_ in match_scores]
    
    return df.iloc[sorted_indexes]
suggest_df = genre_match(df=df)

def calculate_song_score(match_count, popularity, release_year):
    return (match_count * 2) + (popularity / 10) + (2025 - release_year)

def start_song(token,df):
    play_url = "https://api.spotify.com/v1/me/player/play"
    header = {
        "Authorization":f"Bearer {token}"
    }
    data = {
        "uris":list(df.iloc[:,0])
    }
    response = requests.put(play_url,headers=header,json=data)
    if response.status_code != 200:
        print(response.text)
start_song(token=token,df=suggest_df)

def skip_next(token):
    next_url = "https://api.spotify.com/v1/me/player/next"
    header = {
        "Authorization":f"Bearer {token}"
    }
    response = requests.post(next_url,headers=header)
    if response.status_code !=200:
        print(response.text)
skip_next(token=token)

def change_volume(token,volume:int):
    volume_url = f"https://api.spotify.com/v1/me/player/volume?volume_percent={volume}"
    header = {
        "Authorization":f"Bearer {token}"
    }
    response = requests.put(volume_url,headers=header)
    if response.status_code !=200:
        print(response.text)
change_volume(token=token,volume=40)
