# spotify_api# Spotify Listening History Analysis

## Overview

This project fetches your recently played tracks from Spotify, stores them in a database, and provides visual insights into your listening habits using interactive plots. You can analyze:

- Your **most listened genres** (pie chart)
- Your **top 10 most listened artists** (bar chart)
- Your **top 10 most played tracks** (bar chart)

The project uses **Flask** for the web interface, **MySQL** for storing data, and **Plotly** for data visualization.

---

## Features

### 1. Fetch and Store Tracks

- Fetches recently played tracks from Spotify.
- Avoids duplicate storage by checking existing tracks.
- Stores relevant track details (name, artist, popularity, release date, etc.).

### 2. Genre Analysis

- Retrieves stored tracks and their associated genres.
- Displays a **pie chart** showing the distribution of genres you listen to the most.

### 3. Artist and Track Analysis

- Shows a **bar chart** of the top 10 most listened artists.
- Shows a **bar chart** of the top 10 most played tracks.

### 4. Web Interface

- A Flask-based web app that allows users to:
  - Fetch new tracks.
  - View data visualizations.

---

## How It Works

### **Fetch Tracks Algorithm**

1. **Spotify API Request:** The app makes an API call to fetch the recently played tracks.
2. **Duplicate Check:** It compares new tracks with those already stored in the database.
3. **Storage Decision:** If new tracks exist, it asks the user whether they want to store them.
4. **Database Insertion:** If confirmed, the new tracks are inserted into the MySQL database.

#### **Code Breakdown:**

```python
@app.route("/fetch-tracks", methods=["POST"])
def fetch_tracks():
    spotify = spotify_db()
    tracks_to_store = spotify.get_nonoverlapping_tracks()
    
    if not tracks_to_store:
        return jsonify({'message': 'No new tracks to store'})
    
    return jsonify({"message": "New tracks found. Do you want to store them?", "tracks": tracks_to_store})
```

---

## Database Schema

### **Tables Used**

| Table Name              | Description                                            |
| ----------------------- | ------------------------------------------------------ |
| `spotify_track`         | Stores track details (name, artist, popularity, etc.). |
| `spotify_artist_genres` | Stores artist IDs and their associated genres.         |

---

## Data Visualizations

### **1. Most Listened Genres (Pie Chart)**

- Displays the distribution of genres based on the stored tracks.
- Uses Plotly to create an interactive visualization.

**Code:**

```python
def most_listened_genres(mycursor):
    query = """
    SELECT g.genre, COUNT(g.genre) AS genre_count
    FROM spotify_track t
    RIGHT JOIN spotify_artist_genres g ON t.artist_id = g.artist_id
    GROUP BY g.genre
    ORDER BY genre_count DESC LIMIT 10
    """
    mycursor.execute(query)
    data = mycursor.fetchall()
    df = pd.DataFrame(columns=["genre", "genre_count"], data=data)
    fig = px.pie(df, values="genre_count", names="genre", title="Top 10 Most Listened Genres")
    fig.show()
```

### **2. Most Listened Artists (Bar Chart)**

- Displays the top 10 artists you have listened to the most.

**Code:**

```python
def most_listened_artists(mycursor):
    query = """
    SELECT artist, COUNT(artist) AS track_count FROM spotify_track
    GROUP BY artist
    ORDER BY track_count DESC LIMIT 10
    """
    mycursor.execute(query)
    data = mycursor.fetchall()
    df = pd.DataFrame(columns=["artist", "track_count"], data=data)
    fig = px.bar(df, x='track_count', y='artist', orientation='h',
                 title="Top 10 Most Listened Artists",
                 text_auto=True, color='track_count',
                 color_continuous_scale='magma')
    fig.show()
```

---

## How to Run the Project

### **1. Install Dependencies**

```sh
pip install flask mysql-connector-python pandas plotly
```

### **2. Set Up Database**

- Create the required tables in your MySQL database.

### **3. Run the Flask App**

```sh
python app.py
```

- Open `http://127.0.0.1:5000` in your browser.

### **4. Fetch and Store Tracks**

- Click the "Fetch Tracks" button.
- View fetched tracks and confirm storage.

### **5. View Data Visualizations**

- Click buttons to display genre, artist, and track insights.

---

## Screenshots (Add Your Screenshots Here)

### 🎵 Fetch Tracks Page

*Example screenshot of the fetch tracks button*

### 📊 Most Listened Genres (Pie Chart)

![alt text](mostListenedGenres.png)

### 📈 Most Listened Artists (Bar Chart)

![alt text](mostListenedArtists.png)

### 📈 Most Listened Songs (Bar Chart)

![alt text](mostListenedSongs.png)

---

## Future Improvements

- **Improve UI**: Add styling and interactive elements.
- **Advanced Filtering**: Allow users to filter by date range.
- **Spotify Playlist Analysis**: Extend functionality to analyze playlists.

---

## Contributors

- **Seref Can** - Developer

Feel free to contribute by submitting a pull request! 🚀

