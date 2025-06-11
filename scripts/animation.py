import pygame
import os

class AnimationManager:
    def __init__(self, game):
        self.game = game
        self.animations = {
            "IDLE": {"frames": 9, "width": 864, "height": 64, "frame_width": 96},
            "WALKING": {"frames": 8, "width": 768, "height": 64, "frame_width": 96}
        }
        self.current_animation = "IDLE"
        self.current_frame = 0
        self.animation_speed = 0.15
        self.animation_timer = 0
        self.sprites = {}
        
        self.load_sprites()
    
    def load_sprites(self):
        """Загрузка спрайтов без масштабирования"""
        base_path = os.path.join("assets", "sprites", "player")
        
        for anim_name, anim_data in self.animations.items():
            sprite_path = os.path.join(base_path, f"{anim_name}.png")
            
            if os.path.exists(sprite_path):
                sprite_sheet = pygame.image.load(sprite_path).convert_alpha()
                frames = []
                
                # Нарезаем спрайтшит на кадры
                for i in range(anim_data["frames"]):
                    frame = sprite_sheet.subsurface(
                        i * anim_data["frame_width"], 0,
                        anim_data["frame_width"], anim_data["height"]
                    )
                    frames.append(frame)
                
                self.sprites[anim_name] = frames
    
    def get_current_frame(self):
        """Возвращает текущий кадр в оригинальном размере"""
        if self.current_animation in self.sprites:
            return self.sprites[self.current_animation][self.current_frame]
        return None
    
    def update(self, dt, is_moving=False):
        self.current_animation = "WALKING" if is_moving else "IDLE"
        self.animation_timer += dt
        
        if self.animation_timer >= self.animation_speed:
            self.animation_timer = 0
            frames_count = len(self.sprites[self.current_animation])
            self.current_frame = (self.current_frame + 1) % frames_count