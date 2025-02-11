import os
from dotenv import load_dotenv
import dotenv
import requests
import pandas as pd

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
    df = pd.DataFrame(columns=(["song_id","song_name","song_popularity","song_artist","artist_id"]))
    
    for songs in album_song:
        for song in songs:
            song_name = song.get("track").get("name")
            song_id = song.get("track").get("id")
            song_pop = song.get("track").get("popularity")
            song_artist = song.get("track").get("artists")[0].get("name")
            artist_id = song.get("track").get("artists")[0].get("id")
            save = {
                "song_id":song_id,
                "song_name":song_name,
                "song_popularity":song_pop,
                "song_artist":song_artist,
                "artist_id":artist_id
            }
            df.loc[len(df)] = save
    return df
df=song_df(album_song=album_song)


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
artist_togenres(token=token,artist_id="72YIDLCAmSi6zavbWIIhUD")

def genre_match(df):
    current_track_genres = artist_togenres(token=token,artist_id=last_track_artist_id)
    if not current_track_genres:
        print("No genres found for the current track's artist.")
        return None
    print(f"current genre {current_track_genres}")
    
    index_list = []
    prior_list = []
    genre_cache = {}
    for i,artist_id in enumerate(df["artist_id"]):
        if artist_id in genre_cache:
            album_track_genres = genre_cache[artist_id]
        else:
            album_track_genres = artist_togenres(token=token,artist_id=artist_id)
            genre_cache[artist_id] = album_track_genres
            
        # print(album_track_genres)
        common = set(current_track_genres) & set(album_track_genres)
        if common and len(common)<2:
            index_list.append(i)
        if len(common)>= 2:
            prior_list.append(i)
            
    if len(index_list) == 0:
        print("There is no matching")
        return
    combined_indices = prior_list + index_list
    
    return df.iloc[prior_list[:20]]
genre_match(df=df)





