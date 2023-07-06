import kivy
from kivymd.app import MDApp
from kivymd.uix.boxlayout import MDBoxLayout
import re
import pafy
from kivy.core.audio import SoundLoader
import googleapiclient
import vlc

kivy.require('1.9.0')

class video_audio_player:
    def __init__(self):
        self.instance = vlc.Instance()
        self.player = self.instance.media_player_new()

    def play(self, id):
        # Create new pafy obj video
        video = pafy.new(id)
        
        # Extract best audio from video
        audio_stream = video.getbestaudio()

        # Retrive audio url
        audio_url = audio_stream.url
        
         # Play audio using python-vlc 
        media = self.instance.media_new(audio_url)
        self.player.set_media(media)

        self.player.play()
        # while self.player.is_playing():
        #     pass
    def stop(self):
        self.player.stop()

class Music(MDBoxLayout):
    # Construtor
    def __init__(self, **kwargs):
        super(Music, self).__init__(**kwargs)

    # Retrive URL from InputField
    def start_music(self):

        # Retrive Value from url input
        self.url = self.ids.url.text
        
        # Validating url
        if not self.url:
            return

        # Retrive ID from URL
        id = check_video_or_playlist(self.url)
        if not id:
            return 
    
        if id["type"] == "video":
            player = video_audio_player()
            player.play(id["id"])

        elif id["type"] == "playlist":
            pass
        

# Application
class YoutubeMusicPlayer(MDApp):

    # Function to return the UI
    def build(self):
        return Music()


# playlist pattern https://youtube.com/playlist?list=PLOxu-EtycI1lOoGBpE508PuvBsGHLOihJ
# video pattern https://youtu.be/_n_swXU3XEs

# Check URL id video or playlist 
def check_video_or_playlist(url: str) -> dict:
    
    # Check if url match playlist or video url and capture ID in ()
    video_url_pattern = r"^https://youtu.be/([a-zA-Z0-9_-]+)$"
    playlist_url_pattern = r"^https://youtube.com/playlist\?list=([a-zA-Z0-9_-]+)$"
    
    # Check wethere url is playlist or video
    video_match = re.match(video_url_pattern, url)
    playlist_match = re.match(playlist_url_pattern, url)
    
    # print(video_match.group(1))
    if video_match:
        result = {
            "type": "video",
            "id": video_match.group(1)
        }
        return result
        
    elif playlist_match:
        result = {
            "type": "playlist",
            "id": playlist_match.group(1)
        }
        return result
    
    # Not a youtube url
    else:
        return False

if __name__ == '__main__':
    YoutubeMusicPlayer().run()