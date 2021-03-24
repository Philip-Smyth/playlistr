import os
import sys
import json
import math
import random
import spotipy
import webbrowser
import spotipy.util as util
from json.decoder import JSONDecodeError

def chunks(lst, n):
    """Yield successive n-sized chunks from lst."""
    for i in range(0, len(lst), n):
        yield lst[i:i + n]

def selectTracks(results):
    songBatchNum = len(results['items']) / 2 if len(results['items']) < 5 else 5
    songs = random.sample(results['items'], k=songBatchNum)
    songList = []
    for song in songs:
        songList.append(song['track']['id'])
    return songList

def gatherTodaysSongs():
    results = spotifyObject.current_user_saved_tracks(1) #initial small call to get total
    trackTotal = results['total']
    batchNumber = math.ceil(trackTotal / 15)

    songList = []

    for batch in range(batchNumber):
        results = spotifyObject.current_user_saved_tracks(15, batch*15)
        batchResult = selectTracks(results)
        songList = songList + batchResult
    return songList

# Get the username from terminal
username = sys.argv[1]
scope = 'playlist-read-private playlist-modify-public user-library-read'

# Erase cache and prompt for user permission
try:
    token = util.prompt_for_user_token(username, scope) # add scope
except (AttributeError, JSONDecodeError):
    os.remove(f".cache-{username}")
    token = util.prompt_for_user_token(username, scope) # add scope

# Create our spotify object with permissions
spotifyObject = spotipy.Spotify(auth=token)
user_id = spotifyObject.me()['id']

#### Running request and randomizing the way that I am, an explanation #####

# The solution here is tied completely to me as the user. I tend to 
# add songs in bulk, whether it is an album or a playlist with similar
# music altogether. I wanted a way to avoid multiple songs from the same
# album or the same general genre, without the heavy work of pulling, 
# ordering and choosing the data. This ensures a relativly efficient solution
# At least until we add a DB

playlists = spotifyObject.current_user_playlists(limit=50)
playlistId = ''
playlistPresent = False
for i, item in enumerate(playlists['items']):
    if 'DailySoundtrack' in item['name']:
        playlistPresent = True
        playlistId = item['id']

if playlistPresent:
    songList = gatherTodaysSongs()
    songListLength = len(songList)
    spotifyObject.playlist_replace_items(playlistId, [])
    if songListLength >= 100:
        chunkedSongs = list(chunks(songList, 100))
    for i, chunk in enumerate(chunkedSongs):
        spotifyObject.playlist_add_items(playlistId, chunkedSongs[i])

else:
    # Create the soundtrack for the first time
    spotifyObject.user_playlist_create(user_id, "DailySoundtrack") #creating a soundtrack
    playlists = spotifyObject.current_user_playlists(limit=50)
    for i, item in enumerate(playlists['items']):
        if 'DailySoundtrack' in item['name']:
            playlistId = item['id']

    # Add to the playlist for today
    songList = gatherTodaysSongs()
    songListLength = len(songList)
    if songListLength >= 100:
        chunkedSongs = list(chunks(songList, 100))
    for i, chunk in enumerate(chunkedSongs):
        spotifyObject.playlist_add_items(playlistId, chunkedSongs[i])
#
# Next steps:
# Next thing will be to add the song Id's to a DB, and generate the new list
# from that database. The only check then that will be needed is the total song
# count, and if this changes, then we can simply recall the songs and update the DB
#


