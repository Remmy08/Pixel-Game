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
        print("Инициализация Pygame...")
        pygame.init()
        print(f"Pygame инициализирован: {pygame.get_init()}")
        
        # Проверка модулей
        print(f"Display: {pygame.display.get_init()}")
        print(f"Font: {pygame.font.get_init()}")
        self.settings = settings.Settings()
        
        # Создание окна
        self.screen = pygame.display.set_mode(
            (self.settings.SCREEN_WIDTH, self.settings.SCREEN_HEIGHT))
        pygame.display.set_caption("Пиксельная Игра")
        
        # Загрузка карты
        self.tilemap = tilemap.Tilemap(self, "maps/Map.json")
        
        # Игровые объекты
        self.clock = pygame.time.Clock()
        self.player = player.Player(self)
        self.camera = camera.Camera(self)
        self.debug = debug.DebugDisplay(self)
        
        # Установка позиции спавна
        if hasattr(self.tilemap, 'objects') and "spawn" in self.tilemap.objects:
            spawn_pos = self.tilemap.objects["spawn"]
            print(f"Установка позиции спавна: {spawn_pos}")  # Добавляем лог
            self.player.position = pygame.math.Vector2(spawn_pos.x, spawn_pos.y)
            self.player.rect.center = (spawn_pos.x, spawn_pos.y)
    
    def run(self):
        while True:
            try:
                dt = self.clock.tick(self.settings.FPS) / 1000.0
                
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_ESCAPE:
                            pygame.quit()
                            sys.exit()
                        if event.key == pygame.K_e:
                            self._handle_interaction()
                        if event.key == pygame.K_F1:
                            self.settings.SHOW_COLLISIONS = not self.settings.SHOW_COLLISIONS
                
                self.player.update(dt)
                self.camera.update()
                
                self.screen.fill(self.settings.BACKGROUND)
                self.tilemap.draw(self.screen, self.camera)
                self.debug.show_collisions(self.screen, self.camera)
                self.player.draw(self.screen, self.camera)
                self.debug.show()
                
                pygame.display.flip()
                
            except Exception as e:
                print(f"Error in game loop: {str(e)}")
                continue  # Продолжаем игру после ошибки
    
    def _handle_interaction(self):
        """Обработка взаимодействия с объектами"""
        if not hasattr(self.tilemap, 'objects'):
            return
            
        player_rect = self.player.rect
        
        # Проверка алтаря
        if "altar" in self.tilemap.objects:
            altar = self.tilemap.objects["altar"]
            if altar and player_rect.colliderect(altar["rect"]):
                print("Взаимодействие с алтарем")
        
        # Проверка деревьев
        if "trees" in self.tilemap.objects:
            for tree_id, tree in self.tilemap.objects["trees"].items():
                if not tree["is_cut"] and player_rect.colliderect(tree["rect"]):
                    print(f"Удар по дереву {tree_id}")

if __name__ == "__main__":
    print("=== Запуск игры ===")
    try:
        game = Game()
        print("Игра инициализирована")
        game.run()
    except Exception as e:
        print(f"Ошибка: {e}")
        pygame.quit()