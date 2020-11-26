## Python based soundtrack generator for spotify

This is a small piece of python code to generate a playlist that is random based upon my liked songs

This stemmed from some minor issues I had with the current "Daily Drive" soundtrack that spotify generates.
Mainly around repeated songs and news information that I was not interested in, so I decided to quickly create 
this to play a bit more with Python.

## Requirements

You will need to do the following:
 - You should only need to install `spotipy` using `pip` everything else ought to be standard
 - Have a spotify account, or create one
 - Setup spotify developer account 
   - Refer to https://developer.spotify.com/ for overall steps involved
   - Note: ensure you set the redirect url to something valid (e.g. "http://google.com")

## Usage
0. Pull down this repo, or simply copy paste the python code into your own `.py` file
1. Get your ClientID and ClientSecret from your developer account
2. Export these in your terminal as an environment variable
```
export SPOTIPY_CLIENT_ID='<YOUR CLIENT ID>'
export SPOTIPY_CLIENT_SECRET='<YOUR CLIENT SECRET>'

```
3. Export your redirect URL as an environment variable (ensure this matches the one defined in spotify dev account)
```
export SPOTIPY_REDIRECT_URI='<YOUR REDIRECT URL>'
```
4. Get your spotify account user ID (a 10 digit code)
5. In the terminal run the code, giving your spotify account user ID as an argument
```
python3 startNewSoundtrack.py <YOUR SPOTIFY USER ID>
```

## Next steps

Efficiency - At the moment we are making call to the spotify api at every step. Ideally I plan to add a database.
This database will store the library of liked songs, which means we can pull the song ID's directly from this like,
rather than making api calls every time we want to update the playlist. The only thing will be a small call to get 
the total number of songs, and if this differs from the total count in the db, we will then pull down the fresh data
and update the database. 

Randomization - While the randomization is decent, there is still some cases where songs from the same album. However
this is more a balance of probability along with the number of songs available to choose from. 

Consistenct - As you can see this is currently manual, down the line I would like to make this automated on the cloud or
a local machine to update the playlist at a set time every day. 
