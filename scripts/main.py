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

zoom_bg = go.ZoomingBackground(image=bg_image, position=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2), layer=BACKGROUND_LAYER, scaling_speed=0.03, max_scale=3.0)
cockpit = go.GameObject(image=cockpit_image, position=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2), layer=COCKPIT_LAYER)
red_button = go.GameObject(image=red_button_image, position=(600, 520), layer=COCKPIT_LAYER)
garbage = go.Garbage(image=garbage_image, position=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2), layer=GARBAGE_LAYER, scaling_speed=0.5, max_scale=2.5)

while running:
    dt = clock.tick(60) / 1000

    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False

    screen.fill((0, 0, 0))
    game.update(dt)
    game.draw(screen)
    pg.display.flip()

pg.quit() #coucou