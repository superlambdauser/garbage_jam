import os
import random
import pygame as pg
import scene_management as scene
import game_objects as go

# Display :
SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 600
SCREEN_SIZE = (SCREEN_WIDTH, SCREEN_HEIGHT)
SCREEN_CENTER = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)

#Layers :
BACKGROUND_LAYER = 0
GARBAGE_LAYER = 1
COCKPIT_LAYER = 2
BUTTONS_LAYER = 3

# Events :

# Scenes :
class GameScene(scene.Scene) :
### ↓ GAME LOGIC HERE ↓ ###
    def __init__(self):
        super().__init__()
        self.spawn_timer = 0
        self.spawn_interval = self.random_interval()

    def load(self) :
        background = ZoomingBackground(image=self.assets.get("background.png"), position=SCREEN_CENTER, layer=BACKGROUND_LAYER)
        cockpit = go.GameObject(image=self.assets.get("cockpit.png"),position=SCREEN_CENTER, layer=COCKPIT_LAYER)
        red_button = Button(image=self.assets.get("buttons/red_button.png"), position=(600, 520), layer=COCKPIT_LAYER)
        interactive_button_one = Button(image=self.assets.get("buttons/interactive_buttons1.1.png"), position=(900,520),layer=COCKPIT_LAYER)

        self.current_garbage = self.spawn_garbage()
    
    def update(self, dt):
        super().update(dt)

        # Respawning garbage logic :
        self.spawn_timer += dt
        if self.spawn_timer >= self.spawn_interval :
            self.spawn_timer = 0
            self.spawn_interval = self.random_interval()
            self.spawn_garbage()
            
            
            
            

    def random_interval(self) :
        return random.uniform(3.0, 5.0)
    
    def random_position(self) :
        x = random.randrange(100, 1000, 25)
        y = random.randrange(150, 300, 10)
        return (x, y)
    
    def spawn_garbage(self) :
        garbage_folder = self.assets._base_path + "garbage/"
        random_file = random.choice(os.listdir(garbage_folder))
        
        

        garbage = Garbage(image=self.assets.get("garbage/" + random_file), position=self.random_position(), layer=GARBAGE_LAYER, scaling_speed=0.1, max_scale=2.5)
        garbage.set_speed(garbage.rotation_speed * random.uniform(-1, 1))

class MenuScene(scene.Scene) :
    def load(self) :
        pass

# Game Objects :
class ZoomingBackground(go.ZoomingObject) :
    def __init__(self, scaling_speed = 0.03, max_scale = 3, **kwargs):
        super().__init__(scaling_speed, max_scale, **kwargs)
        self.min_scale = self.scale

    def update(self, dt):
        super().update(dt)
        if self.scale > self.max_scale :
            self.scale = self.min_scale

class Garbage(go.ZoomingRotatingObject):
    def update(self, dt):
        super().update(dt)
        if self.scale > self.max_scale:
            # Damage ship
            # ...
            # Then destroy self
            self.destroy()

class Button(go.ClickableObject) :
    def on_click(self) :
        print("clicked")
        # Button logic
        
        # ...
        pass