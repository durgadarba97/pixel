# serves as the application entry point. 
import spotipy
import time
from spotipy.oauth2 import SpotifyOAuth
from pixel.state import State
import requests
from PIL import Image
from pixel.configs import height, width, client_id, client_secret, redirect_uri, scope, cache_path
import os

# a dumb name but i'll get back to it.
class Spotify(State):
    def __init__(self):
        self.spotify = SpotifyOAuth(
            client_id = client_id,
            client_secret = client_secret,
            redirect_uri = redirect_uri,
            scope = scope,
            cache_path = cache_path)
        
        
        self.tokeninfo = self.spotify.get_access_token(check_cache=True)

    #  checks if token is expired and gets new token
    def checkExpired(self):
        now = int(time.time())
        isexpired = (self.tokeninfo['expires_at'] - now < 3600)

        # if it's expired, set new Token
        if(isexpired):
            self.token = self.spotify.refresh_access_token(self.tokeninfo['refresh_token'])

    def getTrack(self):
        self.checkExpired()

        # I would make this a class object but the access token get refreshed so many times, 
        # it feels right, here. 
        sp = spotipy.Spotify(self.tokeninfo['access_token'])
        
        return sp.current_user_playing_track()

    # If get track returns none, we'll return an image form the internet. 
    def getTrackImage(self):
        current_track = self.getTrack()
        # print(current_track)
        if(current_track is None):
            return None

        return current_track['item']['album']['images'][0]['url']
    
    # get audio analysis 
    def getAudioAnalysis(self):
        current_track = self.getTrack()
        sp = spotipy.Spotify(self.tokeninfo['access_token'])
        
        if(current_track is None):
            return None
        
        print(sp.audio_analysis(current_track['item']['id']))
    
    # is track playing
    def isPlaying(self):
        current_track = self.getTrack()
        if(current_track is None):
            return False
        return current_track['is_playing']


    def compareimages(self, image1, image2):
        if(image1 == image2):
            return True
        return False

    def saveGrid(self, imageurl):

        image = Image.open(requests.get(imageurl, stream=True).raw)
        image = self.downsample(image)
        filename = "./output/gifs/" + self.toString() +".png"
        image.save(filename)
        return (0, self.toString()+".png")

    # downsample the image to 64x64 pixels and return the image
    def downsample(self, image):
        return image.resize((height, width), Image.ANTIALIAS)


    # returns the current track name
    def getTrackName(self):
        current_track = self.getTrack()
        # print(current_track)
        if(current_track is None):
            return None
            
        return current_track['item']['name']

    def toString(self):
        return "spotify"
    
    def generateFrames(self, numframes = 0, duration = 0):
        imageurl = self.getTrackImage()
        return self.saveGrid(imageurl)
    

        


