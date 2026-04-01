import pygame as pg
import scene_management as scene
import game_objects as go

### ↓ GAME LOGIC HERE ↓ ###

# Scenes :
SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 600
SCREEN_SIZE = (SCREEN_WIDTH, SCREEN_HEIGHT)
SCREEN_CENTER = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)

BACKGROUND_LAYER = 0
GARBAGE_LAYER = 1
COCKPIT_LAYER = 2
BUTTONS_LAYER = 3

class GameScene(scene.Scene) :
    def load(self) :
        background = ZoomingBackground(image=self.assets.get("background.png"), position=SCREEN_CENTER, layer=BACKGROUND_LAYER)
        cockpit = go.GameObject(image=self.assets.get("cockpit.png"),position=SCREEN_CENTER, layer=COCKPIT_LAYER)
        red_button = go.GameObject(image=self.assets.get("red_button.png"), position=(600, 520), layer=COCKPIT_LAYER)

        ###TEMP
        garbage = Garbage(image=self.assets.get("garbage/fresh_fish.png"), position=SCREEN_CENTER, layer=GARBAGE_LAYER, scaling_speed=0.5, max_scale=2.5)

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
            self.destroy()