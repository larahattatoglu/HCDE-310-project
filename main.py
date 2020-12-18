
import urllib.parse, urllib.request, urllib.error, json
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import random
from flask import Flask,render_template,request
import logging

client_id = '080e9520ae984128b3cc1a637f03a5d7'
client_secret = '7b67094c1fdd4c2dab440864bb17fc39'

client_credentials_manager = SpotifyClientCredentials(client_id, client_secret)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

fitness_dict = {'Stretch': {'stretching'},'Strength':{'Squats','Weight Lifting','Push-ups','Bench Press','Deadlift', 'Overhead Press','Pull Ups' },'Cardio':{'Jump Rope', 'Swimming', 'Dancing','Running','Boxing','Cycling','Rowing','Stairs'},'Cooldown':{'Stretching','Light Jogging','yoga'}}

app = Flask(__name__)

#@app.route("/")

#def hello():
    #return "<!DOCTYPE html><html><body>Welcome! Please input your workout activity to receive a playlist </body></html>"

@app.route("/")
def main_handler():
    app.logger.info("In MainHandler")
    return render_template('greetform.html',page_title="Greeting Form")



#rack_id = []
#for i in range(0,200,50):
    #track_results = sp.search(q='year:2020', offset = 0, type='track', limit=50, market = None)
    #for i, t in enumerate(track_results['tracks']['items']):
        #track_id.append(t['id'])

def getTrackFeatures(id):
    track = {}
    for x in id:
        features = sp.audio_features(x)
        danceability = features[0]['danceability']
        energy = features[0]['energy']
        liveness = features[0]['liveness']
        loudness = features[0]['loudness']
        tempo = features[0]['tempo']
        valence = features[0]['valence']
        if x not in track.keys():
            track[x] = {'valence': valence,'danceability':danceability,'energy':energy,'liveness':liveness,'loudness':loudness,'tempo':tempo}
    return track




def Categorize(trackdict,category):
    playlist = []
    if category == 'Cardio':
        for x in trackdict:
            if trackdict[x]['tempo'] > 120:
                playlist.append(x)
    if category == 'Strength':
        for x in trackdict:
            if trackdict[x]['tempo'] > 80:
                if trackdict[x]['danceability'] > 0.75:
                    playlist.append(x)
    if category == 'Stretch/Cooldown':
        for x in trackdict:
            if trackdict[x]['tempo'] < 80 and trackdict[x]['tempo'] > 60:
                playlist.append(x)


 
    return playlist


    #eturn playlist

#idsCat = Categorize(x,userinput)
#idsCat = Categorize(x,'Stretch')
#print(type(idsCat))

def getTrackName(ids):
    tracklist = []
    for x in ids:
        data = sp.track(x)
        tracklist.append(data['name'])

    return tracklist

#z = []

#for i in range(20):
    #x = random.choice(idsCat)
    #if x not in z:
        #z.append(x)

#finalPlaylist = getTrackName(z)
#print(finalPlaylist)


@app.route('/gresponse')
def greet_response_handler():
    workout = request.args.get('workout')
    year = request.args.get('year')
    app.logger.info(workout)
    app.logger.info(year)
    track_id = []
    a = 'year:'
    b = year
    c = a + b
    for i in range(0, 300, 50):
        track_results = sp.search(q=c, offset=0, type='track', limit=50, market=None)
        for i, t in enumerate(track_results['tracks']['items']):
            track_id.append(t['id'])
    x = getTrackFeatures(track_id)
    userworkout = Categorize(x, workout)
    z = []
    for i in range(50):
        x = random.choice(userworkout)
        if x not in z:
            z.append(x)
    finalPlaylist = getTrackName(z)
    return render_template('gresponse.html',fplaylist = finalPlaylist)

if __name__ =="__main__":
    app.run(host="localhost", port=8080, debug=True)

