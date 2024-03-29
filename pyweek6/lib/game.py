from pyglet import event
from pyglet.window import key
from pyglet import image
from actors import *
from claw import Claw
from hud import *
from timer import Timer
from pyglet import font as pygletfont
from actor import Actor
import data
"""
at the start of the game we need (as for as actors): 
a clock,
a conveyor, 
a claw, 
3 parts bins, 
a random part generator, 
and a finished robot bin.

Clickables are:
the conveyor, 
parts bins, 
and finish shelf
"""
class Game(event.EventDispatcher):
    levelAnnouncementColor = (0,0,0.0,1.0)
    levelStatsColor = (1,0.0,0,1.0)
    gameOverColor = (1.0,0,0,1.0)
    def __init__(self):
        self.actors = []
        self.widgets = self.children = []
        self.background = image.load(data.filepath("Env09.png"))
        self.claw = Claw('claw.png')
        self.recyclebin = RecycleBin()
        self.conveyor = Conveyor(self)
        self.hud = HUD()
        self.finishbin = FinishedBin(self)
        self.add_actor(self.conveyor)
        self.add_actor(self.recyclebin)
        self.add_actor(RandomPartGenerator(self.conveyor))
        self.add_actor(PartsBin(self,'head',32,70,188,60)) 
        self.add_actor(PartsBin(self,'body',240,70,188,60))
        self.add_actor(PartsBin(self,'legs',444,70,188,60))
        self.add_actor(self.finishbin)
        self.add_actor(FinishTag())
        self.add_actor(self.claw)
        self.add_actor(self.hud)
        
        self.level = 1
        self.timer = Timer()
        self.timer.set(0,5,True)
        self.font = pygletfont.load('Arial',50)
        self.fontsmall = pygletfont.load('Arial',30)
        self.beginTime = None
        self.levelText = pygletfont.Text(self.font, "Level %i" %self.level, x = 800 / 2, y = 400, halign = pygletfont.Text.CENTER)
        self.levelText.color = self.levelAnnouncementColor
        self.state = 'levelBegin'
        
        #set things up for level 1
        self.hud.clock.timer.set(1,0,False)
        self.hud.robotsordered.set(1)
        self.finishbin.generate_new_order(1)

    def update(self,dt):
        if self.state == 'gameOver':
            self.background.blit(200,100,-0.9)
        elif self.state == 'levelPaused':
            self.levelPausedState(dt)
        else:
            self.background.blit(0,0,-0.9)
        if self.state == 'levelBegin':
            self.levelBeginState(dt)
        elif self.state == 'levelRunning':
            self.updateActors(dt)
        elif self.state == 'levelOver':
            self.levelOverState(dt)
        elif self.state == 'gameOver':
            self.gameOverState(dt)
        
    def levelPausedState(self,dt):
        self.levelText = pygletfont.Text(self.font, "Paused", x = 800 / 2, y = 350, halign = pygletfont.Text.CENTER)
        self.levelInfoText = pygletfont.Text(self.fontsmall, "Press Spacebar to Unpause.", x = 800 / 2, y = 350 - self.font.ascent, halign = pygletfont.Text.CENTER)
        self.levelInfoText.color = self.levelStatsColor
        self.levelText.color = self.levelStatsColor
        self.levelText.draw()
        self.levelInfoText.draw()
    
    def levelBeginState(self,dt):
        self.timer.update(dt)
        self.updateActors(0)
        self.beginTime = pygletfont.Text(self.fontsmall, "Begins in " + str(self.timer.getSeconds()) + " Seconds", x = 800 / 2, y = 400 - self.font.ascent, halign = pygletfont.Text.CENTER)
        self.beginTime.color = self.levelAnnouncementColor
        self.levelText.draw()
        self.beginTime.draw()
        
        if self.timer.active == False:
            self.state = 'levelRunning'
            self.dispatch_event('on_level_begin',self.level)
        
    def levelOverState(self,dt):
        self.timer.update(dt)
        self.updateActors(0)
        self.levelText.draw()
        self.levelInfoText.draw()
        if self.timer.active == False:
            if self.state == "gameOver":
                self.dispatch_event('on_game_over')
                return True
            else:
                self.level += 1
                self.levelText = pygletfont.Text(self.font, "Level %i" %self.level, x = 800 / 2, y = 400, halign = pygletfont.Text.CENTER)
                self.levelText.color = self.levelAnnouncementColor
                self.timer.set(0,5,True)
                self.state = 'levelBegin'
                #get the HUD ready for the next level
                self.hud.clock.timer.set(0,15+(self.level*45),False)
                self.hud.robotsordered.set(self.level*1.5)
                self.finishbin.generate_new_order(self.level*1.5)
                
    def gameOverState(self,dt):
        self.timer.update(dt)
        self.levelText.draw()
        self.levelInfoText.draw()
        if self.timer.active == False:
            self.dispatch_event("on_game_over")
            
    def updateActors(self,dt):
        for actor in self.actors:
            actor.update(dt)

    def add_actor(self, actor, layer = 0):
        actor.push_handlers(self)
        self.actors.append(actor)
        self.actors.sort(key=lambda actor:actor.z) #sort the actors by z value
        if isinstance(actor, ClickableActor):
            actor.push_handlers(self.claw)
        elif isinstance(actor,HUD):
            actor.initComponents()
            
    def add_actor_for_listening(self, actor):
        actor.push_handlers(self)
        if isinstance(actor,Clock):
            self.push_handlers(actor)
    
    def remove_actor(self, actor):
        self.actors.remove(actor)

    def on_pause(self):
        self.state = 'levelPaused'
        self.dispatch_event('stop_music')
    
    def on_un_pause(self):
        self.state = 'levelRunning'
        self.dispatch_event('play_music')

    def on_recycle_robot(self,robot):
        self.recyclebin.attach(robot)

    def on_robot_rejected(self,robot):
        self.recyclebin.attach(robot)
        
    def on_robot_shipped(self,robot):
        self.hud.money.deposit(5)
        self.hud.robotsordered.decrease()
        if self.hud.robotsordered.remaining == 0:
            self.hud.clock.timer.active = False
            self.hud.money.deposit(self.hud.clock.timer.getMinutes()*10)
            self.on_level_over()

    def on_parts_ordered(self):
        self.hud.money.withdraw(1)

    def on_key_press(self, symbol, modifiers):
        if self.state == 'levelRunning':
            if symbol == key.PAUSE or symbol == key.SPACE:
                self.dispatch_event('on_pause')
                return True
        if self.state == 'levelPaused':
            if symbol == key.PAUSE or symbol == key.SPACE:
                self.dispatch_event('on_un_pause')
                return True
        elif self.state == 'gameOver':
            self.dispatch_event('on_game_over')
            return True
        if symbol == key.ESCAPE:
            self.dispatch_event('on_quit')
            return True

    def on_mouse_press(self, x, y, button, modifiers):
        #find out which item was clicked
        if self.state == 'gameOver':
            self.dispatch_event('on_game_over')
            return True
        for item in self.widgets:
            if item.on_click(x,y):
                return True
                
    def on_mouse_motion(self, x, y, dx, dy):
        for item in self.widgets:
            if item.on_move(x,y,dx,dy):
                return True
                
    def on_level_over(self):
        #clear the robot parts off the conveyor belt
        self.conveyor.clearRobots()
        if self.hud.robotsordered.remaining == 0:
            self.dispatch_event('on_level_completed')
        else:
            self.dispatch_event('on_level_lost')
    
    def on_level_completed(self):
        self.state = 'levelOver'
        self.levelText = pygletfont.Text(self.font, "Level %i Completed!" %self.level, x = 800 / 2, y = 400, halign = pygletfont.Text.CENTER)
        self.levelText.color = self.levelStatsColor
        self.levelInfoText = pygletfont.Text(self.fontsmall, "Bonus: %i Mins * $10 = $%i" %(self.hud.clock.timer.getMinutes(), self.hud.clock.timer.getMinutes()*10), x = 800 / 2, y = 400 - self.font.ascent, halign = pygletfont.Text.CENTER)
        self.levelInfoText.color = self.levelStatsColor
        self.timer.set(0,5,True)
    
    def on_level_lost(self):
        self.state = 'gameOver'
        self.levelText = pygletfont.Text(self.font, "GAME OVER!", x = 800 / 2, y = 580-self.font.ascent, halign = pygletfont.Text.CENTER)
        self.levelText.color = self.gameOverColor
        self.levelInfoText = pygletfont.Text(self.fontsmall, "Out of Time!" , x = 800 / 2, y = self.levelText.y - self.font.ascent, halign = pygletfont.Text.CENTER)
        self.levelInfoText.color = self.gameOverColor
        self.background = image.load(data.filepath("RobotRubbish01.png"))
        self.timer.set(0,7,True)

Game.register_event_type('on_pause')
Game.register_event_type('on_un_pause')
Game.register_event_type('play_music')
Game.register_event_type('stop_music')
Game.register_event_type('on_quit')
Game.register_event_type('on_level_begin')
Game.register_event_type('on_level_completed')
Game.register_event_type('on_level_lost')
Game.register_event_type('on_game_over')

