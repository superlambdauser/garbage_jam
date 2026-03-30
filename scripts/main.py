import pygame as pg
import game_objects as go

SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 600

# Pygame setup :
pg.init()
screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pg.time.Clock()
running = True

# Files :
bg_image = pg.image.load("assets/background.png").convert() # Auto converts image in the most suitable format for pygame to run smoothly
# Game objects :
game = go.GameManager()
zoom_bg = go.ZoomBackground(bg_image, (SCREEN_WIDTH, SCREEN_HEIGHT))


while running:
    dt = clock.tick(60) / 1000 # FPS limit = 60, divided by 1000 to get speed in seconds instead of milliseconds
    
    for event in pg.event.get(): 
        if event.type == pg.QUIT: # pg.QUIT event means the user clicked X to close your window
            running = False
            pg.quit() 

    game.update(dt)
    game.draw(screen)

    pg.display.flip() # Update screen 



pg.quit() #coucou