from spotify_db import spotify_db
import mysql.connector
import pandas as pd
import datetime
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import os


def connect_db():
    mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password=os.getenv("PASSWORD"),
    database="spotify")
    return mydb

conn = connect_db()
mycursor = conn.cursor()
def most_listened_artists(mycursor):
    query = """
    SELECT artist,count(artist) as track_count FROM spotify_track
    GROUP BY artist
    ORDER BY track_count DESC LIMIT 10
    """
    mycursor.execute(query)
    data = mycursor.fetchall()
    df = pd.DataFrame(columns=["artist","track_count"],data=data)
    plt.figure(figsize=(12,6))
    fig = px.bar(df, x='track_count', y='artist', orientation='h',
                title="My Top 10 Most Listened Artists",
                text_auto=True, color='track_count',
                color_continuous_scale='magma',
                category_orders={"artist": df.sort_values("track_count", ascending=False)["artist"].tolist()})

    fig.show()
most_listened_artists(mycursor=mycursor)


query = """
SELECT t.name, count(t.name) as track_count, group_concat(distinct g.genre separator ', ') as genres 
FROM spotify_track t 
left join spotify_artist_genres g 
on t.artist_id = g.artist_id
group by t.name
ORDER BY track_count DESC LIMIT 10
"""
mycursor.execute(query)
data = mycursor.fetchall()
df = pd.DataFrame(columns=["track_name","track_count","genres"],data=data)
plt.figure(figsize=(12,6))
fig = px.bar(df, x='track_count', y='track_name', orientation='h',
             title="My Top 10 Most Listened Songs",
             text_auto=True, color='track_count',
             color_continuous_scale='Plasma',
             category_orders={"track_name": df.sort_values("track_count", ascending=False)["track_name"].tolist()})

fig.show()

def most_listened_genres(mycursor):
    query = """
    SELECT g.genre,count(g.genre) as genre_count
    FROM spotify_track t 
    RIGHT JOIN spotify_artist_genres g 
    on t.artist_id = g.artist_id
    GROUP BY g.genre
    ORDER BY genre_count DESC LIMIT 10
    """
    mycursor.execute(query)
    data = mycursor.fetchall()
    df = pd.DataFrame(columns=["genre","genre_count"],data=data)
    plt.figure(figsize=(6,3))
    fig = px.pie(df,values="genre_count", names="genre",title="Distribution of Song Genres Listened")
    fig.update_traces(textposition="inside",textinfo="percent+label")
    fig.show()
most_listened_genres(mycursor=mycursor)


