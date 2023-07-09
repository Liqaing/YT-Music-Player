import kivy
from kivymd.app import MDApp
from kivymd.uix.boxlayout import MDBoxLayout
import re
import pafy
from kivy.core.audio import SoundLoader
import googleapiclient.discovery
import vlc
import time

kivy.require('1.9.0')

class Audio_Player:
    def __init__(self):
        self.instance = vlc.Instance()
        self.player = self.instance.media_player_new()

    # Play video audio
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

    # Play playlist audio
    def play_playlist(self, id):
        api_key = "AIzaSyBkpY4xMyCSMgFX4opcnyS7Q03x96yzDFk"

        # Create obj to communicate with API
        youtube = googleapiclient.discovery.build(
            "youtube", "v3", developerKey=api_key
        )

        # Get snippet (data) of video from playlist
        request = youtube.playlistItems().list(
            part = "snippet",
            maxResults = 50,
            playlistId = id # id is id of playlist from the input url
        ).execute()

        # Retrive all video url from the returned data
        videos = []
        for video_data in request["items"]:
            video = {
                "video_id": video_data["snippet"]["resourceId"]["videoId"],
                "title": video_data["snippet"]["title"]
            }
            videos.append(video)

        # Play video audio inside of playlist
        media_player = vlc.MediaPlayer()
        self.media_list_player = vlc.MediaListPlayer()
        media_list = vlc.MediaList()

        for video in videos:
            # Create new pafy obj video
            video = pafy.new(video["video_id"])
            
            # Extract best audio from video
            audio_stream = video.getbestaudio()

            # Retrive audio url
            audio_url = audio_stream.url
            
            # Play audio using python-vlc
            try:
                media = self.instance.media_new(audio_url)
            except:
                return

            media_list.add_media(media)

        self.media_list_player.set_media_list(media_list)
        self.media_list_player.set_media_player(media_player)
        self.media_list_player.play_item_at_index(0)

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
        else:
            self.player.play_playlist(self.id)

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