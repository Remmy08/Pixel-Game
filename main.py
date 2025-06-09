import pygame
import sys

# Инициализация Pygame
pygame.init()

# Настройки экрана
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Моя Пиксельная Игра")

# Цвета
BACKGROUND = (20, 30, 50)

# Главный цикл игры
clock = pygame.time.Clock()
running = True

while running:
    # Обработка событий
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    # Отрисовка
    screen.fill(BACKGROUND)
    
    # Здесь будет ваша игровая логика
    
    # Обновление экрана
    pygame.display.flip()
    clock.tick(60)

# Выход
pygame.quit()
sys.exit()