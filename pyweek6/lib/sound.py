from pyglet import media
import data

class SoundManager:
    defaultMusic = data.filepath("robot maker.mp3")
    
    def __init__(self):
        self.lastMusic = self.defaultMusic
        self.playingMusic = False
        
        self.smMusic = media.Player()
        self.smSFX = media.Player()
    
    # Streaming BG Music
    def playMusic(self, filename = defaultMusic):
        self.stopMusic()
        self.playingMusic = True
        self.lastMusic = filename
        musicCD = media.load(filename)
        self.smMusic.queue(musicCD)
        self.smMusic.play()
    
    def stopMusic(self):
        self.playingMusic = False
        self.smMusic.pause()
        self.smMusic.next()
    
    # Buffering for BG Music and SFX
    def buffer(self):
        if self.playingMusic:
            if self.smMusic.source:
                self.smMusic.dispatch_events()
            else:
                self.playMusic(self.lastMusic)
    
