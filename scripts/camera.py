import pygame

class Camera:
    def __init__(self, game):
        self.game = game
        self.offset = pygame.math.Vector2()
    
    def update(self):
        # Используем размеры виртуального экрана
        target_x = self.game.player.rect.centerx - self.game.settings.VIRTUAL_WIDTH // 2
        target_y = self.game.player.rect.centery - self.game.settings.VIRTUAL_HEIGHT // 2
        
        # Плавное следование камеры
        self.offset.x += (target_x - self.offset.x) * 0.1
        self.offset.y += (target_y - self.offset.y) * 0.1
    
    def apply(self, rect):
        """Применяет смещение камеры к прямоугольнику"""
        return rect.move(-self.offset.x, -self.offset.y)