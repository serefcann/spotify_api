from flask import Flask, render_template, jsonify, request
import os
from spotify_db import spotify_db
from track_visualization import visual
import json
import plotly
#from tok import Token
app = Flask(__name__)


@app.route("/")
def index():
    return render_template('index.html')

@app.route("/fetch-tracks",methods=["POST"])
def fetch_tracks():
    try:
        spotify = spotify_db()
        tracks_to_store = spotify.get_nonoverlapping_tracks()
        if not tracks_to_store:
            return jsonify({'message': 'No new tracks to store'})
        
        return jsonify({"message": "New tracks found. Do you want to store them?", "tracks": tracks_to_store})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/store-tracks",methods=["POST"])
def store_tracks():
    try:
        spotify = spotify_db()
        spotify.store_tracks(tracks_to_store=spotify.get_nonoverlapping_tracks())
        spotify.artists_genres_store()
        return jsonify({"message": "New tracks successfully stored"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@app.route('/analysis')
def analysis():
    return render_template('analysis.html')
    
@app.route("/get-plot",methods=["POST"])
def get_plot():
    data = request.json
    plot_type = data.get('chart-type')
    theme = data.get("theme")
    vis = visual()
    if plot_type == "artists":
        data = [vis.most_listened_artists()]
    elif plot_type == "genres":
        data = [vis.most_listened_genres()]
    elif plot_type == "songs":
        data = [vis.most_listened_songs()]
    else:
        data = []
    if theme == "dark":
        data[0] = data[0].update_layout(template="plotly_dark")
    else:
        data[0] = data[0].update_layout(template ="simple_white" )
    graphJSON = json.dumps(data[0],cls=plotly.utils.PlotlyJSONEncoder)
    return jsonify({"graph": graphJSON})

if __name__ == '__main__':
    app.run(debug=True)

