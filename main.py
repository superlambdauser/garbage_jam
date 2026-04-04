import asyncio

import pygame as pg
import scene_management as scenes
import game 

SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 600
SCREEN_SIZE = (SCREEN_WIDTH, SCREEN_HEIGHT)

BACKGROUND_LAYER = 0
GARBAGE_LAYER = 1
COCKPIT_LAYER = 2
BUTTONS_LAYER = 3

async def main() :
# Pygame setup :
    pg.mixer.pre_init(22050, -16, 2, 4096) # Don't ask
    pg.init()

    pg.display.set_caption("Space garbage collector") # Temp title
    pg.display.set_icon(pg.image.load("assets/mop.png")) # lol

    screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    clock = pg.time.Clock()
    running = True

    scene_manager = scenes.SceneManager()

    scene_manager.switch(game.StartScene()) # MenuScene later 

    while running:
        dt = clock.tick(60) / 1000

        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
            scene_manager.handle_event(event)

        screen.fill((0,0,0))
        scene_manager.update(dt)
        scene_manager.draw(screen)
        pg.display.flip()

        await asyncio.sleep(0)

    pg.quit() #coucou

asyncio.run(main())