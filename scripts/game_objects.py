import pygame as pg

# GameManager → pg.sprite.LayeredUpdates
class GameManager:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._group = pg.sprite.LayeredUpdates()  # ← composition not inheritance
        return cls._instance

    def add(self, sprite, layer):
        self._group.add(sprite, layer=layer)

    def update(self, dt):
        self._group.update(dt)

    def draw(self, surface):
        self._group.draw(surface)

    def remove(self, sprite):
        self._group.remove(sprite)

# GameObject → pg.sprite.Sprite
class GameObject(pg.sprite.Sprite):
    def __init__(self, image: pg.Surface, position: tuple, layer: int):
        super().__init__()
        self.image = image
        self.rect = image.get_rect(center=position)
        GameManager().add(self, layer=layer)

    def destroy(self):
        self.kill()


class ZoomingObject(GameObject):
    def __init__(self, scaling_speed: float = 0.03, max_scale: float = 3.0, **kwargs):
        super().__init__(**kwargs)
        self.original = self.image
        self.scale = 1.0
        self.scaling_speed = scaling_speed
        self.max_scale = max_scale

    def update(self, dt: float):
        self.scale += self.scaling_speed * dt
        new_w = int(self.original.get_width() * self.scale)
        new_h = int(self.original.get_height() * self.scale)
        self.image = pg.transform.smoothscale(self.original, (new_w, new_h))
        self.rect = self.image.get_rect(center=self.rect.center)  # recentering after scale


class RotatingObject(GameObject):
    def __init__(self, rotation_speed: float = 5.0, **kwargs):
        super().__init__(**kwargs)
        self.original = self.image
        self.angle = 0.0
        self.rotation_speed = rotation_speed

    def update(self, dt: float):
        self.angle += self.rotation_speed * dt
        self.image = pg.transform.rotate(self.original, self.angle)
        self.rect = self.image.get_rect(center=self.rect.center)


class ZoomingRotatingObject(ZoomingObject, RotatingObject):
    def update(self, dt: float):
        self.scale += self.scaling_speed * dt
        self.angle += self.rotation_speed * dt
        zoomed = pg.transform.smoothscale(self.original, (
            int(self.original.get_width() * self.scale),
            int(self.original.get_height() * self.scale)
        ))
        self.image = pg.transform.rotate(zoomed, self.angle)
        self.rect = self.image.get_rect(center=self.rect.center)

class ZoomingBackground(ZoomingObject) :
    def __init__(self, scaling_speed = 0.03, max_scale = 3, **kwargs):
        super().__init__(scaling_speed, max_scale, **kwargs)
        self.min_scale = self.scale

    def update(self, dt):
        super().update(dt)
        if self.scale > self.max_scale :
            self.scale = self.min_scale

class Garbage(ZoomingRotatingObject):
    def update(self, dt):
        super().update(dt)
        if self.scale > self.max_scale:
            self.destroy()