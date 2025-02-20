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
        nonmatch_list = []
        index = 0
        same_track = 0
        i=0
        while index < len(new_batch) and i < len(past_batch):
            if past_batch[i][0] != new_batch[index][0]: # 0 3 1 4 
                nonmatch_list.append(new_batch[index])
                print(past_batch[i][0],new_batch[index][0])
                index += 1         
            else:
                index += 1
                same_track +=1
                i +=1
            if same_track >=3:
                break
            if index >= len(new_batch):
                i +=1
                index = 0
        return nonmatch_list
        
    
    def store_tracks(self,tracks_to_store):
        insertion = """INSERT INTO spotify_track (name, artist, artist_id, popularity, release_date, saved_at) 
                VALUES (%s, %s, %s, %s, %s, %s)"""
        for track in tracks_to_store:
           print(track)
        answer = input("Bu sarkilari database'de depolamak istiyorsan 'yes' istemiyorsan 'no' yaz: ")
        
        if answer == 'yes':
            self.mycursor.executemany(insertion,tracks_to_store)
            self.conn.commit()
            print("depolandi")
            self.conn.close()
            self.mycursor.close()       
        else:
            print("sarkilar depolanmadi")
            self.conn.close()
            self.mycursor.close()

if __name__  == "__main__":
    spotify=spotify_db()
    recent_track_list = recently_played_track(token=os.getenv("TOKEN"),limit=50)
    tracks_to_store = spotify.get_nonoverlapping_tracks(new_batch=recent_track_list)
    spotify.store_tracks(tracks_to_store=tracks_to_store)
    


    


