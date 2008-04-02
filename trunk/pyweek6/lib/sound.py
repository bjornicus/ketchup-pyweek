from pyglet import media
import data

class SoundManager:
    defaultMusic = "robot maker.mp3"
    
    def __init__(self):
        self.smMusic = media.Player()
        self.smSFX = media.Player()
        
        self.lastMusic = self.defaultMusic
        self.playingMusic = False
        
        self.lastSFX = self.defaultMusic
        self.dictSFX = {}
    
    # Streaming Music
    def playMusic(self, filename = defaultMusic):
        self.stopMusic()
        self.playingMusic = True
        self.lastMusic = filename
        musicCD = media.load(data.filepath(filename))
        self.smMusic.queue(musicCD)
        self.smMusic.play()
    
    def stopMusic(self):
        self.playingMusic = False
        self.smMusic.pause()
        self.smMusic.next()
    
    # Cached SFX
    def loadSFX(self, filename):
        if not self.dictSFX.has_key(filename):
            self.dictSFX[filename] = media.load(data.filepath(filename))
        return self.dictSFX[filename]
    
    def playSFX(self, filename):
        self.stopSFX()
        self.lastSFX = filename
        soundClip = self.loadSFX(self.lastSFX)
        self.smSFX.queue(soundClip)
        self.smSFX.play()
    
    def stopSFX(self):
        self.smSFX.pause()
        self.smSFX.next()
    
    # Buffering for Music and SFX
    def buffer(self):
        if self.playingMusic:
            if self.smMusic.source:
                self.smMusic.dispatch_events()
            else:
                self.playMusic(self.lastMusic)
        if self.smSFX.source:
            self.smSFX.dispatch_events()
