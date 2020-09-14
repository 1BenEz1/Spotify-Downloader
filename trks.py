import requests, os
from bs4 import BeautifulSoup as bs

class Tracks:

    user_id = ''
    playlist = ''
    soup = ''
    
    # Get the playlist
    def __init__(self, user_id):
        self.user_id = user_id
        os.chdir(f'{self.user_id}') # enter dir
        f = open(f'{self.user_id}.txt','r').readlines()
        os.chdir(os.pardir) # exit dir
        self.playlist = f[1]
        response = requests.get(self.playlist)
        self.soup = bs(response.content,'html.parser')

    # Private method to check if the song was already downloaded
    def __present(self, file, name, artist):
        lines = file.readlines()
        s = f'{name} by {artist}'+'\n'
        ret = s in lines
        file.close()
        return ret

    # returns the tracks that wasn't downloaded already
    def getTracks(self):
        songs = []
        os.chdir(f'{self.user_id}') # enter dir
        file = open('tracks.txt','a+')
        tracks = self.soup.find_all('div', attrs={'class':"tracklist-col name"})
        for t in tracks:
            txt = t.find_all('span',attrs={'dir':'auto'})
            name = txt[0].text
            artist = txt[1].text
            if not self.__present(open('tracks.txt','r'), name, artist):
                songs.append({'name':name , 'artist':artist})
                file.write(f'{name} by {artist}'+'\n')
        file.close()
        os.chdir(os.pardir) # exit dir
        return songs

    # delete the records of downloaded songs
    def forget(self):
        os.chdir(f'{self.user_id}') # enter dir
        os.remove('tracks.txt')
        os.chdir(os.pardir) # exit dir