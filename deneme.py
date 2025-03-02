import os
from dotenv import load_dotenv
import dotenv
import requests
import pandas as pd

class sanatci:
    def __init__(self):
        self.search_url = "https://api.spotify.com/v1/search"
        load_dotenv("C:\\Users\\şerefcanmemiş\\Documents\\Projects\\spoti\\.env")
        self.token=os.getenv("TOKEN")

    def get_artists_genres(self,artist_id):
        top_tracks_url = f"https://api.spotify.com/v1/artists/{artist_id}"
        header = {"Authorization":f"Bearer {self.token}"}
        response = requests.get(top_tracks_url,headers=header)
        if response.status_code == 200:
            return response.json()
        else:
            print(response.text)


    def search_artists(self,genres,limit):
        header = {
            "Authorization":f"Bearer {self.token}"
            }
        params={
            "q":" ".join(genres),
            "type":"artist",
            "limit":limit
        }
        response = requests.get(self.search_url,headers=header,params=params)
        return response.json().get("artists").get("items")

    def artist_df(self,artist_ids):
        df = pd.DataFrame(columns=(["id","name","genres","followers","popularity"])).astype("object")
        
        headers = {
            "Authorization":f"Bearer {self.token}"
        }
        for artist_id in artist_ids:
            url =f"https://api.spotify.com/v1/artists/{artist_id}"
            artist = requests.get(url=url,headers=headers).json()
        
            followers=artist.get("followers").get("total")
            genres=artist.get("genres")
            name=artist.get("name")
            popularity0_100=artist.get("popularity")
            artist_id=artist.get("id")

            save = {
                "id":artist_id,
                "name":name,
                "genres":genres,
                "followers":followers,
                "popularity":popularity0_100
            }
            
            df.loc[len(df)] = save
            
        return df
    
    
    def get_artist_id(self,artist_name):
        headers = {
            "Authorization": f"Bearer {self.token}"
        }
        params = {
            "q": artist_name,
            "type": "artist",
            "limit": 1 
        }

        response = requests.get(self.search_url, headers=headers, params=params)
        if response.status_code == 200:
            artists = response.json().get("artists", {}).get("items", [])
            if artists:
                return artists[0]["id"]
        return None

    def ids(self,genres=["rock"],limit=10):
        ids = []
        artists = self.search_artists(genres=genres,limit=limit)
        for artist in artists:
            name = artist.get("name")
            ids.append(self.get_artist_id(artist_name=name))
        return ids


sanat = sanatci()
ids=sanat.ids(genres=["rock"],limit=50)
sanat.artist_df(ids)
    
    
    
def get_artists_top_tracks(artist_id,access_token):
    top_tracks_url = f"https://api.spotify.com/v1/artists/{artist_id}/top-tracks"
    header = {
        "Authorization":f"Bearer {access_token}"
        }
    params = {
        "market":"TR"
        }
    response = requests.get(top_tracks_url,headers=header,params=params)
    if response.status_code == 200:
        return response.json().get("tracks")
    else:
        print(response.text)
#top_tracks= get_artists_top_tracks(artist_id=artist_id,access_token=token)

top_songs=[]
#for i in top_tracks:
#    top_songs.append([i.get("name"),i.get("popularity")])
#top_songs

