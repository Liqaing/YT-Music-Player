import kivy
from kivymd.app import MDApp
from kivymd.uix.boxlayout import MDBoxLayout
import re

kivy.require('1.9.0')

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
        
        print(self.url)

        # Retrive ID from URL
        check_video_or_playlist(self.url)

        # print(self.id)

        # Validating
        # if not self.id:
        #     return

        # if self.id["type"] == "video":
        #     pass
        

# Application
class YoutubeMusicPlayer(MDApp):

    # Function to return the UI
    def build(self):
        return Music()


# playlist pattern https://youtube.com/playlist?list=PLOxu-EtycI1lOoGBpE508PuvBsGHLOihJ
# video pattern https://youtu.be/_n_swXU3XEs

# Check URL id video or playlist 
def check_video_or_playlist(url: str):
    # Check if url is a playlist url
    video_url_pattern = r"(^https://youtu.be/)([a-zA-Z0-9_-]{11})"
    playlist_url_pattern = r"(^https://youtube.com/playlist?list=)([a-zA-Z0-9_-]{})"
    
    match = re.match(video_url_pattern, url)
    if match:
        print("True")
        print(video_url_pattern)
    
    else:
        print("Not match")
    return
if __name__ == '__main__':
    YoutubeMusicPlayer().run()