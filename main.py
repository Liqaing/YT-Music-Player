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
        
        # Retrive ID from URL
        self.id = check_video_or_playlist(self.url)

        # Validating
        if not self.id:
            return

        if self.id["type"] == "video":
            api_key = "AIzaSyBkpY4xMyCSMgFX4opcnyS7Q03x96yzDFk"
            # youtube = build("youtube", "v3", developerKey=api_key)

            api_service_name = "youtube"
            api_version = "v3"

            youtube = googleapiclient.discovery.build(
                api_service_name, api_version, developerKey = api_key)

            playlist_id = "PLSR9lWowvoE3A9i4JVVHtQFjlJt0_LItG"
            request = youtube.playlistItems().list(
                part="snippet",
                maxResults=50,
                playlistId="PLSR9lWowvoE3A9i4JVVHtQFjlJt0_LItG"
            )

            playlist_item = request.execute()

            # print(playlist_item)

            video_link = []
            for item in playlist_item["items"]:
                video = {
                    "video_id": item["snippet"]["resourceId"]["videoId"],
                    "title": item["snippet"]["title"]
                }
                video_link.append(video)
                

            is_opening = False
            is_playing = False

            video_url = "https://www.youtube.com/watch?v=l2l-8jKsh8k&list=RDl2l-8jKsh8k&start_radio=1"
            is_opening = False
            is_playing = False


            # Create new pafy object
            video = pafy.new(video_url)

            # extract best audio stream from youtube
            audio_stream = video.getbestaudio()

            # retrive audio stream url
            audio_url = audio_stream.url

            player = vlc.MediaPlayer()
            media = vlc.Media(audio_url)
            player.set_media(media)
            player.play()



            good_states = [
                "State.Playing", 
                "State.NothingSpecial", 
                "State.Opening"
            ]

            while str(player.get_state()) in good_states:
                if str(player.get_state()) == "State.Opening" and is_opening is False:
                    print("Status: Loading")
                    is_opening = True

                if str(player.get_state()) == "State.Playing" and is_playing is False:
                    print("Status: Playing")
                    is_playing = True

            print("Status: Finish")
            player.stop()

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