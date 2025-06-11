import pygame
import json
import os
from pathlib import Path

class Tilemap:
    def __init__(self, game, map_file):
        print(f"Попытка загрузки карты: {os.path.abspath(map_file)}")
        if not os.path.exists(map_file):
            raise FileNotFoundError(f"Файл карты не найден: {map_file}")
        self.game = game
        self.map_data = self._load_map(map_file)
        self.tileset = self._load_tileset()
        self.layers = {}
        self.collisions = []
        self.objects = {
            "trees": {},
            "altar": None,
            "spawn": None
        }
        
        self._process_layers()
        self._process_objects()
    
    def _load_map(self, map_file):
        print(f"Загрузка карты из: {os.path.abspath(map_file)}")  # Отладка
        with open(map_file, 'r') as f:
            data = json.load(f)
        print(f"Путь к тайлсету: {data['tilesets'][0]['image']}")  # Проверка пути
        return data
    
    def _load_tileset(self):
        """Загрузка тайлсета"""
        tileset_data = self.map_data["tilesets"][0]
        image = pygame.image.load(tileset_data["image"]).convert_alpha()
        
        # Создаем поверхность для тайлсета
        tileset = pygame.Surface(
            (tileset_data["imagewidth"], tileset_data["imageheight"]),
            pygame.SRCALPHA
        )
        tileset.blit(image, (0, 0))
        return tileset
    
    def _process_layers(self):
        """Обработка всех слоев карты"""
        for layer in self.map_data["layers"]:
            if layer["type"] == "tilelayer":
                self._process_tile_layer(layer)
            elif layer["type"] == "objectgroup":
                self._process_object_layer(layer)
            elif layer["type"] == "group":
                self._process_group_layer(layer)
    
    def _process_group_layer(self, group):
        """Обработка группы слоев"""
        for layer in group["layers"]:
            if layer["type"] == "tilelayer":
                self._process_tile_layer(layer, group["name"])
            elif layer["type"] == "objectgroup":
                self._process_object_layer(layer, group["name"])
    
    def _process_tile_layer(self, layer, group_name=None):
        layer_name = f"{group_name}_{layer['name']}" if group_name else layer["name"]
        
        # Коллизии обрабатываем только для специального слоя
        if layer["name"] == "Collisions":
            print("Найден слой коллизий!")
            for y in range(layer["height"]):
                for x in range(layer["width"]):
                    idx = x + y * layer["width"]
                    if layer["data"][idx] != 0:
                        self.collisions.append(pygame.Rect(x * 16, y * 16, 16, 16))
            print(f"Загружено {len(self.collisions)} коллизий")
            return  # Прерываем обработку после коллизий
        
        # Остальные слои
        self.layers[layer_name] = []
        for y in range(layer["height"]):
            for x in range(layer["width"]):
                idx = x + y * layer["width"]
                gid = layer["data"][idx]
                if gid == 0:
                    continue
                self.layers[layer_name].append({
                    "pos": (x * 16, y * 16),
                    "gid": gid
                })
    
    def _process_object_layer(self, layer, group_name=None):
        """Обработка слоя объектов"""
        for obj in layer["objects"]:
            # Точка спавна
            if layer["name"] == "Meta" and obj.get("point", False):
                self.objects["spawn"] = pygame.math.Vector2(obj["x"], obj["y"])
            
            # Алтарь
            elif layer["name"] == "Altar":
                self.objects["altar"] = {
                    "rect": pygame.Rect(obj["x"], obj["y"], obj["width"], obj["height"]),
                    "properties": {p["name"]: p["value"] for p in obj.get("properties", [])}
                }
            
            # Деревья
            elif layer["name"] == "Tree_Objects":
                tree_id = next(
                    (p["value"] for p in obj["properties"] if p["name"] == "tree_id"),
                    None
                )
                if tree_id:
                    self.objects["trees"][tree_id] = {
                        "rect": pygame.Rect(obj["x"], obj["y"], obj["width"], obj["height"]),
                        "properties": {p["name"]: p["value"] for p in obj.get("properties", [])},
                        "is_cut": False,
                        "respawn_timer": 0
                    }
    
    def check_collision(self, rect):
        #for i, collision_rect in enumerate(self.collisions[:5]):  # Проверяем только первые 5 для примера
        #    if rect.colliderect(collision_rect):
        #        print(f"Collision with rect {i}: {collision_rect}")
        #        return True
        #return False
        tolerance = 2  # Пиксели
        adjusted_rect = rect.inflate(-tolerance * 2, -tolerance * 2)
        
        for collision in self.collisions:
            if adjusted_rect.colliderect(collision):
                print(f"Collision at {collision} (player: {rect})")
                return True
        return False
    
            
    
    def draw(self, surface, camera):
        """Отрисовка карты с правильным порядком слоев"""
        # Вода
        self._draw_layer(surface, camera, "Water")
        
        # Острова
        self._draw_layer(surface, camera, "Islands_Start_Island")
        self._draw_layer(surface, camera, "Islands_Island_1")
        
        # Основа моста
        self._draw_layer(surface, camera, "Bridges_Bridge_Base")
        
        # Деревья (только несрубленные)
        for tree_id, tree in self.objects["trees"].items():
            if not tree["is_cut"]:
                self._draw_tree(surface, camera, tree_id)
        
        # Статические деревья
        self._draw_layer(surface, camera, "Resources_Trees_Static")
        
        # Поручни моста (поверх всего)
        self._draw_layer(surface, camera, "Bridges_Bridge_Rails")
    
    def _draw_layer(self, surface, camera, layer_name):
        """Отрисовка конкретного слоя"""
        if layer_name in self.layers:
            for tile in self.layers[layer_name]:
                # Получаем тайл из тайлсета
                gid = tile["gid"] - 1  # Tiled использует 1-based индексы
                tileset_cols = self.map_data["tilesets"][0]["columns"]
                tx = (gid % tileset_cols) * 16
                ty = (gid // tileset_cols) * 16
                
                # Отрисовка с учетом камеры
                dest_rect = pygame.Rect(
                    tile["pos"][0], tile["pos"][1], 16, 16
                )
                dest_rect = camera.apply(dest_rect)
                
                surface.blit(
                    self.tileset,
                    dest_rect,
                    pygame.Rect(tx, ty, 16, 16)
                )
    
    def _draw_tree(self, surface, camera, tree_id):
        """Отрисовка дерева по его ID"""
        tree = self.objects["trees"].get(tree_id)
        if tree and not tree["is_cut"]:
            # Находим связанные тайлы из Trees_Cuttable
            tree_rect = tree["rect"]
            layer_name = "Resources_Trees_Cuttable"
            
            if layer_name in self.layers:
                for tile in self.layers[layer_name]:
                    tile_rect = pygame.Rect(tile["pos"][0], tile["pos"][1], 16, 16)
                    if tree_rect.contains(tile_rect):
                        # Отрисовка тайла
                        gid = tile["gid"] - 1
                        tileset_cols = self.map_data["tilesets"][0]["columns"]
                        tx = (gid % tileset_cols) * 16
                        ty = (gid // tileset_cols) * 16
                        
                        dest_rect = camera.apply(tile_rect)
                        surface.blit(
                            self.tileset,
                            dest_rect,
                            pygame.Rect(tx, ty, 16, 16)
                        )
                        
    def _process_objects(self):
        """Обработка всех объектов карты"""
        self.objects = {
            "trees": {},
            "altar": None,
            "spawn": None
        }
        
        for layer in self.map_data["layers"]:
            if layer["type"] == "objectgroup":
                self._process_object_layer(layer)
            elif layer["type"] == "group":
                for sublayer in layer["layers"]:
                    if sublayer["type"] == "objectgroup":
                        self._process_object_layer(sublayer, layer["name"])