import pygame
import sys
import os
import json
from scripts import settings
from scripts import player
from scripts import camera
from scripts import debug
from scripts import tilemap

class Game:
    def __init__(self):
        pygame.init()
        self.settings = settings.Settings()
        
        # Создание окна
        self.screen = pygame.display.set_mode(
            (self.settings.SCREEN_WIDTH, self.settings.SCREEN_HEIGHT))
        pygame.display.set_caption("Пиксельная Игра")
        
        # Игровые объекты
        self.clock = pygame.time.Clock()
        
        # Загрузка карты
        self._create_temp_map()
        self.tilemap = tilemap.TileMap(self, "temp_map.json")
        
        self.player = player.Player(self)
        self.camera = camera.Camera(self)
        self.debug = debug.DebugDisplay(self)
    
    def _create_temp_map(self):
        """Создание временной карты для тестирования"""
        map_data = {
            "tilewidth": 16,
            "tileheight": 16,
            "width": 40,
            "height": 30,
            "layers": [
                {
                    "name": "collisions",
                    "data": [1 if x == 0 or x == 39 or y == 0 or y == 29 or 
                            (10 < x < 30 and 10 < y < 20) else 0 
                            for y in range(30) for x in range(40)]
                }
            ]
        }
        
        with open("temp_map.json", "w") as f:
            json.dump(map_data, f)
    
    def run(self):
        while True:
            # Рассчитываем delta time для плавной анимации
            dt = self.clock.tick(self.settings.FPS) / 1000.0  # В секундах
            
            # Обработка событий
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        sys.exit()
                    if event.key == pygame.K_F1:
                        self.settings.SHOW_COLLISIONS = not self.settings.SHOW_COLLISIONS
                    if event.key == pygame.K_q:
                        # Переключение инструмента (если реализовано)
                        if hasattr(self.player, 'switch_tool'):
                            self.player.switch_tool()
            
            # Обновление игровой логики с передачей delta time
            self.player.update(dt)  # Теперь передаем dt
            self.camera.update()
            
            # Отрисовка
            self.screen.fill(self.settings.BACKGROUND)
            
            # Рисуем коллизии (если включено)
            if hasattr(self.tilemap, 'draw_collisions'):
                self.tilemap.draw_collisions(self.screen, self.camera)
            
            # Рисуем игрока (новый метод draw)
            self.player.draw(self.screen, self.camera)
            
            # Отладочная информация
            self.debug.show()
            
            # Дополнительная отладочная информация
            debug_text = [
                f"Animation: {self.player.animation.current_animation}",
                f"Frame: {self.player.animation.current_frame}",
                f"Direction: {self.player.direction}"
            ]
            
            if hasattr(self.player, 'current_tool'):
                debug_text.append(f"Tool: {self.player.current_tool} (Q to switch)")
            
            for i, text in enumerate(debug_text):
                text_surface = self.debug.font.render(text, True, self.settings.DEBUG_TEXT)
                self.screen.blit(text_surface, (10, 90 + i * 20))
            
            pygame.display.flip()

if __name__ == "__main__":
    game = Game()
    game.run()