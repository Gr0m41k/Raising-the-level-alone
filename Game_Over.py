import moviepy.editor
import pygame


def game_end():
    # Инициализация Pygame
    pygame.init()

    pygame.mixer.music.load("music/dobroe-skazochnoe-nachalo-teatralnogo-predstavleniya-864.mp3")
    pygame.mixer.music.play(-1)

    # Загрузка шрифта
    font_path = 'Font/Minecraft Rus NEW.otf'
    font_size = 50
    font = pygame.font.Font(font_path, font_size)

    # Размеры окна
    width, height = 1920, 1010

    # Создание окна
    screen = pygame.display.set_mode((width, height))

    icon = pygame.image.load('sprits/icon.jpg')  # Указываете здесь путь к файлу с иконкой
    pygame.display.set_icon(icon)

    # Загрузка анимации и масштабирование под размер окна
    animation = moviepy.editor.VideoFileClip('sprits/145dd02dbaa43b6ad940451584b07b02 (1).gif')

    # Проигрываем анимацию циклично
    animation = animation.loop(1)

    # Преобразуем каждый кадр анимации в изображение Pygame
    frames = []
    for frame in animation.iter_frames():
        img = pygame.image.frombuffer(frame, animation.size, 'RGB')
        frames.append(img)

    # Создание кнопки "Main Menu"
    button_width = 300
    button_height = 50
    button_main_menu = pygame.Rect(width // 2 - button_width // 2, height // 2 + 200, button_width, button_height)
    text_main_menu = font.render('Main Menu', True, (255, 255, 255))

    # Воспроизводим анимацию
    frame_index = 0
    clock = pygame.time.Clock()

    def main_menu_function():
        global running
        from Open_window import open_game
        # Здесь должен быть код или вызов функции, которая выполняет необходимое действие для "Main Menu"
        # print("Переход в главное меню")
        open_game()

    running = True
    while running:
        screen.fill((0, 0, 0))

        # Отображаем текущий кадр анимации
        screen.blit(frames[frame_index], (0, 0))

        # Переключаемся на следующий кадр
        frame_index += 1
        if frame_index >= len(frames):
            frame_index = 0

        # Рисуем кнопку "Main Menu"
        pygame.draw.rect(screen, (128, 128, 128), button_main_menu)  # серый цвет
        screen.blit(text_main_menu,
                    (button_main_menu.x + (button_width - text_main_menu.get_width()) // 2, button_main_menu.y))

        # Обработка событий
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                from Open_window import open_game
                open_game()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Левая кнопка мыши
                    mouse_pos = event.pos
                    if button_main_menu.collidepoint(mouse_pos):
                        # Вызываем функцию для кнопки "Main Menu"
                        main_menu_function()

        pygame.display.update()
        clock.tick(10)

    pygame.quit()

# game_end()
