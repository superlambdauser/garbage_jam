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
RETICLES_LAYER = 2
COCKPIT_LAYER = 3
BUTTONS_LAYER = 4

# Reticles directions/speed :
RETICLE_SPEED = 50.0 # Pixels per millisecond

LEFT = (-1, 0)
RIGHT = (1, 0)
UP = (0, -1)
DOWN = (0, 1)

# Events :

# Scenes :
class GameScene(scene.Scene) :
### ↓ GAME LOGIC HERE ↓ ###
    def __init__(self):
        super().__init__()
        self.spawn_timer = 0
        self.spawn_interval = self.random_interval()

        self.buttons = []
        self.reticles = []

    def load(self) :
        background = ZoomingBackground(image=self.assets.get("background.png"), position=SCREEN_CENTER, layer=BACKGROUND_LAYER)
        cockpit = go.GameObject(image=self.assets.get("cockpit.png"),position=SCREEN_CENTER, layer=COCKPIT_LAYER)
        reticle_x = Reticles(image=self.assets.get("reticule1.png"),position=(250,250),layer=RETICLES_LAYER)
        reticle_y = Reticles(image=self.assets.get("reticule2.png"),position=(950,250),layer=RETICLES_LAYER)

        # RETICLE X MOVEMENT :
        clickable_one = Button(images=[self.assets.get("buttons/interactive_buttons1.1.png"),self.assets.get("buttons/interactive_buttons1.2.png")], position=(850,520),layer=BUTTONS_LAYER, reticle=reticle_x, direction=UP) # -> This button moves the reticle_x up
        clickable_two = Button(images=[self.assets.get("buttons/interactive_buttons2.1.png")], position=(700,550),layer=BUTTONS_LAYER, reticle=reticle_x, direction=DOWN)
        clickable_three = Button(images=[self.assets.get("buttons/interactive_buttons3.1.png")], position=(500,550),layer=BUTTONS_LAYER, reticle=reticle_x, direction=LEFT)
        clickable_four = Button(images=[self.assets.get("buttons/interactive_buttons4.1.png")], position=(230,430),layer=BUTTONS_LAYER, reticle=reticle_x, direction=RIGHT)

        ### !! RED BUTTON = SPECIAL GARBAGE LOGIC
        # red_button = Button(image=self.assets.get("buttons/red_button.png"), position=(600, 520), layer=COCKPIT_LAYER) 

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

class Button(go.AnimatedObject, go.ClickableObject):
    def __init__(self, images, position, layer, reticle=None, direction:tuple=None):
        super().__init__(images, position, layer)
        self.reticle = reticle
        self.direction = direction

    def update_reticle(self):
        if self.is_clicked:
            self.reticle.must_move = True
            self.reticle.direction = self.direction

    def update(self, dt):
        if self.reticle :
            self.update_reticle()

    def on_click(self) :
        print("clicked")
        # Button animation logic
        # ...
        pass


class Reticles(go.GameObject):
    def __init__(self, image, position, layer):
        super().__init__(image, position, layer)
        self.must_move = False
        self.direction = [1, 1]
        self.current_pos = list(self.position)
    
    def move_on_click(self, dt, direction):
        self.current_pos[0] += direction[0] * dt * RETICLE_SPEED
        self.current_pos[1] += direction[1] * dt * RETICLE_SPEED
        self.rect.center = self.current_pos

    def update(self, dt):
        if self.must_move :
            self.move_on_click(dt, self.direction)
        self.must_move = False


    def set_position(self, position):
        self.current_pos = list(position)
        self.rect.center = self.current_pos
    
    def reset_position(self):
        self.set_position(self.position)
