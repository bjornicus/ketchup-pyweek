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
from pyglet import window
from pyglet import clock
from pyglet import event
from pyglet.gl import *

win = window.Window(width=800, height=600, resizable=False)
glEnable(GL_BLEND)
glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
soundManager = SoundManager()

# this for debugging,
# uncomment if you want to see all events output ot the terminal
#from pyglet.window.event import WindowEventLogger
#win.push_handlers(WindowEventLogger())


def main():
    stateManager = StateManager()
    soundManager.playMusic()
    while not win.has_exit:
        win.dispatch_events()
        win.clear()
        dt = clock.tick()
        stateManager.update(dt)
        win.flip()
        soundManager.buffer()


class StateManager(object):
    def __init__(self):
        self.intro = Intro()
        self.intro.push_handlers(self)
        
        self.menu = Menu(800,600)
        self.menu.push_handlers(self)
        
        self.game = Game()
        self.game.push_handlers(self)
        
        self.credits = Credits()
        self.credits.push_handlers(self)
        
        #change this back to intro before we ship!
        self.currentState = self.game
        win.push_handlers(self.game)
    
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
    
    def on_new_game(self):
        win.pop_handlers()
        self.game = Game()
        self.game.push_handlers(self)
        self.currentState = self.game
        win.push_handlers(self.game)

    def on_quit(self):
        self.show_menu()
        
    def on_credits(self):
        win.pop_handlers()
        self.currentState = self.credits
        win.push_handlers(self.credits)
        
    def on_play_music(self):
        soundManager.playMusic()
        
    def on_exit_program(self):
        win.has_exit = True
