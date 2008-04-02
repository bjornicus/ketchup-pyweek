from pyglet import media
import data

class SoundManager:
    # Data Attributes
    defaultMusic = data.filepath("robot maker.mp3")
    lastMusic = defaultMusic
    playingMusic = False
    
    def __init__(self):
        self.smMusic = media.Player()
        self.smSFX = media.Player()
    
    # Streaming BG Music
    def playMusic(self, filename):
        self.playingMusic = True
        self.lastMusic = filename
        musicCD = media.load(filename)
        self.smMusic.queue(musicCD)
        self.smMusic.play()
    
    def bufferMusic(self):
        if self.playingMusic:
            if self.smMusic.source:
                self.smMusic.dispatch_events()
            else:
                self.playMusic(self.lastMusic)
    
    def stopMusic(self):
        self.playingMusic = False
        self.smMusic.pause()
        self.smMusic.next()