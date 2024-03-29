'''Game main module.

Contains the entry point used by the run_game.py script.

Feel free to put all your game code here, or in other modules in this "lib"
directory.
'''
from intro import Intro
from menu import Menu
from game import Game
from credits import Credits
from sound import SoundManager
from story import Story
from pyglet import window
from pyglet import clock
from pyglet import event
from pyglet import image
from pyglet.gl import *
import data

import pyglet
#uncomment the next line for ship release:
pyglet.options['debug_gl'] = False

win = window.Window(width=800, height=600, resizable=False, caption="Ketchup's Bot Builder 2000")
img = image.load(data.filepath('mouse.png'))
cursor = window.ImageMouseCursor(img, 0, 32)
win.set_mouse_cursor(cursor)
glEnable(GL_BLEND)
glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
soundManager = SoundManager()

# this for debugging,
# uncomment if you want to see all events output ot the terminal
#from pyglet.window.event import WindowEventLogger
#win.push_handlers(WindowEventLogger())
clock.set_fps_limit(30)
fps_display = clock.ClockDisplay()

def main():
    stateManager = StateManager()
    while not win.has_exit:
        win.dispatch_events()
        win.clear()
        dt = clock.tick()
        stateManager.update(dt)
        #fps_display.draw()
        win.flip()
        soundManager.buffer()


class StateManager(object):
    def __init__(self):
        self.intro = Intro()
        self.intro.push_handlers(self)
        
        self.menu = Menu(800,600)
        self.menu.push_handlers(self)
        
        self.game = None
        
        self.credits = Credits()
        self.credits.push_handlers(self)
        
        self.story = Story()
        self.story.push_handlers(self)
        
        #change this back to intro before we ship!
        self.currentState = self.intro
        win.push_handlers(self.intro)
    
    def update(self, dt):
        self.currentState.update(dt)
        
    def show_menu(self):
        win.pop_handlers()
        self.currentState = self.menu
        win.push_handlers(self.menu)
        
    def on_intro_finish(self):
        self.show_menu()

    def on_resume_game(self):
        win.pop_handlers()
        self.currentState = self.game
        win.push_handlers(self.game)
        self.play_music()
    
    def on_new_game(self):
        win.pop_handlers()
        self.game = Game()
        self.game.push_handlers(self)
        self.currentState = self.game
        win.push_handlers(self.game)
        self.menu.enable_resume()
        self.play_music()
        
    def on_new_story_game(self):
        win.pop_handlers()
        self.currentState = self.story
        win.push_handlers(self.story)
        
    def on_game_over(self):
        self.menu.disable_resume()
        self.on_quit()

    def on_quit(self):
        self.show_menu()
        self.stop_music()
        
    def on_credits(self):
        win.pop_handlers()
        self.credits.reset()
        self.currentState = self.credits
        win.push_handlers(self.credits)
        
    def play_music(self, filename = soundManager.defaultMusic):
        soundManager.playMusic(filename)
        
    def stop_music(self):
        soundManager.stopMusic()
        
    def on_play_sfx(self, filename):
        soundManager.playSFX(filename)
        
    def on_stop_sfx(self):
        soundManager.stopSFX()
        
    def on_exit_program(self):
        win.has_exit = True
