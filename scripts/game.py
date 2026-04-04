import os
import math
import random
import pygame as pg

import scores
import game_objects as go
import configs as configs
import scene_management as scenes
from event_bus import EventBus

# Display :
SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 600
SCREEN_SIZE = (SCREEN_WIDTH, SCREEN_HEIGHT)
SCREEN_CENTER = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)

#Game Layers :
BACKGROUND_LAYER = 0
GARBAGE_LAYER = 1
RETICLES_LAYER = 2
COCKPIT_LAYER = 3
BUTTONS_LAYER = 4

#Start layers:
START_BG_LAYER = 0
START_IMAGE_LAYER = 1
START_BUTTON_LAYER = 2
START_TEXT_LAYER = 3

# Reticles directions/speed :
RETICLE_SPEED = 200.0 # Pixels per millisecond
RETICLE_SNAPPING_THRESHOLD = 20.0
### PLEASE DO NOT TOUCH BOUNDS OMG IT WAS HORRIBLE TO SET THX
RETICLE_BOUNDS_X = (160,1050)
RETICLE_BOUNDS_Y = (125,370)

# Scenes :
class GameScene(scenes.Scene) :
    def load(self) :
        self.score = 0

        self.spawn_timer = 0
        self.spawn_interval = self.random_interval()
        self.first_garbage_timer = 1.0

        self.reticles_snapped = False
        self.first_garbage = True
        
        self.garbage_on_screen = []
        self.cracks = []

        #music :
        pg.mixer.init()
        pg.mixer.music.load("assets/sound/ambient_horror.wav")
        pg.mixer.music.set_volume(0.3)
        pg.mixer.music.play()

        # Events :
        self._register_events()

        # Objects :
        self.background = ZoomingBackground(
            image=self.assets.get("background.png"),
            position=SCREEN_CENTER, 
            layer=BACKGROUND_LAYER)
        
        self.cockpit = Cockpit(
            image=self.assets.get("cockpit.png"),
            position=SCREEN_CENTER,  
            layer=COCKPIT_LAYER)
        
        self.score_display = TextObject(
            position=(960, 425),
            layer=COCKPIT_LAYER,
            font_size=50,
            color=(13, 69, 30),
            text="0")
        
        self.hp_display = TextObject(
            position=(1000, 425),
            layer=COCKPIT_LAYER,
            font_size=50,
            color=(150,0,75),
            text=f"{self.cockpit.cockpit_actual_pv}")

        self.portrait = HangingPortrait(
            image=self.assets.get("family_portrait_hanging.png"),
            position=(1000, 80),
            layer=COCKPIT_LAYER )

        self.post_its_left = [
            go.GameObject(
                image=self.assets.get(cfg["image"]),
                position=cfg["position"],
                layer=COCKPIT_LAYER
            )
            for cfg in configs.POST_IT_LEFT_CONFIGS
        ]

        self.post_its_right = [
            go.GameObject(
                image=self.assets.get(cfg["image"]),
                position=cfg["position"],
                layer=COCKPIT_LAYER
            )
            for cfg in configs.POST_IT_RIGHT_CONFIGS
        ]

        # Reticles :
        self.reticle_x = Reticles(image=self.assets.get("reticles/reticule_x.png"),position=(250,250),layer=RETICLES_LAYER)
        self.reticle_y = Reticles(image=self.assets.get("reticles/reticule_y.png"),position=(950,250),layer=RETICLES_LAYER)

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

    def _register_events(self):
        # Here goes events like so :
        # EventBus.on(event_name:str, callback:custom_method)
        EventBus.on("garbage_escaped", self.on_garbage_collision)
        EventBus.on("garbage_destroyed", self.on_garbage_destroyed)
        EventBus.on("reticles_snap", self.on_reticles_snapped)
        EventBus.on("game_over", self.on_game_over)
    
    def _unregister_event(self, event, callback):
        print("unregistering events")
        EventBus.off_all(self)

    def update(self, dt):
        super().update(dt)
        
        # Snapping reticles :
        if self.reticle_x.is_near(target=self.reticle_y, threshold=RETICLE_SNAPPING_THRESHOLD) and not self.reticles_snapped :
            self.reticles_snapped = True
            EventBus.emit("reticles_snap")

            self.red_button.set_active()
        
        #if garbage destroy : reset_buttons (later), reset reticles pos + unlink them
        if self.reticles_snapped :
            for garbage in self.garbage_on_screen :
                if pg.sprite.collide_mask(garbage, self.viewfinder) and self.red_button.is_clicked : 
                    EventBus.emit("garbage_destroyed", garbage=garbage)
                    garbage.destroy()
                    
        # Respawning garbage logic :
        self.spawn_timer += dt
        if self.spawn_timer >= self.spawn_interval and not self.first_garbage:
            self.spawn_timer = 0
            self.spawn_interval = self.random_interval()
            self.spawn_garbage()    

            #make first garbage spawn after x amount of time
        if self.first_garbage :
            # print("waiting")
            self.first_garbage_timer -= dt
            if self.first_garbage_timer <= 0:
                self.first_garbage = False
    
    def on_game_over(self) :
        scores.update_best(score=self.score)
        scenes.SceneManager().switch(GameOverScene(score=self.score))

    # Garbage
    def random_interval(self) :
        return random.uniform(5.0, 7.0)
    
    def random_position(self) :
        x = random.randrange(100, 1000, 25)
        y = random.randrange(150, 300, 10)
        return (x, y)
    
    def spawn_garbage(self) :
        # Access images :
        garbage_folder = self.assets._base_path + "garbage/"
        random_file = random.choice(os.listdir(garbage_folder))
        
        # Actually spawn garbage :
        garbage = Garbage(image=self.assets.get("garbage/" + random_file), position=self.random_position(), layer=GARBAGE_LAYER, scaling_speed=0.1, max_scale=2.5)
        garbage.set_speed(garbage.rotation_speed * random.uniform(-1, 1))

        # Store garbage spawned in a list :
        self.garbage_on_screen.append(garbage)

    def spawn_cracks(self, position):
        cracks_folder = self.assets._base_path + "cracks/"
        random_file_crack = random.choice(os.listdir(cracks_folder))

        crack = go.GameObject(image=self.assets.get("cracks/" + random_file_crack), position=position, layer=RETICLES_LAYER)
        self.cracks.append(crack)

    def on_garbage_collision(self, damage, position) :
        print("OUCH")
        self.cockpit.take_damage(damage)
        self.spawn_cracks(position)

    def on_garbage_destroyed(self, garbage) :
        self.score += 1
        self.score_display.set_text(str(self.score))
        self.garbage_on_screen.remove(garbage)

    # Reticles
    def on_reticles_near(self):
        self.reticle_x.snap_to(self.reticle_y)

    def on_reticles_snapped(self) :
        print(f"snapped called, reticles_snapped: {self.reticles_snapped}")
        self.viewfinder = Reticles(
                image=self.assets.get("reticles/viewfinder.png"),
                position = self.reticle_x.current_pos,
                layer=RETICLES_LAYER)

        for button in self.buttons :
            if button.is_active :
                button.set_reticle(self.viewfinder)

        self.reticle_x.destroy()
        self.reticle_y.destroy()

        self.red_button.set_active()

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


class StartScene(scenes.Scene):
    def load(self):
        self.button_timer = 3
        
        self.start_background = ZoomingBackground(
            image=self.assets.get("background1.png"),
            position=SCREEN_CENTER,
            layer=START_BG_LAYER)
        
        self.post_it = go.GameObject(
            image=self.assets.get("post_its/post_it_remember.png"),
            position=(820,480),
            layer=START_IMAGE_LAYER)
        
        self.family_portait = go.GameObject(
            image=self.assets.get("family_drawing.png"),
            position=SCREEN_CENTER,
            layer=START_IMAGE_LAYER)
        
        self.start_button = RedButton(images=[self.assets.get(img) for img in configs.START_BTN_CONFIG["images"]],
                                   position=configs.START_BTN_CONFIG["position"],
                                   layer=START_BUTTON_LAYER)
        self.start_button.is_active = False

        self.start_text = TextObject(
            position=(SCREEN_WIDTH/2,50),
            layer=START_TEXT_LAYER,
            font_size=32,
            color= (150,0,75),
            text="You remember, right? What all of this is for ?\n"
            "       What you have done ?"
        )
    
    def update(self, dt):
        super().update(dt)
        self.button_timer -= dt
        if self.button_timer <=0:
            self.start_button.is_active = True
        
        if self.start_button.is_active and self.start_button.is_clicked:
            scenes.SceneManager().switch(GameScene())

class GameOverScene(scenes.Scene) :
    def __init__(self, score):
        self.final_score = score
        self.best_score = scores.best_score

        super().__init__()
    def load(self):
        self.end_background = ZoomingBackground(
            image=self.assets.get("background1.png"),
            position=SCREEN_CENTER,
            layer=START_BG_LAYER)
        
        self.game_over_txt = TextObject(
            position=(600,250),
            layer=START_IMAGE_LAYER,
            font_size= 100,
            text="GAME OVER"
        )

        self.score_display = TextObject(
            position=(600, 350),
            layer=START_IMAGE_LAYER,
            font_size=50,
            text=f"You collected {self.final_score} garbage. BEST : {self.best_score}"
        )

        self.restart_button = RestartButton(
            images=[self.assets.get(img) for img in configs.RESTART_BTN_CONFIG["images"]],
            position=configs.RESTART_BTN_CONFIG["position"],
            layer=START_BUTTON_LAYER
        )

        self._register_events() 

    def _register_events(self):
        EventBus.on("restart_clicked", self.on_restart_clicked)

    def on_restart_clicked(self) :
        scenes.SceneManager().switch(StartScene())
    
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
    def __init__(self, scaling_speed = 0.03, max_scale = 3, **kwargs):
        super().__init__(scaling_speed, max_scale, **kwargs)
        self.damage = 1
        self.last_pos = None

    def update(self, dt):
        super().update(dt)
        if self.scale > self.max_scale:
            self.escape()

    def escape(self) :
        if not self.alive():
            return
        EventBus.emit("garbage_escaped", damage=self.damage, position=self.position)
        super().destroy()
    
    def destroy(self):
        super().destroy()

class Cockpit(go.GameObject):
    def __init__(self, image, position, layer):
        super().__init__(image, position, layer)
        self.cockpit_max_pv = 10
        self.cockpit_actual_pv = self.cockpit_max_pv

    def take_damage(self,damage):
        self.cockpit_actual_pv -= damage
        print(f"Remaining PV : {self.cockpit_actual_pv}")

    def update(self, dt):
        super().update(dt)
        if self.cockpit_actual_pv <= 0:
            #launch game over
            print("game over")
            EventBus.emit("game_over")

class Button(go.AnimatedObject, go.ClickableObject, go.OutlineHoverEffectObjects):
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

    def update(self, dt):
        super().update(dt)
        if self.is_clicked:
            self.image = self.images[-1] # Image stays on click
        else:
            self.image = self.images[0] # Resets to idle on release

class RestartButton(Button) :
    def on_click(self):
        super().on_click()
        EventBus.emit("restart_clicked")

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
        if self.reticle :
            self.update_reticle()

class RedButton(Button) :
    # Garbage destruction button
    def __init__(self, images, position, layer, frame_duration = 0.1):
        super().__init__(images, position, layer, frame_duration)
        self.is_active = False
        self.idle = images[0]
        self.images = [images[i] for i in range(1, len(images))] # Remove idle

        self.color = (179, 227, 28)

    def update(self, dt):
        if self.is_active :
            super().update(dt)

    def destroy_garbage(self, garbage):
        if self.is_active and garbage:
            garbage.destroy()

    def is_hovered(self):
        if self.is_active :
            return super().is_hovered()
        else : return False

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
        self.set_position(target.rect.center)
        self.is_snapped = True
    
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

class TextObject(go.GameObject) :
    def __init__(self, position, layer, font_size=32, color=(255, 255, 255), text=""):
        self.text = text
        self.font = pg.font.Font(None, font_size)
        self.color = color
        self.anchor = position
        image = self._render(self.text)

        super().__init__(image, position, layer)

    def _render(self, text:str) :
        return self.font.render(text, True, self.color)
    
    def set_text(self, text:str) :
        self.image = self._render(text)
        self.rect = self.image.get_rect(center=self.anchor)

class ScoreDisplay(TextObject) :
    def set_text(self, text):
        super().set_text(self.set_text + text)
    
    def set_text(self, text:str) :
        self.image = self._render(text)
        self.rect = self.image.get_rect(midright=self.anchor)
