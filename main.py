import kivy
from kivymd.app import MDApp
from kivymd.uix.boxlayout import MDBoxLayout
import pafy
import vlc
import googleapiclient.discovery


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
        
        if self.url[:20] != "https://youtube.com/":
            return "Invalid URL"
        
        print(self.url)

        # Retrive ID from URL
        self.id = check_video_or_playlist(self.url)

        print(self.id)

        # Validating
        if not self.id:
            return

        if self.id["type"] == "video":
            pass
        

# playlist pattern https://youtube.com/playlist?list=PLOxu-EtycI1lOoGBpE508PuvBsGHLOihJ
# video pattern https://www.youtube.com/watch?v=y6cWxCFx1i8&list=PLOxu-EtycI1lOoGBpE508PuvBsGHLOihJ&index=1

# Application
class YoutubeMusicPlayer(MDApp):

    # Function to return the UI
    def build(self):
        return Music()


# Check URL id video or playlist 
def check_video_or_playlist(url: str) -> str:
    # Check if url is a playlist url
    if url[:34] == "https://youtube.com/playlist?list=":
        info = {
            'type': 'playlist',
            'url': url[:34]
        }
        return info
    elif url[:38] == "https://www.youtube.com/playlist?list=":
        info = {
            'type': 'playlist',
            'url': url[:38]
        }
        return info

    # Or is a video url
    elif url[:32] == "https://www.youtube.com/watch?v=":
        info = {
            'type': 'video',
            'url': url[:32]
        }
        return info
    else:
        return False

if __name__ == '__main__':
    YoutubeMusicPlayer().run()