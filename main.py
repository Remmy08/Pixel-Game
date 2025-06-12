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
        
        self.settings = settings.Settings()
        
        # Создание окна и виртуальной поверхности
        self.screen = pygame.display.set_mode(
            (self.settings.SCREEN_WIDTH, self.settings.SCREEN_HEIGHT))
        self.virtual_screen = pygame.Surface(
            (self.settings.VIRTUAL_WIDTH, self.settings.VIRTUAL_HEIGHT))
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
            print(f"Установка позиции спавна: {spawn_pos}")
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
                            self.settings.SHOW_DEBUG = not self.settings.SHOW_DEBUG
                            self.settings.SHOW_COLLISIONS = not self.settings.SHOW_COLLISIONS
                
                self.player.update(dt)
                self.camera.update()
                
                # Отрисовка на виртуальный экран
                self.virtual_screen.fill(self.settings.BACKGROUND)
                self.tilemap.draw(self.virtual_screen, self.camera)
                self.debug.show_collisions(self.virtual_screen, self.camera)
                self.player.draw(self.virtual_screen, self.camera)
                self.debug.show(self.virtual_screen)  # Только один вызов с параметром
                
                # Масштабирование виртуального экрана на основной
                scaled_screen = pygame.transform.scale(
                    self.virtual_screen, 
                    (self.settings.SCREEN_WIDTH, self.settings.SCREEN_HEIGHT))
                self.screen.blit(scaled_screen, (0, 0))
                
                pygame.display.flip()
                
            except Exception as e:
                print(f"Error in game loop: {str(e)}")
                continue

if __name__ == "__main__":
    print("=== Запуск игры ===")
    try:
        game = Game()
        print("Игра инициализирована")
        game.run()
    except Exception as e:
        print(f"Ошибка: {e}")
        pygame.quit()