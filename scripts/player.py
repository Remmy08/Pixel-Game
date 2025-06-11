import pygame
from .animation import AnimationManager

class Player:
    def __init__(self, game):
        self.game = game
        self.settings = game.settings
        
        # Анимации
        self.animation = AnimationManager(game)
        
        # Направление и движение
        self.direction = "right"
        self.moving = False
        
        # Размеры (теперь используем оригинальные размеры спрайтов)
        sample_frame = self.animation.get_current_frame()
        self.width = sample_frame.get_width() if sample_frame else 96
        self.height = sample_frame.get_height() if sample_frame else 64
        
        # Позиция и хитбокс
        self.position = pygame.math.Vector2(100, 100)
        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.rect.center = self.position
        
        # Скорость (увеличим для больших спрайтов)
        self.speed = self.settings.PLAYER_SPEED * 2
    
    def update(self, dt):
        self._get_input()
        self._move(dt)
        self.animation.update(dt, self.moving)
    
    def _get_input(self):
        keys = pygame.key.get_pressed()
        
        self.moving = False
        
        if keys[pygame.K_a]:
            self.direction = "left"
            self.moving = True
        elif keys[pygame.K_d]:
            self.direction = "right"
            self.moving = True
        if keys[pygame.K_w] or keys[pygame.K_s]:
            self.moving = True
    
    def _move(self, dt):
        if self.moving:
            # Горизонтальное движение
            if self.direction == "left":
                self.position.x -= self.speed * dt * 60
            elif self.direction == "right":
                self.position.x += self.speed * dt * 60
            
            # Вертикальное движение
            keys = pygame.key.get_pressed()
            if keys[pygame.K_w]:
                self.position.y -= self.speed * dt * 60
            if keys[pygame.K_s]:
                self.position.y += self.speed * dt * 60
            
            self.rect.center = self.position
            
            # Проверка коллизий (если есть)
            if hasattr(self.game, 'tilemap') and self.game.tilemap.check_collision(self.rect):
                self.position.x = self.rect.centerx
                self.position.y = self.rect.centery
    
    def draw(self, surface, camera):
        frame = self.animation.get_current_frame()
        if frame:
            # Зеркалим для левого направления
            if self.direction == "left":
                frame = pygame.transform.flip(frame, True, False)
            
            # Позиция с учетом камеры
            screen_pos = camera.apply(self.rect)
            surface.blit(frame, screen_pos)