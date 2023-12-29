import pygame

# Инициализация Pygame
pygame.init()

# Указываем размеры экрана
screen_width = 1920
screen_height = 1010
screen = pygame.display.set_mode((screen_width, screen_height))

# Загрузка карты
background_image = pygame.image.load('place.jpg')

# Основной игровой цикл
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Отображение карты на экране
    screen.blit(background_image, (0, 0))

    # Обновление экрана
    pygame.display.flip()

# Завершение работы Pygame
pygame.quit()
