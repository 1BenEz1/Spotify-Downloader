from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
import youtube_dl

class Ytb:

    """
        Selenium part
    """
    options = Options()
    options.binary_location = 
    driver_path = 

    links = []

    def __init__(self, songs):

        # Opening the browser and going to youtube
        driver = webdriver.Chrome(options = self.options, executable_path = self.driver_path)
        url = 'https://www.youtube.com/results?search_query='

        # Searcing links for each songs and appending them to the links list
        self.links = []
        
        for song in songs:
            search = song['name']+'+by+'+song['artist']+' official audio'
            driver.get(url+search)
            href = driver.find_element_by_xpath("//a[@id='video-title']").get_attribute('href')
            self.links.append({'name': song['name'], 'href':href})

        # Closing the browser
        driver.close()

    def downloadSongs(self, user_id):

        """
            YouTube DL part
        """
        path_list = []

        #os.chdir(f'{self.user_id}') # enter dir

        for link in self.links:
            video_info = youtube_dl.YoutubeDL().extract_info(url = link['href'], download = False)
            filename = f"{link['name']}.mp3"

            path = f'{user_id}/{filename}'
            path_list.append(path)

            yt_options = {
                'format': 'bestaudio/best',
                'keepvideo': False,
                'outtmpl': path,
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': '192'
                }]
            }
            with youtube_dl.YoutubeDL(yt_options) as ydl:
                ydl.download([video_info['webpage_url']])
        
        return path_list

