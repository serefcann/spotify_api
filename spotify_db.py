from dotenv import load_dotenv
import pandas as pd
import mysql.connector
import datetime
from track import recently_played_track
import os
import requests

class spotify_db:
    def __init__(self):
        load_dotenv("C:\\Users\\şerefcanmemiş\\Documents\\Projects\\spoti\\.env")
        self.conn = self.connect_db()
        self.mycursor = self.conn.cursor()
        self.token = os.getenv("TOKEN")

    def connect_db(self):
        mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password=os.getenv("PASSWORD"),
        database="spotify")
        return mydb

    def create_table(self):
        self.mycursor.execute("CREATE TABLE IF NOT EXISTS \
            spotify_track (name VARCHAR(255), \
            artist VARCHAR(255),\
            artist_id VARCHAR(255), \
            popularity INT,\
            release_date DATE\
            saved_at DATETIME)")

    def get_past_batch(self):
        self.mycursor.execute("SELECT name FROM spotify_track\
                        ORDER BY saved_at DESC LIMIT 40")
        rows = self.mycursor.fetchall()
        return rows
    
    def get_nonoverlapping_tracks(self):
        new_batch = recently_played_track(token=os.getenv("TOKEN"),limit=50)
        past_batch = self.get_past_batch()
        
        if not past_batch or not new_batch:
            print("Either past_batch or new_batch is empty")
            return new_batch
        
        nonmatch_list = []
        index,same_track,i = 0,0,0
        
        if past_batch[0][0] != new_batch[0][0]:
            while index < len(new_batch) and i < len(past_batch):
                if past_batch[i][0] != new_batch[index][0]:
                    nonmatch_list.append(new_batch[index])
                    index += 1         
                else:
                    index += 1
                    same_track +=1
                    i +=1
                if same_track >=5:
                    break
                if index >= len(new_batch):
                    i +=1
                    index = 0
        else:
            print("already all tracks matched")
            return []
        if len(nonmatch_list) > 50:
            return new_batch
        df = pd.DataFrame(data=nonmatch_list)
        print(df)
        return nonmatch_list
        
    
    def store_tracks(self,tracks_to_store):
        
        if not tracks_to_store:
            print("there are no new tracks to store")
            return
        
        insertion = """INSERT INTO spotify_track (name, artist, artist_id, popularity, release_date, saved_at) 
                       VALUES (%s, %s, %s, %s, %s, %s)"""
        
        # Veritabanına şarkıları ekleme
        self.mycursor.executemany(insertion, tracks_to_store)
        self.conn.commit()
            
    def get_several_artists(self,db_ids):
        artist_url = f"https://api.spotify.com/v1/artists/"
        params = {"ids":",".join(db_ids)}
        header = {
                "Authorization":f"Bearer {self.token}"
            }
        response = requests.get(artist_url,headers=header,params=params)
        
        if response.status_code != 200:
            print(response.text)
            
        artists_data = response.json().get("artists")
        if not artists_data:
            print("API returned no artist data.")
            return
        return artists_data
           
    def artists_genres_store(self):
        self.mycursor.execute("""
            SELECT DISTINCT t.artist_id
            FROM spotify_track t
            LEFT JOIN spotify_artist_genres g
            ON t.artist_id = g.artist_id
            WHERE g.artist_id IS NULL
        """)
        rows = self.mycursor.fetchall()
        nonexist_indb_artistids = set(row[0] for row in rows)
        db_ids = list(nonexist_indb_artistids)
        
        print(f"Length of the db_ids is {len(db_ids)}")
        
        if not db_ids:
            print("No new artists to update.")
            return
            
        artists_data = self.get_several_artists(db_ids=db_ids)
        
        artist_ids_genres = []
        for artist in artists_data:
            artist_id = artist.get("id")
            artist_genres = artist.get("genres",None)
            
            if artist_genres:
                for genre in artist_genres:
                    artist_ids_genres.append((artist_id,genre))
                    
        if artist_ids_genres:
            insertion = """INSERT INTO spotify_artist_genres (artist_id, genre) VALUES (%s, %s)"""
            self.mycursor.executemany(insertion, artist_ids_genres)
            self.conn.commit()
            print("Genres stored successfully!")
            self.mycursor.close()
            self.conn.close()
            
if __name__  == "__main__":
    spotify=spotify_db()
    spotify.store_tracks()
    spotify.artists_genres_store()
    


    


