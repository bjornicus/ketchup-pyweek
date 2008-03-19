'''Game main module.

Contains the entry point used by the run_game.py script.

Feel free to put all your game code here, or in other modules in this "lib"
directory.
'''
import data
from pyglet import window
from pyglet.window import key
from pyglet.window import mouse
from pyglet import font as pygletfont
from pyglet import window

def main():
    win = window.Window()
    ft = pygletfont.load('Arial', 36)
    message = data.load('sample.txt').read()
    textObject = Text(ft,message)
    win.push_handlers(on_key_press, on_mouse_press)
    win.push_handlers(textObject)
    while not win.has_exit:
        win.dispatch_events()
        win.clear()
        textObject.draw()
        win.flip()
        
class Text(object):
    def __init__(self, font, message):
        self.text = pygletfont.Text(font, message)
    def on_key_press(self, symbol, modifiers):
        if symbol == key.LEFT:
            self.text.x -=10
        elif symbol == key.RIGHT:
            self.text.x +=10
        elif symbol == key.UP:
            self.text.y +=10
        elif symbol == key.DOWN:
            self.text.y -=10
    def draw(self):
        self.text.draw()


def on_key_press(symbol, modifiers):
    if symbol == key.A:
        print 'The "LEFT" key was pressed.'
    elif symbol == key.ENTER:
        print 'The enter key was pressed.'

def on_mouse_press(x, y, button, modifiers):
    if button == mouse.LEFT:
        print 'The left mouse button was pressed.'    

