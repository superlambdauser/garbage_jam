import pygame as pg
import game_objects as go

SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 600
SCREEN_SIZE = (SCREEN_WIDTH, SCREEN_HEIGHT)

BACKGROUND_LAYER = 0
GARBAGE_LAYER = 1
COCKPIT_LAYER = 2
BUTTONS_LAYER = 3

# Pygame setup :
pg.init()
pg.display.set_caption("Space garbage collector") # Temp title
screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pg.time.Clock()
running = True

# Files :
bg_image = pg.image.load("assets/background.png").convert_alpha()
cockpit_image = pg.image.load("assets/cockpit.png").convert_alpha()
red_button_image = pg.image.load("assets/red_button.png").convert_alpha()

garbage_image = pg.image.load("assets/garbage/fresh_fish.png").convert_alpha() ### TEMP

# Game objects :
game = go.GameManager()
game.set_screen_size(SCREEN_SIZE)
zoom_bg = go.ZoomingBackground(image=bg_image, screen_size=SCREEN_SIZE, layer_idx=BACKGROUND_LAYER)
cockpit = go.StaticObject(image=cockpit_image, screen_size=SCREEN_SIZE, layer_idx=COCKPIT_LAYER)
red_button = go.StaticObject(image=red_button_image, screen_size=SCREEN_SIZE, layer_idx=COCKPIT_LAYER, position=(600,520))

garbage = go.Garbage(image=garbage_image, layer_idx=GARBAGE_LAYER, scaling_speed=0.5, max_scale=2.5) ### TEMP

while running:
    dt = clock.tick(60) / 1000 # FPS limit = 60, divided by 1000 to get speed in seconds instead of milliseconds
    
    for event in pg.event.get(): 
        if event.type == pg.QUIT: # pg.QUIT event means the user clicked X to close window
            running = False
            pg.quit() 

    game.update(dt)
    game.draw(screen)

    pg.display.flip() # Update screen 

pg.quit() #coucou