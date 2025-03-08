from spotify_db import spotify_db
import mysql.connector
import pandas as pd
import plotly
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import os
from dotenv import load_dotenv
import json

class visual():
    def __init__(self):
        load_dotenv("C:\\Users\\şerefcanmemiş\\Documents\\Projects\\spoti\\.env")
        self.PASSWORD = os.getenv("PASSWORD")
        self.conn = self.connect_db()
        self.mycursor = self.conn.cursor()
        
    
    def connect_db(self):
        mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password=self.PASSWORD,
        database="spotify")
        return mydb

    def most_listened_artists(self):
        query = """
        SELECT artist,count(artist) as track_count FROM spotify_track
        GROUP BY artist
        ORDER BY track_count DESC LIMIT 10
        """
        self.mycursor.execute(query)
        data = self.mycursor.fetchall()
        df = pd.DataFrame(columns=["artist","track_count"],data=data)
        plt.figure(figsize=(12,6))
        fig = px.bar(df, x='track_count', y='artist', orientation='h',
                    title="My Top Artists",
                    text_auto=True, color='track_count',
                    color_continuous_scale='magma',
                    template="simple_white",
                    category_orders={"artist": df.sort_values("track_count", ascending=False)["artist"].tolist()})

        return fig

    def most_listened_songs(self):
        query = """
        SELECT t.name, count(t.name) as track_count, group_concat(distinct g.genre separator ', ') as genres 
        FROM spotify_track t 
        left join spotify_artist_genres g 
        on t.artist_id = g.artist_id
        group by t.name
        ORDER BY track_count DESC LIMIT 10
        """
        self.mycursor.execute(query)
        data = self.mycursor.fetchall()
        df = pd.DataFrame(columns=["track_name","track_count","genres"],data=data)
        plt.figure(figsize=(12,6))
        fig = px.bar(df, x='track_count', y='track_name', orientation='h',
                    title="My Top Songs",
                    text_auto=True, color='track_count',
                    color_continuous_scale='Plasma',
                    template="simple_white",
                    category_orders={"track_name": df.sort_values("track_count", ascending=False)["track_name"].tolist()})

        return fig

    def most_listened_genres(self):
        query = """
        SELECT g.genre,count(g.genre) as genre_count
        FROM spotify_track t 
        RIGHT JOIN spotify_artist_genres g 
        on t.artist_id = g.artist_id
        GROUP BY g.genre
        ORDER BY genre_count DESC LIMIT 10
        """
        self.mycursor.execute(query)
        data = self.mycursor.fetchall()
        df = pd.DataFrame(columns=["genre","genre_count"],data=data)
        plt.figure(figsize=(12,6))
        fig = px.pie(df,values="genre_count",
                     names="genre",
                     title="Top 10 Genres Listened",
                     height=550,
                     template="simple_white",)
        fig.update_traces(textposition="inside",textinfo="percent+label")
        return fig

