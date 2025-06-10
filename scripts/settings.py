class Settings:
    # Окно
    SCREEN_WIDTH = 1024
    SCREEN_HEIGHT = 768
    FPS = 60
    
    # Тайлы
    TILE_SIZE = 16  # 16x16 пикселей
    
    # Игрок
    PLAYER_SPEED = 3
    
    # Отладка
    SHOW_FPS = True
    SHOW_POSITION = True
    SHOW_COLLISIONS = False  # Для визуализации коллизий
    
    # Цвета
    BACKGROUND = (40, 44, 52)
    PLAYER_COLOR = (86, 156, 214)
    DEBUG_TEXT = (220, 220, 170)
    COLLISION_COLOR = (255, 0, 0, 100)  # Полупрозрачный красный