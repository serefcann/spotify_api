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
    
    def get_nonoverlapping_tracks(self,new_batch):
        past_batch = self.get_past_batch()
        
        if not past_batch or not new_batch:
            print("Either past_batch or new_batch is empty")
            return new_batch
        
        nonmatch_list = []
        index,same_track,i = 0,0,0
        
        if past_batch[0][0] != new_batch[0][0]:
            while index < len(new_batch) and i < len(past_batch):
                if past_batch[i][0] != new_batch[index][0]: # 0 3 1 4 
                    nonmatch_list.append(new_batch[index])
                    #print(past_batch[i][0],new_batch[index][0])
                    index += 1         
                else:
                    index += 1
                    same_track +=1
                    i +=1
                if same_track >=1:
                    break
                if index >= len(new_batch):
                    i +=1
                    index = 0
        else:
            print("already all tracks matched")
            return []
        return nonmatch_list
        
    
    def store_tracks(self,tracks_to_store):
        if not tracks_to_store:
            print("No new tracks to store.")
            return
        
        insertion = """INSERT INTO spotify_track (name, artist, artist_id, popularity, release_date, saved_at) 
                VALUES (%s, %s, %s, %s, %s, %s)"""
                
        df = pd.DataFrame(data=tracks_to_store)
        print(df)
        
        answer = input("Bu sarkilari database'de depolamak istiyorsan 'yes' istemiyorsan 'no' yaz: ")
        
        if answer == 'yes':
            self.mycursor.executemany(insertion,tracks_to_store)
            self.conn.commit()
            print("depolandi")        
        else:
            print("sarkilar depolanmadi")
            #self.conn.close()
            #self.mycursor.close()
            
    def artists_genres_store(self):
        self.mycursor.execute("""
            SELECT DISTINCT t.artist_id
            FROM spotify_track t
            LEFT JOIN spotify_artist_genres g
            ON t.artist_id = g.artist_id
            WHERE g.artist_id IS NULL
        """)
        rows = self.mycursor.fetchall()
        db_ids = set(row[0] for row in rows)
        
        if not db_ids:
            print("No new artists to update.")
            return
            
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
        artist_ids_genres = []
        
        for artist in artists_data:
            artist_id = artist.get("id")
            artist_genres = artist.get("genres",None)
            
            if not artist_genres:
                artist_ids_genres.append((artist_id,None))
            else:
                for genre in artist_genres:
                    artist_ids_genres.append((artist_id,genre))
                    
        if artist_ids_genres:
            df_to_store = pd.DataFrame(data=artist_ids_genres)
            print(df_to_store)
            
            answer = input("depolamak ister misin yes veya no: ")
            
            if answer == "yes":
                self.mycursor.execute("""
                        INSERT INTO spotify_artist_genres (artist_id, genre) 
                        VALUES (%s, %s)
                    """, (artist_id, genre))    
                self.conn.commit()
                self.conn.close()
                self.mycursor.close()
                print("sarki turleri depolandi")
            else:
                self.conn.close()
                self.mycursor.close()
                print("sarki turleri depolanmadi")

if __name__  == "__main__":
    spotify=spotify_db()
    recent_track_list = recently_played_track(token=os.getenv("TOKEN"),limit=50)
    tracks_to_store = spotify.get_nonoverlapping_tracks(new_batch=recent_track_list)
    spotify.store_tracks(tracks_to_store=tracks_to_store)
    spotify.artists_genres_store()
    


    


