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
            
            # Обновление
            self.player.update()
            self.camera.update()
            
            # Отрисовка
            self.screen.fill(self.settings.BACKGROUND)
            self.tilemap.draw_collisions(self.screen, self.camera)
            pygame.draw.rect(self.screen, self.settings.PLAYER_COLOR,
                           self.camera.apply(self.player.rect))
            self.debug.show()
            
            pygame.display.flip()
            self.clock.tick(self.settings.FPS)

if __name__ == "__main__":
    game = Game()
    game.run()