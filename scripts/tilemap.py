import pygame
import json
import os

class TileMap:
    def __init__(self, game, map_file):
        self.game = game
        self.settings = game.settings
        self.load_map(map_file)
        self.collision_layer = None
        self._process_collision_layer()
    
    def load_map(self, map_file):
        """Загрузка карты из JSON файла"""
        with open(map_file, 'r') as f:
            map_data = json.load(f)
        
        self.tilewidth = map_data['tilewidth']
        self.tileheight = map_data['tileheight']
        self.width = map_data['width'] * self.tilewidth
        self.height = map_data['height'] * self.tileheight
        
        # Находим слой коллизий
        for layer in map_data['layers']:
            if layer['name'] == 'collisions':
                self.collision_layer = layer
                break
    
    def _process_collision_layer(self):
        """Создаем прямоугольники коллизий"""
        self.collision_rects = []
        
        if not self.collision_layer:
            return
        
        for y in range(self.collision_layer['height']):
            for x in range(self.collision_layer['width']):
                idx = x + y * self.collision_layer['width']
                if self.collision_layer['data'][idx] != 0:
                    self.collision_rects.append(
                        pygame.Rect(
                            x * self.tilewidth,
                            y * self.tileheight,
                            self.tilewidth,
                            self.tileheight
                        )
                    )
    
    def draw_collisions(self, surface, camera):
        """Отрисовка зон коллизий (для отладки)"""
        if not self.settings.SHOW_COLLISIONS:
            return
            
        for rect in self.collision_rects:
            pygame.draw.rect(surface, self.settings.COLLISION_COLOR, 
                           camera.apply(rect))
    
    def check_collision(self, rect):
        """Проверка коллизий с картой"""
        for collision_rect in self.collision_rects:
            if rect.colliderect(collision_rect):
                return True
        return False