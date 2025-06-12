class Settings:
    # Базовые настройки
    TILE_SIZE = 16
    VIRTUAL_WIDTH = 18 * TILE_SIZE  # 640 (40 тайлов)
    VIRTUAL_HEIGHT = 12 * TILE_SIZE  # 320 (20 тайлов)
    
    # Окно (может быть больше виртуального экрана)
    SCREEN_WIDTH = 1280
    SCREEN_HEIGHT = 720
    FPS = 60
    
    # Игрок
    PLAYER_SPEED = 0.5
    
    # Отладка
    SHOW_FPS = True
    SHOW_POSITION = True
    SHOW_COLLISIONS = False
    
    # Цвета
    BACKGROUND = (40, 44, 52)
    DEBUG_TEXT = (220, 220, 170)
    
    SHOW_DEBUG = False  # Включает всю отладочную информацию
    SHOW_COLLISIONS = False  # Можно оставить для отдельных случаев