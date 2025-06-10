import pygame

class Camera:
    def __init__(self, game):
        self.game = game
        self.offset = pygame.math.Vector2()
    
    def update(self):
        # Плавное следование за игроком
        target_x = self.game.player.rect.centerx - self.game.settings.SCREEN_WIDTH // 2
        target_y = self.game.player.rect.centery - self.game.settings.SCREEN_HEIGHT // 2
        
        # Плавное перемещение камеры (Lerp)
        self.offset.x += (target_x - self.offset.x) * 0.1
        self.offset.y += (target_y - self.offset.y) * 0.1
    
    def apply(self, rect):
        # Применяем смещение камеры к объекту
        return rect.move(-self.offset.x, -self.offset.y)