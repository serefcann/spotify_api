from spotify_db import spotify_db
import mysql.connector
import pandas as pd

spotify = spotify_db()
conn = spotify.conn
mycursor = spotify.mycursor

mycursor.execute("SELECT * FROM spotify_track\
                        ORDER BY saved_at DESC LIMIT 40")
results = mycursor.fetchall()
df=pd.DataFrame(columns=["name","artist","artist_id","popularity","release_date","saved_at"],data=results)
print(df)