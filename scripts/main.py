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

# Game objects :
game = go.GameManager()
game.set_screen_size(SCREEN_SIZE)

zoom_bg = go.ZoomBackground(image=bg_image, layer_idx=BACKGROUND_LAYER)

cockpit = go.StaticObject(image=cockpit_image, layer_idx=COCKPIT_LAYER)

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