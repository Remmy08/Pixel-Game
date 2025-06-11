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
        
        # Размеры спрайта
        sample_frame = self.animation.get_current_frame()
        self.width = sample_frame.get_width() if sample_frame else 96
        self.height = sample_frame.get_height() if sample_frame else 64
        
        # Позиция и хитбокс
        self.position = pygame.math.Vector2(50, 50)
        self.hitbox_size = 12  # Фиксированный размер хитбокса 32x32
        self._init_hitbox()
        
        # Физика и движение
        self.speed = self.settings.PLAYER_SPEED * 2
        self.velocity = pygame.math.Vector2(0, 0)
        
        # Взаимодействия
        self.interaction_cooldown = 0
        self.interaction_range = 50
    
    def _init_hitbox(self):
        """Инициализация центрированного хитбокса 32x32"""
        self.rect = pygame.Rect(0, 0, self.hitbox_size, self.hitbox_size)
        self.rect.center = self.position
    
    def update(self, dt):
        self._get_input()
        self._move(dt)
        self._update_hitbox_position()
        self.animation.update(dt, self.moving)
        
        if self.interaction_cooldown > 0:
            self.interaction_cooldown -= dt
    
    def _update_hitbox_position(self):
        """Обновление позиции хитбокса относительно персонажа"""
        self.rect.center = self.position
    
    def _get_input(self):
        keys = pygame.key.get_pressed()
        
        self.moving = False
        self.velocity = pygame.math.Vector2(0, 0)
        
        # Обработка горизонтального движения
        if keys[pygame.K_a]:
            self.direction = "left"
            self.velocity.x = -1
            self.moving = True
        if keys[pygame.K_d]:
            self.direction = "right"
            self.velocity.x = 1
            self.moving = True
        
        # Обработка вертикального движения
        if keys[pygame.K_w]:
            self.direction = "up"
            self.velocity.y = -1
            self.moving = True
        if keys[pygame.K_s]:
            self.direction = "down"
            self.velocity.y = 1
            self.moving = True
        
        # Определение диагонального направления
        if self.velocity.x != 0 and self.velocity.y != 0:
            if self.velocity.x > 0 and self.velocity.y < 0:
                self.direction = "up-right"
            elif self.velocity.x > 0 and self.velocity.y > 0:
                self.direction = "down-right"
            elif self.velocity.x < 0 and self.velocity.y < 0:
                self.direction = "up-left"
            elif self.velocity.x < 0 and self.velocity.y > 0:
                self.direction = "down-left"
        
        # Нормализация вектора скорости (чтобы диагональная скорость не была больше)
        if self.velocity.length() > 0:
            self.velocity = self.velocity.normalize()
    
    def _move(self, dt):
        if self.moving:
            move_speed = self.speed * dt * 50  # Оптимальная скорость
            
            # Сохраняем исходную позицию для отката
            original_pos = self.position.copy()
            
            # Временный Rect для проверки коллизий
            temp_rect = self.rect.copy()
            
            # Применяем движение по обеим осям
            temp_rect.x += self.velocity.x * move_speed
            temp_rect.y += self.velocity.y * move_speed
            
            # Проверяем коллизии с новым положением
            if not self.game.tilemap.check_collision(temp_rect):
                self.position.x = temp_rect.centerx
                self.position.y = temp_rect.centery
                self.rect.center = self.position
    
    def draw(self, surface, camera):
        frame = self.animation.get_current_frame()
        if not frame:  # Если кадр не загружен
            # Рисуем простой прямоугольник для отладки
            debug_rect = camera.apply(self.rect)
            pygame.draw.rect(surface, (255, 0, 0), debug_rect)
            return
            
        # Обработка направления для отражения спрайта
        if "left" in self.direction:
            frame = pygame.transform.flip(frame, True, False)
        
        if self.game.settings.SHOW_COLLISIONS:
            debug_rect = camera.apply(self.rect)
            pygame.draw.rect(surface, (0, 255, 0), debug_rect, 1)
        
        # Позиция для отрисовки спрайта (центрирование относительно хитбокса)
        sprite_rect = frame.get_rect(center=self.rect.center)
        screen_pos = camera.apply(sprite_rect)
        surface.blit(frame, screen_pos)
            
    def can_interact(self):
        """Можно ли взаимодействовать с объектами"""
        return self.interaction_cooldown <= 0
    
    def get_interaction_rect(self):
        """Возвращает область взаимодействия перед игроком"""
        if "left" in self.direction:
            return pygame.Rect(
                self.rect.left - self.interaction_range,
                self.rect.top,
                self.interaction_range,
                self.rect.height
            )
        elif "right" in self.direction:
            return pygame.Rect(
                self.rect.right,
                self.rect.top,
                self.interaction_range,
                self.rect.height
            )
        