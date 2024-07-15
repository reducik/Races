import pygame
import sys
import random

# Инициализация Pygame
pygame.init()

# Параметры экрана
screen_width = 800  # Ширина экрана
screen_height = 600  # Высота экрана
screen = pygame.display.set_mode((screen_width, screen_height))  # Создаем окно с заданными размерами
pygame.display.set_caption("Гонки 2D")  # Устанавливаем заголовок окна

# Цвета
white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)
green = (0, 200, 0)
blue = (0, 0, 255)

# Загрузка изображений машин
player_image = pygame.image.load('car_1463810.png').convert_alpha()
enemy_image = pygame.image.load('car_16422421.png').convert_alpha()

# Масштабирование изображений до нужного размера
player_image = pygame.transform.scale(player_image, (50, 85))
enemy_image = pygame.transform.scale(enemy_image, (50, 85))

# Параметры игрока
player_pos = [screen_width // 2, screen_height - 2 * 85]

# Параметры врагов
enemy_speed = 8
enemy_spawn_rate = 5  # Частота появления врагов (в кадрах)
enemies = []

clock = pygame.time.Clock()  # Создаем объект для контроля времени

# Функция для рисования кнопок
def draw_button(screen, color, x, y, width, height, text, text_color):
    pygame.draw.ellipse(screen, color, (x, y, width, height))  # Рисуем окружность (эллипс)

    font = pygame.font.Font(None, 36)  # Устанавливаем шрифт и размер текста
    text_surf = font.render(text, True, text_color)  # Создаем поверхность с текстом
    text_rect = text_surf.get_rect(center=(x + width / 2, y + height / 2))  # Получаем прямоугольник текста
    screen.blit(text_surf, text_rect)  # Отображаем текст на экране

# Функция для проверки клика по кнопке
def button_clicked(mouse_pos, button_pos, button_radius):
    if (mouse_pos[0] - button_pos[0])**2 + (mouse_pos[1] - button_pos[1])**2 <= button_radius**2:
        return True
    return False

# Отображение стартового меню
def start_menu():
    while True:
        screen.fill(white)  # Заполняем экран белым цветом

        # Рисуем кнопку "Start"
        draw_button(screen, green, 300, 200, 200, 100, "Start", white)

        # Рисуем кнопку "Exit"
        draw_button(screen, red, 300, 350, 200, 100, "Exit", white)

        pygame.display.update()  # Обновляем экран

        for event in pygame.event.get():  # Обрабатываем события
            if event.type == pygame.QUIT:  # Если пользователь закрыл окно
                pygame.quit()  # Завершаем Pygame
                sys.exit()  # Завершаем выполнение программы
            elif event.type == pygame.MOUSEBUTTONDOWN:  # Если было нажатие кнопки мыши
                mouse_pos = pygame.mouse.get_pos()  # Получаем позицию мыши
                if button_clicked(mouse_pos, (300 + 100, 200 + 50), 50):  # Проверяем клик по кнопке "Start"
                    return True
                elif button_clicked(mouse_pos, (300 + 100, 350 + 50), 50):  # Проверяем клик по кнопке "Exit"
                    pygame.quit()
                    sys.exit()

# Функция для создания нового врага
def create_enemy():
    x_pos = random.randint(0, screen_width - enemy_image.get_width())
    y_pos = -enemy_image.get_height()
    return [x_pos, y_pos]

# Запуск стартового меню
if start_menu():
    game_over = False  # Стартуем игру
else:
    pygame.quit()
    sys.exit()

# Игровой цикл
frame_count = 0
while not game_over:
    for event in pygame.event.get():  # Обрабатываем события
        if event.type == pygame.QUIT:  # Если пользователь закрыл окно
            pygame.quit()  # Завершаем Pygame
            sys.exit()  # Завершаем выполнение программы

    keys = pygame.key.get_pressed()  # Получаем состояние всех клавиш

    if keys[pygame.K_LEFT]:  # Если нажата клавиша влево
        player_pos[0] -= 5  # Двигаем игрока влево
    if keys[pygame.K_RIGHT]:  # Если нажата клавиша вправо
        player_pos[0] += 5  # Двигаем игрока вправо
    if keys[pygame.K_UP]:  # Если нажата клавиша вверх
        player_pos[1] -= 5  # Двигаем игрока вверх
    if keys[pygame.K_DOWN]:  # Если нажата клавиша вниз
        player_pos[1] += 5  # Двигаем игрока вниз

    # Ограничиваем движение игрока пределами экрана
    if player_pos[0] < 0:
        player_pos[0] = 0
    if player_pos[0] > screen_width - player_image.get_width():
        player_pos[0] = screen_width - player_image.get_width()
    if player_pos[1] < 0:
        player_pos[1] = 0
    if player_pos[1] > screen_height - player_image.get_height():
        player_pos[1] = screen_height - player_image.get_height()

    screen.fill(white)  # Заполняем экран белым цветом

    # Генерация новых врагов
    frame_count += 1
    if frame_count % enemy_spawn_rate == 0:
        enemies.append(create_enemy())

    # Обновление позиции врагов
    for enemy in enemies:
        enemy[1] += enemy_speed
        # Удаление врагов, вышедших за пределы экрана
        if enemy[1] > screen_height:
            enemies.remove(enemy)

    # Отображение спрайтов машин
    screen.blit(player_image, player_pos)
    for enemy in enemies:
        screen.blit(enemy_image, enemy)

    # Проверка столкновения
    for enemy in enemies:
        if player_pos[1] < enemy[1] + enemy_image.get_height() and player_pos[1] + player_image.get_height() > enemy[1]:
            if player_pos[0] < enemy[0] + enemy_image.get_width() and player_pos[0] + player_image.get_width() > enemy[0]:
                game_over = True  # Если есть столкновение, завершаем игру

    pygame.display.update()  # Обновляем экран
    clock.tick(30)  # Устанавливаем количество кадров в секунду

# Отображение экрана Game Over
screen.fill(white)
font = pygame.font.Font(None, 74)
text = font.render("Game Over", True, red)
text_rect = text.get_rect(center=(screen_width / 2, screen_height / 2))
screen.blit(text, text_rect)
pygame.display.update()
pygame.time.wait(2000)  # Ждем 2 секунды

pygame.quit()
sys.exit()
