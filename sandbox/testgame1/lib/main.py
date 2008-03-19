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
from pyglet import image
from pyglet import clock

def main():
    clock.set_fps_limit(20)
    #fps_display = clock.ClockDisplay()
    win = window.Window(400,300)
    ft = pygletfont.load('Arial', 36)
    message = data.load('sample.txt').read()
    textObject = Text(ft,message)
    win.push_handlers(on_key_press, on_mouse_press)
    win.push_handlers(textObject)
    archer_data = image.load(data.filepath('walk_sequence.png'))
    archer_seq = image.ImageGrid(archer_data, 8,8)
    archer_texture_grid = image.TextureGrid(archer_seq)
    archer = AnimatedSprite(archer_texture_grid)
    while not win.has_exit:
        win.dispatch_events()
        clock.tick()
        win.clear()
        textObject.draw()
        archer.draw()
        #fps_display.draw()
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

class AnimatedSprite(object):
    def __init__(self,texturegrid):
        self.texture_grid = texturegrid
        self.frame = 0
    def draw(self):
        self.texture_grid[self.frame].blit(300,200)
        self.frame +=1
        if self.frame == len(self.texture_grid):
            self.frame = 0;

def on_key_press(symbol, modifiers):
    if symbol == key.A:
        print 'The "LEFT" key was pressed.'
    elif symbol == key.ENTER:
        print 'The enter key was pressed.'

def on_mouse_press(x, y, button, modifiers):
    if button == mouse.LEFT:
        print 'The left mouse button was pressed.'    

