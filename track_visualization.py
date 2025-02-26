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
mycursor.execute("SELECT * FROM spotify_track ORDER BY saved_at DESC LIMIT 40")
mycursor.fetchall()

#mycursor.execute(f"SELECT * FROM spotify_track\
 #                       WHERE saved_at {datetime.datetime.now()-datetime.timedelta(days=1)} 
  #                      ORDER BY saved_at DESC")

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


query = """
SELECT name,count(name) as track_count FROM spotify_track
GROUP BY name
ORDER BY track_count DESC LIMIT 10
"""
mycursor.execute(query)
data = mycursor.fetchall()
df = pd.DataFrame(columns=["track_name","track_count"],data=data)
plt.figure(figsize=(12,6))
fig = px.bar(df, x='track_count', y='track_name', orientation='h',
             title="My Top 10 Most Listened Songs",
             text_auto=True, color='track_count',
             color_continuous_scale='Plasma',
             category_orders={"track_name": df.sort_values("track_count", ascending=False)["track_name"].tolist()})

fig.show()