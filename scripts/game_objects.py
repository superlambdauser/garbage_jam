import pygame as pg

# GameManager (wrapper for pg.sprite.LayeredUpdates)
class GameManager:
    """
    Singleton instance wrapping LayeredUpdates() instance and custom behaviours.    
    """
    _instance = None

    def __new__(cls): # Singleton pattern
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._group = pg.sprite.LayeredUpdates()
            cls._instance._update_order = None  # default: layer order
        return cls._instance

    def add(self, sprite, layer):
        self._group.add(sprite, layer=layer)

    def remove(self, sprite):
        if sprite in self._group :
            self._group.remove(sprite)

    def clear_all(self) :
        self._group.empty()

    # Convenience accessors :
    def get_all_in_layer(self, layer) -> list:
        return self._group.get_sprites_from_layer(layer)

    def handle_event(self, event):
        for sprite in self._group.sprites():
            if isinstance(sprite, InteractiveObject):
                sprite.handle_event(event)

    def update(self, dt):
        self._group.update(dt)

    def draw(self, surface):
        for layer in self._group.layers():
            layer_sprites = self.get_all_in_layer(layer)
            
            if layer == 1:  # Garbage layer
                layer_sprites = list(reversed(layer_sprites))
            
            for sprite in layer_sprites:
                surface.blit(sprite.image, sprite.rect)
                if isinstance(sprite, HoverEffectObject) and sprite.is_hovered():
                    surface.blit(sprite.get_outline(), sprite.rect)

            # GameObject
class GameObject(pg.sprite.Sprite):
    def __init__(self, image: pg.Surface, position:tuple, layer: int):
        """Wrapper for Sprite() objects.

        Args:
            image (pg.Surface): Image to display
            position (tuple): Spawn position
            layer (int): Display layer
        """
        super().__init__()
        self.image = image
        self.position = position
        self.rect = image.get_rect(center=position)
        self.mask = pg.mask.from_surface(self.image)
        GameManager().add(self, layer=layer)

    def update(self, dt:float) :
        pass

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

    def update(self, dt:float):
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
        self.mask = pg.mask.from_surface(self.image)
        self.rect = self.image.get_rect(center=self.rect.center)

# Interactive Objects :
class InteractiveObject(GameObject) :
    def handle_event(self, event) :
        raise NotImplementedError("Interactive Objects must implement a handle_event method.")

class ClickableObject(InteractiveObject) : 
    def __init__(self, image, position, layer):
        super().__init__(image, position, layer)
        self.is_clicked = False
    def is_hovered(self) -> bool:
        return self.rect.collidepoint(pg.mouse.get_pos())
    
    def handle_event(self, event):
        if event.type == pg.MOUSEBUTTONDOWN :
            if self.is_hovered() :
                self.is_clicked = True
                self.on_click()
        elif event.type == pg.MOUSEBUTTONUP :
            self.is_clicked = False
    
    def on_click() :
        raise NotImplementedError("Clickable Objects must implement on_click() method.")
    
class SnappingObject(GameObject) :
    def __init__(self, image, position, layer):
        super().__init__(image, position, layer)
        self.threshold = 0 # Defaults to no snapping

    def snap_to(self, target:GameObject) :
        self.set_position(target.rect.center)
    
    def is_near(self, target: GameObject, threshold:float) :
        a = pg.math.Vector2(self.rect.center)
        b = pg.math.Vector2(target.rect.center)
        return a.distance_to(b) <= threshold
    
# Visual effects objects :
class AnimatedObject(GameObject) :
    def __init__(self, images:list, position, layer, frame_duration:float=0.1):
        super().__init__(images[0], position, layer) #Initializes Sprite with first image of the list
        self.images = images

        self.frame = 0
        self.frame_timer = 0
        self.frame_duration = frame_duration  # ms per frame

        self.is_animating = False

    def animate(self, dt):
        self.frame_timer += dt
        if self.frame_timer >= self.frame_duration:
            self.frame_timer = 0
            self.frame += 1
            if self.frame >= len(self.images): # Reset to idle & end animation
                self.frame = 0
                self.is_animating = False
        self.image = self.images[self.frame]

    def update(self, dt):
        if self.is_animating:
            self.animate(dt)
    
class HoverEffectObject(GameObject) :
    def is_hovered(self) -> bool :
        mouse_pos = pg.mouse.get_pos()
        if not self.rect.collidepoint(mouse_pos):
            return False
        local_x = mouse_pos[0] - self.rect.x
        local_y = mouse_pos[1] - self.rect.y
        return self.mask.get_at((local_x, local_y))
    
class OutlineHoverEffectObjects(HoverEffectObject) :
    def __init__(self, image, position, layer):
        super().__init__(image, position, layer)
        self.color = (255, 255, 255) # White
        self.thickness = 2

    def get_outline(self,) :
        if not hasattr(self, '_outline'):
            outline_surf = pg.Surface(self.image.get_size(), pg.SRCALPHA)
            for point in self.mask.outline():
                pg.draw.circle(outline_surf, self.color, point, self.thickness) # Many small circles that mimic a thickened outline
            self._outline = outline_surf
        return self._outline