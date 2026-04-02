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
        # red_button = Button(image=self.assets.get("buttons/red_button.png"), position=(600, 520), layer=COCKPIT_LAYER)
        self.clickable_one = Button(images=[self.assets.get("buttons/interactive_buttons1.1.png"),self.assets.get("buttons/interactive_buttons1.2.png")], position=(850,520),layer=COCKPIT_LAYER)
        
        # clickable_two = Button(image=self.assets.get("buttons/interactive_buttons2.1.png"), position=(700,550),layer=COCKPIT_LAYER)
        # clickable_three = Button(image=self.assets.get("buttons/interactive_buttons3.1.png"), position=(500,550),layer=COCKPIT_LAYER)
        # clickable_four = Button(image=self.assets.get("buttons/interactive_buttons4.1.png"), position=(230,430),layer=COCKPIT_LAYER)
        self.reticle_x = Reticles(image=self.assets.get("reticule1.png"),position=(250,250),layer=COCKPIT_LAYER)
        self.reticle_y = Reticles(image=self.assets.get("reticule2.png"),position=(950,250),layer=COCKPIT_LAYER)
        self.current_garbage = self.spawn_garbage()
    
    def update(self, dt):
        super().update(dt)

        # Respawning garbage logic :
        self.spawn_timer += dt
        if self.spawn_timer >= self.spawn_interval :
            self.spawn_timer = 0
            self.spawn_interval = self.random_interval()
            self.spawn_garbage()
        
        if self.clickable_one.is_clicked:
            self.reticle_x.move_on_click([0,1])
            
            
            

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

class Button(go.AnimatedObject, go.ClickableObject):
    def __init__(self, images, position, layer):
        super().__init__(images, position, layer)

        self.is_clicked = False
    
    def on_click(self) :
        print("clicked")
        self.is_clicked = True
        # Button logic
        # move reticle randomly 
        # ...
        pass


class Reticles(go.GameObject):
    def __init__(self, image, position, layer):
        self.position = position
        super().__init__(image, position, layer)

    
    def move_on_click(self,direction:tuple):
        self.position[0] += direction[0]
        self.position[1] += direction[1]