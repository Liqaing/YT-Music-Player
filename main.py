import kivy
from kivymd.app import MDApp
from kivymd.uix.boxlayout import MDBoxLayout
import re
import pafy
from kivy.core.audio import SoundLoader
import googleapiclient
import vlc

kivy.require('1.9.0')

class Audio_Player:
    def __init__(self):
        self.instance = vlc.Instance()
        self.player = self.instance.media_player_new()

    def play_video(self, id):
        
        # Create new pafy obj video
        video = pafy.new(id)
        
        # Extract best audio from video
        audio_stream = video.getbestaudio()

        # Retrive audio url
        audio_url = audio_stream.url
        
        # Play audio using python-vlc
        try:
            media = self.instance.media_new(audio_url)
        except:
            return

        self.player.set_media(media)

        self.player.play()
        # while self.player.is_playing():
        #     pass
    
    def stop(self):
        if self.player.is_playing():
            self.player.stop()
    
    def pause(self):
        self.player.set_pause(1)
        
    def resume(self):
        self.player.set_pause(0)

class Music(MDBoxLayout):
    # Construtor
    def __init__(self, **kwargs):
        super(Music, self).__init__(**kwargs)
        self.player = Audio_Player()

    # Retrive URL from InputField
    def retrive_url(self):
        # Retrive Value from url input
        url = self.ids.url.text
        if not url:
            return

        # Check if url is vide or playlist and retrive ID from URL
        result = check_video_or_playlist(url)
        if not result:
            return
        
        # Get necessary data and play music
        self.type = result["type"]
        self.id = result["id"]
        self.start_music()

    # Start playing music
    def start_music(self):
        # If video
        if self.type == "video":
            try:
                self.player.play_video(self.id)
                # Change status in .kv
                self.ids.status.text = "Status: Playing Video Audio"
            except:
                print("error")

        # If playlist

    # Stop playing music
    def stop_music(self):
        self.player.stop()

    def pause_and_resume(self):
        button = self.ids.puase_and_resume_icon
        
        # Pause
        if button.icon == "play-circle-outline":
            button.icon = "pause-circle-outline"
            self.player.pause()

        # Resume
        else:
            button.icon = "play-circle-outline"
            self.player.resume()

# Application
class YoutubeMusicPlayer(MDApp):

    # Function to return the UI
    def build(self):
        return Music()


# playlist pattern https://youtube.com/playlist?list=PLOxu-EtycI1lOoGBpE508PuvBsGHLOihJ
# video pattern https://youtu.be/pdZT8jd6bMk

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