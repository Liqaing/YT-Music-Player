import kivy
from kivymd.app import MDApp
from kivymd.uix.boxlayout import MDBoxLayout

kivy.require('1.9.0')

class Music(MDBoxLayout):
    # Construtor
    def __init__(self, **kwargs):
        super(Music, self).__init__(**kwargs)



# Application
class YoutubeMusicPlayer(MDApp):

    # Function to return the UI
    def build(self):
        return Music()
    
if __name__ == '__main__':
    YoutubeMusicPlayer().run()