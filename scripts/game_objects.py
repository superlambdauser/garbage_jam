import pygame as pg

# GameManager → pg.sprite.LayeredUpdates
class GameManager:
    """
    Singleton instance wrapping LayeredUpdates() instance and custom behaviours.    
    """
    _instance = None

    def __new__(cls): # Singleton pattern
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._group = pg.sprite.LayeredUpdates()
        return cls._instance

    def add(self, sprite, layer):
        self._group.add(sprite, layer=layer)

    def remove(self, sprite):
        if sprite in self._group :
            self._group.remove(sprite)

    def clear_all(self) :
        self._group.empty()

    def handle_event(self, event):
        for sprite in self._group.sprites():
            if isinstance(sprite, InteractiveObject):
                sprite.handle_event(event)

    def update(self, dt):
        self._group.update(dt)

    def draw(self, surface):
        for layer in self._group.layers():
            layer_sprites = self._group.get_sprites_from_layer(layer)
            
            if layer == 1:  # Garbage layer
                layer_sprites = list(reversed(layer_sprites))
            
            for sprite in layer_sprites:
                surface.blit(sprite.image, sprite.rect)

# GameObject
class GameObject(pg.sprite.Sprite):
    def __init__(self, image: pg.Surface, position: tuple, layer: int):
        """Wrapper for Sprite() objects.

        Args:
            image (pg.Surface): Image to display
            position (tuple): Spawn position
            layer (int): Display layer
        """
        super().__init__()
        self.image = image
        self.rect = image.get_rect(center=position)
        GameManager().add(self, layer=layer)

    def destroy(self):
        self.kill()

class ZoomingObject(GameObject):
    def __init__(self, scaling_speed: float = 0.03, max_scale: float = 3.0, **kwargs):
        """Object that zooms in (positive speed) or out (negative speed) over time.

        Args:
            scaling_speed (float, optional): Zooming speed. Must be set negative for a zooming out behaviour. Defaults to 0.03.
            max_scale (float, optional): Maximum scaling before reset/destroy/other behaviours trigger. Defaults to 3.0.
        """
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
        """Objects that rotate over time.
        Positive speed = anti-clockwise direction.
        Negative speed = clockwise direction.

        Args:
            rotation_speed (float, optional): Rotation speed. Defaults to 5.0.
        """
        super().__init__(**kwargs)
        self.original = self.image
        self.angle = 0.0
        self.rotation_speed = rotation_speed

    def set_speed(self, speed:float) :
        self.rotation_speed = speed 

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

# Interactive Objects :
class InteractiveObject(GameObject) :
    def handle_event(self, event) :
        raise NotImplementedError("Interactive Objects must implement a handle_event method.")

class ClickableObject(InteractiveObject) : 
    def handle_event(self, event):
        if event.type == pg.MOUSEBUTTONDOWN :
            if self.rect.collidepoint(event.pos) :
                self.on_click()
    
    def on_click() :
        raise NotImplementedError("Clickable Objects must implement on_click() method.")
    
    
# Visual effects objects :
class AnimatedObject(GameObject) :
    def __init__(self, images:list, position, layer):
        super().__init__(images[0], position, layer) #Initializes Sprite with first image of the list

    def animate(self) :
        raise NotImplementedError("Animated objects must implements animate() method.")
    
class HoverEffectObject(GameObject) :
    def __init__(self, hover_image, image, position, layer):
        super().__init__(image, position, layer)
        self.original = image
        self.hover_image = hover_image

    def hover_effect(self) :
        if self.rect.collidepoint(pg.mouse.get_pos()) :
            self.image = self.hover_image
        else : 
            self.image = self.original