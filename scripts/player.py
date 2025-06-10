import pygame

class Player:
    def __init__(self, game):
        self.game = game
        self.settings = game.settings
        
        # Прямоугольник игрока
        self.rect = pygame.Rect(
            100, 100,
            self.settings.TILE_SIZE,  # Размер тайла
            self.settings.TILE_SIZE
        )
        
        # Движение
        self.direction = pygame.math.Vector2()
        self.speed = self.settings.PLAYER_SPEED
    
    def update(self):
        self._get_input()
        self._move()
    
    def _get_input(self):
        keys = pygame.key.get_pressed()
        
        # Сброс направления
        self.direction.x = 0
        self.direction.y = 0
        
        # Обработка WASD
        if keys[pygame.K_w]: self.direction.y = -1
        if keys[pygame.K_s]: self.direction.y = 1
        if keys[pygame.K_a]: self.direction.x = -1
        if keys[pygame.K_d]: self.direction.x = 1
        
        # Нормализация диагонального движения
        if self.direction.magnitude() > 0:
            self.direction = self.direction.normalize()
    
    def _move(self):
        # Сохраняем исходную позицию
        original_x = self.rect.x
        original_y = self.rect.y
        
        # Пробуем двигаться по X
        self.rect.x += self.direction.x * self.speed
        if self.game.tilemap.check_collision(self.rect):
            self.rect.x = original_x
        
        # Пробуем двигаться по Y
        self.rect.y += self.direction.y * self.speed
        if self.game.tilemap.check_collision(self.rect):
            self.rect.y = original_y