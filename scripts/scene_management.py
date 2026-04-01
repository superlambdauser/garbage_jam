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

    def switch(self, scene) :
        self.current = scene
    
    def update(self, dt) :
        self.current.update(dt)

    def draw(self, surface) :
        self.current.draw(surface)

class Scene :
    manager = go.GameManager()
    assets = AssetsManager()

    def __init__(self):
        self.manager.clear_all()
        self.load()
    
    def load(self) :
        raise NotImplementedError("Scenes must implement objects loading method load() !")
    
    def update(self, dt) :
        self.manager.update(dt)
    
    def draw(self, surface) :
        self.manager.draw(surface)
