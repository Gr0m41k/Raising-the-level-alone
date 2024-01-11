import pygame
import random

# Инициализация Pygame
pygame.init()

# Размер окна игры
width = 1920
height = 1010


# Создание окна игры
window = pygame.display.set_mode((width, height))
pygame.display.set_caption("Raising-the-level-alone")

# Загрузка фоновой картинки
background_image = pygame.image.load("../Raising-the-level-alone/place.jpg")
background_rect = background_image.get_rect()

# Создание групп спрайтов
all_sprites = pygame.sprite.Group()
enemies = pygame.sprite.Group()

# Класс для главного героя
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.transform.scale(pygame.image.load('../Raising-the-level-alone/SlimeBlue_Jump1.png').convert_alpha(), (220, 150))
        self.rect = pygame.Rect(0, 0, 50, 50)
        self.rect.center = (width // 2 - 54, height // 2 - 110)

    def update(self):
        # Движение главного героя с помощью стрелочек
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.rect.x -= 5
        if keys[pygame.K_RIGHT]:
            self.rect.x += 5
        if keys[pygame.K_UP]:
            self.rect.y -= 5
        if keys[pygame.K_DOWN]:
            self.rect.y += 5

# Класс для врагов
class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.transform.scale(pygame.image.load('../Raising-the-level-alone/SlimeRed_Jump1.png').convert_alpha(), (220, 150))
        self.rect = pygame.Rect(0, 0, 50, 50)
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

    def update(self):
        # Преследование игрока
        if self.rect.x < player.rect.x:
            self.rect.x += 1
        elif self.rect.x > player.rect.x:
            self.rect.x -= 1
        if self.rect.y < player.rect.y:
            self.rect.y += 1
        elif self.rect.y > player.rect.y:
            self.rect.y -= 1

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

# Создание главного героя
player = Player()
all_sprites.add(player)

# Создание врагов
num_enemies = 20
for _ in range(num_enemies):
    enemy = Enemy()
    all_sprites.add(enemy)
    enemies.add(enemy)

# Главный цикл игры
running = True
clock = pygame.time.Clock()

def update_all():
    all_sprites.update()
    enemy_collisions()

while running:
    # Ограничение количества кадров в секунду
    clock.tick(60)

    # Обработка событий
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Обновление спрайтов
    update_all()

    # Ограничение главного героя в пределах поля
    if player.rect.left < 0:
        player.rect.left = 0

    if player.rect.right > 1750:
        player.rect.right = 1750
    if player.rect.top < 0:
        player.rect.top = 0
    if player.rect.bottom > 900:
        player.rect.bottom = 900


    # Ограничение врагов в пределах поля
    for enemy in enemies:
        if enemy.rect.left < 0:
            enemy.rect.left = 0
        if enemy.rect.right > width:
            enemy.rect.right = width
        if enemy.rect.top < 0:
            enemy.rect.top = 0
        if enemy.rect.bottom > height:
            enemy.rect.bottom = height

    # Отрисовка фоновой картинки
    window.blit(background_image, background_rect)

    # Проверка столкновений главного героя с врагами
    if pygame.sprite.spritecollide(player, enemies, True):
        running = False

    # Отрисовка всех спрайтов
    all_sprites.draw(window)

    # Обновление экрана
    pygame.display.flip()

# Завершение игры
pygame.quit()
