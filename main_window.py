running = True
fl_gm = False
import math
import random
import time

import numpy as np
import pygame


def play():
    global num_enemies
    global current_level
    global current_level
    global running
    global mob_kill_count
    num_enemies = 5  # Начальное количество врагов
    current_level = 1  # Текущий уровень игры
    count_lvl_max = 10  # макс лвл игры
    mob_kill_count = 0
    running = True

    # Инициализация Pygame
    pygame.init()

    pygame.mixer.music.load("music/muzyka_ekshen_dlia_fona_bez_avtorskikh_prav_54N.mp3")
    pygame.mixer.music.play(-1)
    # Загрузка изображения сердца
    heart_image = pygame.image.load(
        "sprits/eMK0qDeBxi_05nF__bb85HzoG6tj3HoIimZ3G5q0H20ls_TVN9V5Z36IuEgVl0ZOKCEWlPbMvfPUKmW-7scgpfp5.png")
    heart_rect = heart_image.get_rect()

    # Масштабируем изображение сердца (возможно, потребуется подобрать нужные размеры)
    heart_image = pygame.transform.scale(heart_image, (heart_rect.width // 2, heart_rect.height // 2))

    # Размер окна игры
    width = 1920
    height = 1010

    # Создание окна игры
    window = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Выживание")

    # Загрузка фоновой картинки
    background_image = pygame.image.load("sprits/photo_2023-12-29_19-30-43.jpg")
    background_rect = background_image.get_rect()

    icon = pygame.image.load('sprits/icon.jpg')  # Указываете здесь путь к файлу с иконкой
    pygame.display.set_icon(icon)

    # Создание групп спрайтов
    all_sprites = pygame.sprite.Group()
    enemies = pygame.sprite.Group()
    bullets = pygame.sprite.Group()

    # Класс для главного героя
    class Player(pygame.sprite.Sprite):
        def __init__(self, bullets):
            super().__init__()

            self.change_back_time = float('inf')  # инициализация переменной
            self.size_x = 70
            self.size_y = 50
            self.last_hit_time = 0  # время последнего получения урона
            self.hit_cooldown = 1  # cooldown в секундах после получения урона
            # HP главного героя
            self.hp = 5
            self.ultimate_cooldown = 10  # cooldown ультимейт-атаки
            self.last_ultimate_time = 0  # время последнего использования ультимейт-атаки
            self.bullets = bullets
            # Переменная для проверки, был ли выстрел
            self.bullet_shot = False

            # Анимация для главного героя
            self.images = []
            for i in range(1, 5):
                image = pygame.transform.scale(pygame.image.load(f"sprits/SlimeBlue_Idle{i}.png").convert_alpha(),
                                               (self.size_x, self.size_y))
                self.images.append(image)
            self.idle_images = self.images.copy()  # Сохраняем оригинальные изображения для восстановления
            self.index = 0
            self.image = self.images[self.index]
            self.rect = self.image.get_rect()
            self.rect.center = (width // 2 + 30, height // 2 - 10)

            # Создаем отдельный хитбокс для проверки столкновений
            self.hitbox = self.rect
            self.hitbox.center = self.rect.center

            self.animation_time = pygame.time.get_ticks()
            self.animation_delay = 150  # Задержка между кадрами в миллисекундах

            # Скорости движения главного героя
            self.speed_x = 0
            self.speed_y = 0

            # Установка направления главного героя
            self.direction = "idle"
            self.damage_images = []
            for i in range(1, 5):
                image = pygame.transform.scale(
                    pygame.image.load(f"sprits/тескутра{i}.png").convert_alpha(),
                    (self.size_x, self.size_y)
                )
                self.damage_images.append(image)

        def take_damage(self):
            current_time = time.time()
            if current_time - self.last_hit_time > self.hit_cooldown:
                self.hp -= 1
                self.last_hit_time = current_time
                self.images = self.damage_images
                self.change_back_time = current_time + 0.5  # Время, через которое анимацию нужно изменить обратно
                # Убедитесь, что self.index обнуляется на начальное значение
                self.index = 0

                if self.hp <= 0:
                    global running
                    running = False

        def ultimate_attack(self):
            current_time = time.time()
            if current_time - self.last_ultimate_time >= self.ultimate_cooldown:
                # Количество пуль и шаг изменения угла
                num_bullets = 20
                angle_step = 360 / num_bullets
                for i in range(num_bullets):
                    # Определение угла в радианах
                    angle_rad = math.radians(i * angle_step)
                    target_x = self.rect.centerx + math.cos(angle_rad) * 50
                    target_y = self.rect.centery + math.sin(angle_rad) * 50
                    self.shoot(target_x, target_y)

                self.last_ultimate_time = current_time  # Обновление времени последнего использования

        # shoot
        def shoot(self, target_x, target_y):
            # Создаем экземпляр пули
            bullet = Bullet(self.rect.centerx, self.rect.centery, target_x, target_y)
            # Добавляем пулю в группу пуль
            self.bullets.add(bullet)

        def update(self):
            # Обновление координат главного героя
            self.rect.x += self.speed_x
            self.rect.y += self.speed_y

            # Обновление координат хитбокса
            self.hitbox.center = self.rect.center

            # Проверка столкновений главного героя с врагами и добавление временной неуязвимости
            current_time = time.time()
            # если прошло достаточно времени после получения урона...
            if current_time > self.change_back_time:
                self.images = self.idle_images  # возвращаем обычные изображения
                self.index = (self.index + 1) % len(self.images)  # и сбрасываем индекс на следующий кадр анимации
                self.change_back_time = float(
                    'inf')  # устанавливаем значение в бесконечность для предотвращения повторного входа

            # Если главный герой недавно был ударен, мы проверяем время для временной неуязвимости
            if current_time - self.last_hit_time > self.hit_cooldown:
                hits = pygame.sprite.spritecollide(self, enemies, False)
                if hits and self.take_damage():
                    # Используйте этот флаг для выхода из игры
                    global running
                    running = False

            animation_now = pygame.time.get_ticks()
            if animation_now - self.animation_time >= self.animation_delay:
                # Циклично проходим по индексам изображений
                self.index = (self.index + 1) % len(self.images)
                # Обновляем изображение на каждом кадре
                self.image = self.images[self.index]
                # Обновляем время последнего изменения кадра анимации
                self.animation_time = animation_now

            # Проверка нажатия клавиши для стрельбы
            keys = pygame.key.get_pressed()
            if keys[pygame.K_SPACE]:
                self.bullet_shot = True
            # Проверка нажатых клавиш
            if keys[pygame.K_a]:
                self.speed_x = -5
                self.direction = "left"
            elif keys[pygame.K_d]:
                self.speed_x = 5
                self.direction = "right"
            else:
                self.speed_x = 0
                self.direction = "idle"

            if keys[pygame.K_w]:
                self.speed_y = -5
                self.direction = "up"
            elif keys[pygame.K_s]:
                self.speed_y = 5
                self.direction = "down"
            else:
                self.speed_y = 0
                if self.speed_x == 0:
                    self.direction = "idle"

    # Класс пули
    class Bullet(pygame.sprite.Sprite):
        def __init__(self, start_x, start_y, target_x, target_y):
            super().__init__()
            self.image = pygame.image.load("sprits/shoot.png").convert_alpha()
            self.rect = self.image.get_rect()
            # Позиционируем пульку
            self.rect.center = (start_x, start_y)
            # Рассчитываем вектор движения пули
            dist_x = target_x - start_x
            dist_y = target_y - start_y
            dist = (dist_x ** 2 + dist_y ** 2) ** 0.5
            # Скорость движения пули
            self.speed_x = (dist_x / dist) * 10
            self.speed_y = (dist_y / dist) * 10
            # Счетчик отражений от стенок
            self.bounce_count = 0

        def update(self):
            # Обновляем положение пули
            self.rect.x += self.speed_x
            self.rect.y += self.speed_y

            # Отражение от левой и правой стенок
            if self.rect.right >= width or self.rect.left <= 0:
                self.speed_x *= -1
                self.bounce_count += 1
            # Отражение от верхней и нижней стенок
            if self.rect.bottom >= height or self.rect.top <= 0:
                self.speed_y *= -1
                self.bounce_count += 1

            # Удаляем пулю если превысила количество отражений
            if self.bounce_count > 2:
                self.kill()

    # Класс для анимации смерти врага
    class Explosion(pygame.sprite.Sprite):
        def __init__(self, center, x, y):
            super().__init__()
            self.x = x
            self.y = y
            self.images = []
            for i in range(1, 10):
                img = pygame.image.load(f'sprits/SlimeRed_Death{i}.png').convert_alpha()
                img = pygame.transform.scale(img, (self.x, self.y))
                self.images.append(img)
            self.index = 0
            self.image = self.images[self.index]
            self.rect = self.image.get_rect(center=center)
            self.frame_rate = 50  # Скорость анимации
            self.last_update = pygame.time.get_ticks()

        def update(self):
            now = pygame.time.get_ticks()
            if now - self.last_update > self.frame_rate:
                self.last_update = now
                self.index += 1
                if self.index == len(self.images):
                    self.kill()  # Удаляем спрайт после последнего кадра
                else:
                    center = self.rect.center
                    self.image = self.images[self.index]
                    self.rect = self.image.get_rect(center=center)

    class Enemy(pygame.sprite.Sprite):
        # Теперь используем фиксированный размер для всех спрайтов
        def __init__(self):
            super().__init__()
            self.hp = 3
            self.speed = 2
            self.size_x = 120
            self.size_y = 80

            self.images = []
            for i in range(1, 5):
                image = pygame.image.load(f"sprits/SlimeRed_Idle{i}.png").convert_alpha()
                image = pygame.transform.scale(image,
                                               (self.size_x,
                                                self.size_y))  # -> Ключевое место: масштабируем только здесь
                self.images.append(image)

            self.index = 0
            self.image = self.images[self.index]
            self.rect = self.image.get_rect()
            side = random.choice(["left", "right", "top", "bottom"])

            # Установка соответствующей координаты
            if side == "left":
                self.rect.x = 0
                self.rect.y = random.randint(0, height - self.rect.height)
            elif side == "right":
                self.rect.x = width - self.rect.width
                self.rect.y = random.randint(0, height - self.rect.height)
            elif side == "top":
                self.rect.x = random.randint(0, width - self.rect.width)
                self.rect.y = 0
            else:
                self.rect.x = random.randint(0, width - self.rect.width)
                self.rect.y = height - self.rect.height

            self.animation_time = pygame.time.get_ticks()
            self.animation_delay = 200  # Задержка между кадрами в миллисекундах

        #  метод take_damage класса Enemy для создания анимации смерти
        def take_damage(self):
            global mob_kill_count  # Объявляем глобальную переменную
            self.hp -= 1
            if self.hp <= 0:
                explosion = Explosion(self.rect.center, self.size_x, self.size_y)
                all_sprites.add(explosion)
                # Вместо прямого уничтожения, вызываем функцию для разделения
                spawn_mini_enemies(self.rect.center)
                self.kill()
                mob_kill_count += 1  # Увеличиваем счетчик мобов

        def update(self):
            # Анимация движения врагов
            if pygame.time.get_ticks() - self.animation_time > self.animation_delay:
                if self.index < len(self.images) - 1:
                    self.index += 1
                else:
                    self.index = 0
                self.image = self.images[self.index]
                self.animation_time = pygame.time.get_ticks()

            # Преследование игрока
            if self.rect.x < player.rect.x:
                self.rect.x += 1

            elif self.rect.x > player.rect.x:
                self.rect.x -= 1
            if self.rect.y < player.rect.y:
                self.rect.y += 1
            elif self.rect.y > player.rect.y:
                self.rect.y -= 1

    def spawn_mini_enemies(center):
        for _ in range(3):  # Создаем трех маленьких врагов
            mini_enemy = MiniEnemy(center)
            all_sprites.add(mini_enemy)
            enemies.add(mini_enemy)

    # Создаем класс мини-врагов, наследуя его от класса врагов и переопределяем нужные нам методы и свойства
    class MiniEnemy(Enemy):
        def __init__(self, center):
            super().__init__()

            self.size_x = 70
            self.size_y = 50
            self.images = []
            for i in range(1, 5):
                image = pygame.image.load(f"sprits/SlimeRed_Idle{i}.png").convert_alpha()
                image = pygame.transform.scale(image,
                                               (self.size_x,
                                                self.size_y))  # -> Ключевое место: масштабируем только здесь
                self.images.append(image)
            self.index = 0
            self.image = self.images[self.index]
            self.rect = self.image.get_rect()
            self.rect = self.image.get_rect(center=center)
            self.hp = 1  # У мини врага всего 1 HP

        def take_damage(self):
            global mob_kill_count  # Объявляем глобальную переменную
            self.hp -= 1
            if self.hp <= 0:
                explosion = Explosion(self.rect.center, self.size_x, self.size_y)
                all_sprites.add(explosion)
                mob_kill_count += 1  # Увеличиваем счетчик мобов
                self.kill()  # Удаляем мини-врага без создания новых

        def update(self):
            # Преследование игрока
            if self.rect.x < player.rect.x:
                self.rect.x += 2

            elif self.rect.x > player.rect.x:
                self.rect.x -= 2
            if self.rect.y < player.rect.y:
                self.rect.y += 2
            elif self.rect.y > player.rect.y:
                self.rect.y -= 2

    def enemy_collisions():
        # Обнаружение столкновений между врагами
        for enemy_1 in enemies:
            for enemy_2 in enemies:
                if enemy_1 != enemy_2 and pygame.sprite.collide_rect(enemy_1, enemy_2):
                    # Изменение координат врага
                    if enemy_1.rect.x < enemy_2.rect.x:
                        enemy_1.rect.x -= 5
                        enemy_2.rect.x += 5
                    else:
                        enemy_1.rect.x += 5
                        enemy_2.rect.x -= 5

                    # Также оттолкнем их по оси Y для полного разделения
                    if enemy_1.rect.y < enemy_2.rect.y:
                        enemy_1.rect.y -= 5
                        enemy_2.rect.y += 5
                    else:
                        enemy_1.rect.y += 5
                        enemy_2.rect.y -= 5

    def update_all():
        all_sprites.update()
        enemy_collisions()

    def complex_enemy_update():
        num_enemies = len(enemies)
        angle_step = 360 / num_enemies  # Шаг угла для распределения врагов
        formation_radius = 150  # Радиус формации вокруг игрока, где враги будут расположены

        for idx, enemy in enumerate(enemies):
            target_angle = math.radians(idx * angle_step)
            target_x = player.rect.centerx + formation_radius * math.cos(target_angle)
            target_y = player.rect.centery + formation_radius * math.sin(target_angle)

            # Вычисляем вектор движения врага к целевой точке
            move_vector = np.array([target_x - enemy.rect.centerx, target_y - enemy.rect.centery])
            move_vector = move_vector / np.linalg.norm(move_vector) if np.linalg.norm(move_vector) != 0 else np.zeros(2)

            # Уклонение от пуль
            for bullet in bullets:
                # Вычисляем вектор от пули до врага
                bullet_vector = np.array(
                    [bullet.rect.centerx - enemy.rect.centerx, bullet.rect.centery - enemy.rect.centery])
                bullet_distance = np.linalg.norm(bullet_vector)

                # Если пуля находится достаточно близко, уклоняемся от нее
                if bullet_distance < 50:
                    move_vector -= bullet_vector / (bullet_distance + 1)

            # Расходятся от других врагов
            for other_enemy in enemies:
                if other_enemy != enemy:
                    enemy_vector = np.array(
                        [enemy.rect.centerx - other_enemy.rect.centerx, enemy.rect.centery - other_enemy.rect.centery])
                    enemy_distance = np.linalg.norm(enemy_vector)

                    # Если враги слишком близко друг к другу, расходятся
                    if enemy_distance < 60:
                        move_vector += enemy_vector / (enemy_distance + 1)

            # Ускорение, если враги находятся далеко
            player_distance = np.linalg.norm(np.array([target_x - player.rect.centerx, target_y - player.rect.centery]))
            if player_distance > 300:
                move_vector *= 1.5

            # Обновляем положение врага, двигаясь по вектору с заданной скоростью
            enemy.rect.centerx += int(move_vector[0] * enemy.speed)  # Скорость преследования корректируем здесь
            enemy.rect.centery += int(move_vector[1] * enemy.speed)

    # Отображение здоровья, счетчика убийств и времени игры на каждом кадре
    def draw_ui():
        global current_level
        draw_health(player.hp, 20, 20)  # Отрисовываем здоровье в левом верхнем углу
        draw_mob_kill_count(mob_kill_count, 20, 60)  # Отрисовываем счетчик убийств под сердцами
        draw_game_time(start_time, 20, 100)  # Отрисовываем время игры под счетчиком убийств
        draw_level_and_remaining_enemies(current_level, len(enemies), 20,
                                         140)  # Отрисовываем номер уровня и кол-во оставшихся врагов под временем игры

    # Функция для отображения текущего уровня и количества оставшихся врагов
    def draw_level_and_remaining_enemies(current_level, remaining_enemies, x, y):
        font = pygame.font.Font("Font/Minecraft Rus NEW.otf", 26)
        level_text = font.render(f'Уровень: {current_level}/10', True, (255, 255, 255))
        enemies_text = font.render(f'Осталось врагов: {remaining_enemies}', True, (255, 255, 255))
        window.blit(level_text, (x, y))
        window.blit(enemies_text, (x, y + 30))

    #  место отображения сердец на статичное в левом верхнем углу
    def draw_health(health, x, y):
        for i in range(health):
            window.blit(heart_image, (x + 30 * i, y))

    def draw_game_time(start_time, x, y):
        """
        Отображение прошедшего времени игры
        :param start_time: float, время начала игры
        :param x: int, позиция x текста на экране
        :param y: int, позиция y текста на экране
        """
        elapsed_time = int(time.time() - start_time)  # Вычисляем прошедшее время в секундах
        # Конвертируем время в минуты и секунды
        minutes = elapsed_time // 60
        seconds = elapsed_time % 60
        font = pygame.font.Font("Font/Minecraft Rus NEW.otf", 26)
        text = font.render(f'Время игры: {minutes:02d}:{seconds:02d}', True, (255, 255, 255))
        window.blit(text, (x, y))

    # Функция для отображения счетчика убийств мобов
    def draw_mob_kill_count(kill_count, x, y):
        font = pygame.font.Font("Font/Minecraft Rus NEW.otf", 26)
        text = font.render(f'Убито мобов: {kill_count}', True, (255, 255, 255))
        window.blit(text, (x, y))

    # Создание главного героя
    player = Player(bullets)
    all_sprites.add(player)

    # Создаем врагов для следующего уровня
    for _ in range(num_enemies):
        enemy = Enemy()
        all_sprites.add(enemy)
        enemies.add(enemy)

    # Функция для перехода к следующему уровню
    def next_level():
        global current_level, num_enemies, count_lvl_max

        current_level += 1  # Переходим к следующему уровню
        num_enemies += 2  # Увеличиваем количество врагов
        enemies.empty()  # Очищаем список врагов

        # Создаем врагов для следующего уровня
        for _ in range(num_enemies):
            enemy = Enemy()
            all_sprites.add(enemy)
            enemies.add(enemy)

    clock = pygame.time.Clock()

    # таймер
    start_time = time.time()
    while running:
        # Ограничение количества кадров в секунду
        clock.tick(70)

        # Обработка событий
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:  # Обработка события нажатия на кнопку мыши
                mouse_x, mouse_y = event.pos
                player.shoot(mouse_x, mouse_y)  # Стрельба в направлении клика мыши

        # Проверяем столкновение пуль с врагами
        for bullet in bullets:
            # Получаем врагов, которых поразила пуля
            hits = pygame.sprite.spritecollide(bullet, enemies, False)
            if hits:
                # При попадании у врага уменьшаем здоровье
                for hit in hits:
                    hit.take_damage()
                    # Убираем пулю
                    bullet.kill()
                    break  # Убиваем пулю и продолжаем - чтобы пуля не поражала более одного врага

        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            player.ultimate_attack()  # Вызов функции ультимейт-атаки

        # Обновление спрайтов
        update_all()

        # Ограничение главного героя в пределах поля
        if player.rect.left < 0:
            player.rect.left = 0
        if player.rect.right > width:
            player.rect.right = width
        if player.rect.top < 0:
            player.rect.top = 0
        if player.rect.bottom > height:
            player.rect.bottom = height

        # Отрисовка фоновой картинки
        window.blit(background_image, background_rect)

        # Проверяем, закончился ли уровень
        if len(enemies) == 0 and current_level <= count_lvl_max:
            next_level()  # Если да, начинаем следующий уровень

        complex_enemy_update()

        # Отрисовка всех спрайтов
        all_sprites.draw(window)
        bullets.update()  # Обновление пуль
        bullets.draw(window)  # Отрисовка пуль

        # Отображение UI (здоровье + счетчик)
        draw_ui()

        # Обновление экрана
        pygame.display.flip()

    # В месте завершения игры вызываем функцию сохранения результатов
    if not running:
        elapsed_time = time.time() - start_time
        save_game_results(player.hp, elapsed_time, mob_kill_count, current_level)

    # Завершение игры
    from Game_Over import game_end
    game_end()
    pygame.quit()


# Вспомогательная функция для сохранения результатов игры в файл
def save_game_results(hp, time_played, mob_kill_count, level):
    # Создаем или открываем файл для добавления записей
    with open('game_results.txt', 'a') as file:
        # Создаем форматированный текст статистики
        stats = [
            '-' * 30,  # верхняя рамка
            '| Время игры: {:02d}:{:02d} |'.format(*divmod(int(time_played), 60)),
            '| Уровень: {} |'.format(level),
            '| Здоровье: {} |'.format(hp),
            '| Убито мобов: {} |'.format(mob_kill_count),
            '-' * 30  # нижняя рамка
        ]
        # Подгоняем рамку под длину самой длинной строки
        max_length = max(len(line) for line in stats)
        top_and_bottom_border = '-' * max_length

        stats[0] = stats[-1] = top_and_bottom_border
        for i, line in enumerate(stats[1:-1], 1):
            # Выровняем текст по центру
            stats[i] = '|{:^{}}|'.format(line[1:-1].strip(), max_length - 2)

        # Записываем каждую строку в файл
        file.write('\n'.join(stats))
        file.write('\n\n')  # Добавляем пустые строки между результатами
