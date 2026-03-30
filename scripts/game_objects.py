import pygame as pg

class GameManager:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._objects = []
        return cls._instance

    def add(self, obj: "GameObject"):
        self._objects.append(obj)

    def remove(self, obj: "GameObject"):
        self._objects.remove(obj)

    def clear(self):
        self._objects.clear()

    def update(self, dt: float):
        for obj in self._objects:
            obj.update(dt)

    def draw(self, surface: pg.Surface):
        for obj in self._objects:
            obj.draw(surface)

class GameObjectMeta(type):
    '''Metaclass that auto-registers all GameObject subclasses.'''
    _registry: list = []

    def __call__(cls, *args, **kwargs):
        instance = super().__call__(*args, **kwargs)

        GameManager().add(instance)  # Singleton ensures it's always the same manager
        return instance

class GameObject(metaclass=GameObjectMeta) :
    '''GameObject is a superclass from which all objects that need update() and draw() methods will inherit.
    Instances are auto-registered on creation.'''
    def update(self, dt:float):
        raise NotImplementedError("Subclass must implement update()")

    def draw(self, surface:pg.surface):
        raise NotImplementedError("Subclass must implement draw()")
    
    def destroy(self) :
        GameManager().remove(self)

class ZoomBackground(GameObject):
    def __init__(self, image:pg.image, screen_size:tuple, scaling_speed:float=0.005, max_scale:float=10.0):
        self.original = image
        self.screen_width, self.screen_height = screen_size

        self.scaling_speed = scaling_speed
        self.max_scale = max_scale

        # Start at a scale that exactly fills the screen, then zoom in from there
        self.min_scale = max(
        self.screen_width / image.get_width(),
        self.screen_height / image.get_height())

        self.scale = self.min_scale

    def update(self, dt:float) :
        self.scale += self.scaling_speed * dt

        if self.scale > self.max_scale :
            self.scale = self.min_scale  # reset back to "just filling the screen"

    def draw(self, surface:pg.surface) :
        new_width = int(self.original.get_width() * self.scale)
        new_height = int(self.original.get_height() * self.scale)

        scaled = pg.transform.smoothscale(self.original, (new_width, new_height))
        rect = scaled.get_rect(center = (self.screen_width // 2, self.screen_height // 2))

        surface.blit(scaled, rect)
        