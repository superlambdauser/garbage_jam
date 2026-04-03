import os
import math
import random
import pygame as pg
import scene_management as scene
import game_objects as go
import configs as configs

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
RETICLE_SPEED = 200.0 # Pixels per millisecond
RETICLE_SNAPPING_THRESHOLD = 20.0
### PLEASE DO NOT TOUCH BOUNDS OMG IT WAS HORRIBLE TO SET THX
RETICLE_BOUNDS_X = (150,1050)
RETICLE_BOUNDS_Y = (125,375)
###TEST :
ret_path = "reticles/"
# Assets :
# constants / asset keys
BTN_ONE_IMAGES = ["buttons/interactive_buttons1.1.png", "buttons/interactive_buttons1.2.png"]
BTN_TWO_IMAGES = ["buttons/interactive_buttons2.1.png", "buttons/interactive_buttons2.2.png"]
BTN_THREE_IMAGES = ["buttons/interactive_buttons3.1.png", "buttons/interactive_buttons3.2.png"]
BTN_FOUR_IMAGES = ["buttons/interactive_buttons4.1.png", "buttons/interactive_buttons4.2.png"]
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
        background = ZoomingBackground(image=self.assets.get("background.png"), 
                                       position=SCREEN_CENTER, 
                                       layer=BACKGROUND_LAYER)
        cockpit = go.GameObject(image=self.assets.get("cockpit.png"),
                                position=SCREEN_CENTER, 
                                layer=COCKPIT_LAYER)
        portrait = HangingPortrait(image=self.assets.get("family_portrait_hanging.png"),
                                  position=(1000, 80),
                                  layer=COCKPIT_LAYER )


        # Reticles :
        self.reticle_x = Reticles(image=self.assets.get(ret_path + "reticule_x.png"),position=(250,250),layer=RETICLES_LAYER)
        self.reticle_y = Reticles(image=self.assets.get(ret_path + "reticule_y.png"),position=(950,250),layer=RETICLES_LAYER)

        self.reticles = {
        "reticle_x": self.reticle_x,
        "reticle_y": self.reticle_y,
        }
        
        # Buttons :
        self.buttons = [
        ReticlesButton(images=[self.assets.get(img) for img in cfg["images"]],
            position=cfg["position"],
            layer=BUTTONS_LAYER
            ) 
            for cfg in configs.BUTTON_CONFIGS
        ]
        self.red_button = RedButton(images=[self.assets.get(img) for img in configs.RED_BUTTON_CONFIG["images"]],
                                    position=configs.RED_BUTTON_CONFIG["position"],
                                    layer=BUTTONS_LAYER)
        
        
        self.set_random_buttons_active()

        ### !! RED BUTTON = SPECIAL GARBAGE LOGIC  --damn ok, no need to scream--
        # red_button = RedButton(image=self.assets.get("buttons/red_button.png"), position=(600, 520), layer=COCKPIT_LAYER) 

        self.current_garbage = self.spawn_garbage()
    
    def update(self, dt):
        super().update(dt)

        # Snapping reticles :
        if self.reticle_x.is_near(target=self.reticle_y, threshold=RETICLE_SNAPPING_THRESHOLD) and not self.reticle_x.linked :
            self.reticle_x.snap_to(self.reticle_y)


        # Respawning garbage logic :
        self.spawn_timer += dt
        if self.spawn_timer >= self.spawn_interval :
            self.spawn_timer = 0
            self.spawn_interval = self.random_interval()
            self.spawn_garbage()    

        #if garbage destroy : reset_buttons (later), reset reticles pos + unlink them

    # Garbage 
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

    # Buttons 
    def set_all_buttons_to_decoys(self) :
        for button in self.buttons :
            button.set_to_decoy()

    def set_random_buttons_active(self) :
        for reticle in self.reticles.values() :
            for dir in configs.DIRECTIONS :
                button = random.choice(self.buttons)
                while button.is_active :
                    button = random.choice(self.buttons)
                button.set_controls(reticle=reticle, direction=dir)
    
    def reset_buttons(self) :
        self.set_all_buttons_to_decoys()
        self.set_random_buttons_active()

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
    def __init__(self, images, position, layer, frame_duration = 0.1):
        super().__init__(images, position, layer, frame_duration)
        self.is_active = False

    def set_active(self):
        self.is_active = True

    def set_inactive(self):
        self.is_active = False

    def on_click(self) :
        # print(f"images: {len(self.images)}, animating: {self.is_animating}")
        self.is_animating = True
        self.frame = 0
        

class ReticlesButton(Button) :
    def __init__(self, images, position, layer, frame_duration:float=0.1):
        super().__init__(images, position, layer, frame_duration)
        self.reticle = None
        self.direction = None
        

    def update_reticle(self):
        if self.is_clicked:
            self.reticle.must_move = True
            self.reticle.direction = self.direction

    def set_to_decoy(self) :
        self.reticle = None
        self.set_inactive()
        self.direction = None

    def set_controls(self, reticle, direction) :
        self.set_active()
        self.set_reticle(reticle)
        self.set_direction(direction)
    
    def set_reticle(self, reticle) :
        self.reticle = reticle
    
    def set_direction(self, direction:tuple) :
        self.direction = direction

    def update(self, dt):
        super().update(dt)
        if self.is_clicked:
            self.image = self.images[-1] # Image stays on click
        else:
            self.image = self.images[0] # Resets to idle on release

        if self.reticle :
            self.update_reticle()

class RedButton(Button) :
    # Garbage destruction button
    def __init__(self, images, position, layer, frame_duration = 0.1):
        super().__init__(images, position, layer, frame_duration)
        self.is_active = False
    
    def update(self, dt):
        super().update(dt)
        

    def destroy_garbage(self):
        if self.is_active:
            self.destroy(Garbage)

        
    pass

class Reticles(go.SnappingObject):
    def __init__(self, image, position, layer):
        super().__init__(image, position, layer)
        self.must_move = False
        self.direction = [1, 1]
        self.current_pos = list(self.position)

        self.bounds_x = RETICLE_BOUNDS_X
        self.bounds_y = RETICLE_BOUNDS_Y

        self.linked = None
        self.is_snapped = False
    
    def move_on_click(self, dt, direction):
        new_x = self.current_pos[0] + direction[0] * dt * RETICLE_SPEED
        new_y = self.current_pos[1] + direction[1] * dt * RETICLE_SPEED
        
        half_w = self.rect.width // 2
        half_h = self.rect.height // 2

        # Check if in bounds :
        if self.bounds_x[0] <= new_x - half_w and new_x + half_w <= self.bounds_x[1]:
            self.current_pos[0] = new_x
        if self.bounds_y[0] <= new_y - half_h and new_y + half_h <= self.bounds_y[1]:
            self.current_pos[1] = new_y
    
        self.rect.center = self.current_pos

        if self.linked:
            self.linked.current_pos = self.current_pos.copy()
            self.linked.rect.center = self.linked.current_pos

    def update(self, dt):
        if self.must_move :
            self.move_on_click(dt, self.direction)
        self.must_move = False

    def set_position(self, position):
        self.current_pos = list(position)
        self.rect.center = self.current_pos
    
    def reset_position(self):
        self.set_position(self.position)

    def snap_to(self, target):
        # Linking both so controls are shared between reticles :
        self.linked = target
        target.linked = self
        self.set_position(target.rect.center)
        self.is_snapped = True

    def unlink(self) :
        if self.linked :
            self.linked.linked = None
            self.linked = None
            self.is_snapped = False
    

class HangingPortrait(go.RotatingObject) :
    def __init__(self, amplitude:float=5, rotation_speed=2, **kwargs):
        super().__init__(rotation_speed, **kwargs)
        self.amplitude = amplitude # degrees
        self.wiggle_speed = rotation_speed #radians per second
        self.timer = 0.0
        self.pin = self.original.get_rect(topleft=self.rect.topleft).midtop

    def update(self, dt):
        self.timer += dt
        self.angle = self.amplitude * math.sin(self.timer * self.wiggle_speed)
        
        # Rotate the image
        self.image = pg.transform.rotate(self.original, self.angle)
        
        # Calculate offset caused by rotation
        offset = pg.math.Vector2(0, self.original.get_height() / 2)  # distance from pin to center
        offset.rotate_ip(-self.angle)  # rotate the offset by the same angle
        
        # Place rect so the pin stays fixed
        self.rect = self.image.get_rect(center=self.pin + offset)