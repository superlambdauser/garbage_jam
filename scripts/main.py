import pygame as pg

# pygame setup
pg.init()
screen = pg.display.set_mode((1600, 1200))
clock = pg.time.Clock()
running = True

while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False

    # fill the screen with a color to wipe away anything from last frame
    screen.fill("purple")

    # RENDER YOUR GAME HERE

    pg.display.flip() # Update screen 

    clock.tick(60)  # FPS limit = 60

pg.quit()#coucou