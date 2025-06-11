import pygame
import os

class AnimationManager:
    def __init__(self, game):
        self.game = game
        self.animations = {
            "IDLE": {"frames": 9, "path": "IDLE.png"},
            "WALKING": {"frames": 8, "path": "WALKING.png"}
        }
        self.current_animation = "IDLE"
        self.current_frame = 0
        self.animation_speed = 0.15
        self.animation_timer = 0
        self.sprites = {}
        self._load_all_animations()
        
    def _load_all_animations(self):
        base_path = os.path.join("assets", "sprites", "player")
        for anim_name, anim_data in self.animations.items():
            try:
                sprite_path = os.path.join(base_path, anim_data["path"])
                if not os.path.exists(sprite_path):
                    print(f"Warning: Missing animation file {sprite_path}")
                    continue
                
                sprite_sheet = pygame.image.load(sprite_path).convert_alpha()
                frame_width = sprite_sheet.get_width() // anim_data["frames"]
                frames = []
                
                for i in range(anim_data["frames"]):
                    frame = sprite_sheet.subsurface(
                        i * frame_width, 0,
                        frame_width, sprite_sheet.get_height()
                    )
                    frames.append(frame)
                
                self.sprites[anim_name] = frames
                print(f"Loaded {len(frames)} frames for {anim_name}")
                
            except Exception as e:
                print(f"Error loading animation {anim_name}: {str(e)}")
                self.sprites[anim_name] = []  # Пустой список для избежания ошибок

    def get_current_frame(self):
        if not self.sprites.get(self.current_animation):
            return None
            
        try:
            return self.sprites[self.current_animation][self.current_frame]
        except IndexError:
            print(f"Animation frame error: {self.current_animation}[{self.current_frame}]")
            return self.sprites[self.current_animation][0] if self.sprites[self.current_animation] else None

    def update(self, dt, is_moving=False):
        prev_animation = self.current_animation
        self.current_animation = "WALKING" if is_moving else "IDLE"
        
        # Сброс кадра при смене анимации
        if prev_animation != self.current_animation:
            self.current_frame = 0
            self.animation_timer = 0
            
        if not self.sprites.get(self.current_animation):
            return
            
        self.animation_timer += dt
        if self.animation_timer >= self.animation_speed:
            self.animation_timer = 0
            self.current_frame = (self.current_frame + 1) % len(self.sprites[self.current_animation])
