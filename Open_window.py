import sys
import subprocess
import os
import pygame


def open_game():

    # Инициализация Pygame
    pygame.init()

    # Размеры окна
    window_width = 1920
    window_height = 1010

    # Создание главного окна
    window = pygame.display.set_mode((window_width, window_height))
    # Загрузка и установка иконки
    icon = pygame.image.load('sprits/icon.jpg')  # Указываете здесь путь к файлу с иконкой
    pygame.display.set_icon(icon)

    pygame.mixer.music.load("music/dobroe-skazochnoe-nachalo-teatralnogo-predstavleniya-864.mp3")
    pygame.mixer.music.play(-1)

    # Загрузка фоновых изображений
    bg_image = pygame.image.load('sprits/мир на фон.jpg').convert()
    button1_image = pygame.image.load('sprits/кнопка 1.png').convert_alpha()
    button3_image = pygame.image.load('sprits/кнопка 3.png').convert_alpha()

    # Изменение размера изображений кнопок
    button1_image = pygame.transform.scale(button1_image, (300, 87))
    button3_image = pygame.transform.scale(button3_image, (300, 87))
    pygame.display.set_caption('Raising the level alone')

    # Функция для обработки нажатий кнопок
    def handle_button_click(button_num):
        if button_num == 1:
            play1()
        elif button_num == 3:
            statistics()

    # Функция для реализации действий при нажатии на кнопку "play"
    def play1():
        from main_window import play
        global running
        play()
        running = False  # Убрали вызов pygame.quit() отсюда

    # Функция для реализации действий при нажатии на кнопку "statistics"
    def statistics():
        # Путь к текстовому файлу со статистикой
        stats_file_path = 'game_results.txt'

        # Проверяем существует ли файл
        if not os.path.exists(stats_file_path):
            # Если файл не существует, создаем пустой файл
            with open(stats_file_path, 'w') as file:
                pass

        # Определяем путь к текстовому редактору (зависит от операционной системы)
        # В данном примере используем стандартный редактор для Windows - notepad
        text_editor_path = 'notepad.exe'

        # Запускаем текстовый редактор с файлом статистики
        try:
            subprocess.run([text_editor_path, stats_file_path])
        except Exception as e:
            print(f"Ошибка при открытии файла статистики: {e}")

    running = True
    # Рисование фонового изображения
    window.blit(bg_image, (0, 0))
    # Рисование кнопок
    button1_rect = window.blit(button1_image, (
        window_width // 2 - button1_image.get_width() // 2,
        window_height // 2 - button1_image.get_height() // 2))
    button3_rect = window.blit(button3_image, (
        window_width // 2 - button3_image.get_width() // 2,
        window_height // 2 - button3_image.get_height() // 2 + button3_image.get_height() + 50))
    # Основной цикл игры
    # Обновление окна
    pygame.display.update()
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if button1_rect.collidepoint(event.pos):
                    handle_button_click(1)
                elif button3_rect.collidepoint(event.pos):
                    handle_button_click(3)

    pygame.quit()
    sys.exit()


if __name__ == '__main__':
    open_game()
