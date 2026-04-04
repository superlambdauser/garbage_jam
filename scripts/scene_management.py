import os
import pygame as pg
import game_objects as go

# Assets Manager :
class AssetsManager:
    """
    Assets manager avoids loading the same asset multiple times in and between scenes.
    """
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._cache = {}
            cls._instance._base_path = "assets/" # Default path to assets
        return cls._instance
    
    def set_base_path(self, path: str):
        self._base_path = path

    def get(self, path: str) -> pg.Surface:
        full_path = os.path.join(self._base_path, path)
        if full_path not in self._cache:
            self._cache[full_path] = pg.image.load(full_path).convert_alpha()
        return self._cache[full_path]

# Scenes :
class SceneManager :
    _instance = None

    def __new__(cls): # Singleton pattern
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self):
        self.current = None

    def switch(self, new_scene) :
        if self.current_scene:
            self.current_scene.unload()  # cleanup listeners
        self.current_scene = new_scene
        self.current_scene.load()

    def handle_event(self, event) :
        self.current.handle_event(event)
    
    def update(self, dt) :
        self.current.update(dt)

    def draw(self, surface) :
        self.current.draw(surface)

class Scene :
    _manager = go.GameManager()

    def __init__(self):
        self._manager.clear_all()
        self.assets = AssetsManager()
        self.load()
    
    def load(self) :
        raise NotImplementedError("Scenes must implement objects loading method load() !")
    
    def unload(self):
        self._unregister_events()

    def _register_events(self):
        pass  # override only in subclasses that need it

    def _unregister_events(self):
        pass  # override only in subclasses that need it

    def handle_event(self, event) :
        self._manager.handle_event(event)
    
    def update(self, dt) :
        self._manager.update(dt)
    
    def draw(self, surface) :
        self._manager.draw(surface)
