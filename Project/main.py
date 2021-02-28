# Импортируем необходимые библиотеки
import pygame
import random
from copy import deepcopy
import os
import sys


# Функция для проекри нахождения фигуры в пределах поля
def check_coord():
    if figure[i].x < 0:
        return False
    elif figure[i].x > (w - 1):
        return False
    elif figure[i].y > (h - 1):
        return False
    elif field[figure[i].y][figure[i].x]:
        return False
    else:
        return True


# Функция для генерации цвета
def get_color():
    r = random.randint(100, 200)
    g = random.randint(100, 200)
    b = random.randint(100, 200)
    return (r, g, b)


# Функция для загрузки изображений
def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    if colorkey is not None:
        image = image.convert()
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
            image.set_colorkey(colorkey)
        else:
            image = image.convert_alpha()
            pass
    return image


# Функция для загрузки шрифтов
def load_font(name):
    fullname = os.path.join('font', name)
    if not os.path.isfile(fullname):
        print(f"Файл со шрифтом '{fullname}' не найден")
        sys.exit()
    return fullname


# Функция для загрузки рекорда
def load_record(name):
    fullname = os.path.join(name)
    if not os.path.isfile(fullname):
        print(f"Файл с рекодами не существует")
        print('Файл для рекордов создан, теперь ваш рекорд будет сохраняться')
        f = open(fullname, mode='w', encoding="utf-8")
        f.close()
    f = open(fullname, mode='r', encoding="utf-8")
    string_lines = [i.strip() for i in f.readlines()]
    return string_lines


# Функция  сохранения
def save_record(name, record):
    fullname = os.path.join(name)
    if not os.path.isfile(fullname):
        print(f"Файл с рекодами не существует")
        print('Файл для рекордов создан, теперь ваш рекорд будет сохраняться')
    f = open(fullname, mode='w', encoding="utf-8")
    f.write(str(record))
    f.close()


# Функция для заставки игры
def start_screen():
    screen.fill((0, 0, 0))
    surface.fill((0, 0, 0))
    intro_text = ["Тетрис классический",
                  "Правила игры: ",
                  "состовляй из падающих фигур",
                  "горизонтальные линии,",
                  "всё просто",
                  "ВПЕРЁД МОЙ ДРУГ!!!",
                  "Для продолжения,",
                  "нажми на любую кнопку"]

    fon = load_image('fon.jpg')
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 50)
    text_coord = 100
    for line in intro_text:
        string_rendered = font.render(line, 1, pygame.Color('white'))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 10
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)

    while True:
        flag = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                flag = True
        if flag:
            break
        pygame.display.flip()
        clock.tick(fps)


# Функция для перезапуска игр
def restart_screen(record=False):
    screen.fill((0, 0, 0))
    surface.fill((0, 0, 0))
    intro_text = ["Game over",
                  "К сожалению, вы проиграли",
                  "Не отчаивайтесь",
                  "Попробуйте снова",
                  "У тебя всё получится",
                  "ВПЕРЁД МОЙ ДРУГ!!!",
                  "Для продолжения,",
                  "нажми на любую кнопку"]
    if (record):
        intro_text.append('')
        intro_text.append('Ваш рекорд записан и сохранён')

    fon = load_image('fon.jpg')
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 50)
    text_coord = 100
    for line in intro_text:
        string_rendered = font.render(line, 1, pygame.Color('white'))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 10
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)

    while True:
        flag = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                flag = True
        if flag:
            break
        pygame.display.flip()
        clock.tick(fps)


# Задаём размеры окна и поля
w, h = 10, 20
size = 45
res = 750, 950
game_res = w * size, h * size

# Инициализируем окна и обявляем частоту смены кадров в игре
pygame.init()
screen = pygame.display.set_mode(res)
surface = pygame.Surface(game_res)
pygame.display.set_caption(f"Игра «Тетрис классический»")
fps = 60
clock = pygame.time.Clock()
screen.fill((0, 0, 0))
surface.fill((0, 0, 0))

# Преобразовывам поле в клеточное поле
grid = [pygame.Rect(x * size, y * size, size, size) for x in range(w) for y in range(h)]

# Задаём фигуры их координатами
figures_position = [[(-1, 0), (-2, 0), (0, 0), (1, 0)],
                    [(0, -1), (-1, -1), (-1, 0), (0, 0)],
                    [(-1, 0), (-1, 1), (0, 0), (0, -1)],
                    [(0, 0), (-1, 0), (0, 1), (-1, -1)],
                    [(0, 0), (0, -1), (0, 1), (-1, -1)],
                    [(0, 0), (0, -1), (0, 1), (1, -1)],
                    [(0, 0), (0, -1), (0, 1), (-1, 0)]]

# Создаём список который оторажает поле
field = [[0 for h in range(w)] for i in range(h)]

# Представляем фигуры как экземпляры класса
figures = [[pygame.Rect(x + w // 2, y + 1, 1, 1) for x, y in figures_pos] for figures_pos in figures_position]
figure_rect = pygame.Rect(0, 0, size - 2, size - 2)

# Задаём или генерируем необхожимые значения для начала игры
figure, next_figure = deepcopy(random.choice(figures)), deepcopy(random.choice(figures))
color, next_color = get_color(), get_color()
step_count, step_speed, step_limit = 0, 60, 2000
score, lines = 0, 0
scores = {0: 0,
          1: 50,
          2: 200,
          3: 500,
          4: 1000,
          5: 2000,
          6: 3500,
          7: 6000}
game_over = False
running = True

# Загрузка фоновой картинки игры
fon = load_image('fon.jpg')

# Загрузка необходимых шрифтов
font1 = pygame.font.Font(load_font('arial.ttf'), 75)
font2 = pygame.font.Font(load_font('arial.ttf'), 45)
font3 = pygame.font.Font(load_font('arial.ttf'), 100)

# Создание надписей с необходимой информацией
title_tetris = font1.render('TETRIS', True, pygame.Color('red'))
title_score = font2.render('Очки', True, pygame.Color('green'))
title_record = font2.render('Рекорд', True, pygame.Color('blue'))
title_next = font2.render('Следующая', True, pygame.Color('white'))
title_figure = font2.render('фигура', True, pygame.Color('white'))
title_down = font3.render('↓', True, pygame.Color('white'))

# Запускаем заставку
start_screen()

# Запускаем основной цикл игры
while not game_over:
    # Читаем из файла предыдуший рекод
    record_save = False
    record = load_record('record.txt')
    if len(record) == 0:
        record = 0
    else:
        if str(record[0]).isdigit():
            record = int(record[0])
        else:
            print('Предшествующий рекор не распознан')
            record = 0
    # Запускаем саму игру
    while running:
        # Отрисовка необхожимых полей
        screen.fill((0, 0, 0))
        screen.blit(fon, (0, 0))
        screen.blit(surface, (20, 20))
        surface.fill((0, 0, 0))

        # Установка значений по умолчанию
        dx = 0
        rotate = False
        flag_down = False
        for i in range(lines):
            pygame.time.wait(200)

        # Обработка нажатий
        for event in pygame.event.get():
            keys = pygame.key.get_pressed()
            if event.type == pygame.QUIT:
                running = False
                game_over = True
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    dx -= 1
                if event.key == pygame.K_RIGHT:
                    dx += 1
                if event.key == pygame.K_UP:
                    rotate = True
            if not keys[pygame.K_DOWN]:
                step_limit = 2000
            else:
                step_limit = 100

        for i in grid:  # Отрисовка клеточного поля
            pygame.draw.rect(surface, (50, 50, 50), i, 1)

        # Делаем копию фигуры, что бы в случаи неудачного поворота, могли востановить ей
        figure_old = deepcopy(figure)

        # Перемешение фигуры по координате X
        for i in range(4):
            figure[i].x += dx
            if not check_coord():
                figure = deepcopy(figure_old)
                break

        # Перемешение фигуры по координате Y
        step_count += step_speed
        if step_count > step_limit:
            step_count = 0
            figure_old = deepcopy(figure)
            for i in range(4):
                figure[i].y += 1
                if not check_coord():
                    for i in range(4):
                        field[figure_old[i].y][figure_old[i].x] = color
                    color, next_color = next_color, get_color()
                    figure, next_figure = next_figure, deepcopy(random.choice(figures))
                    anim_limit = 2000
                    break

        # Поворот фигруы
        center_figure = figure[0]
        figure_old = deepcopy(figure)
        if rotate:
            for i in range(4):
                x = figure[i].y - center_figure.y
                y = figure[i].x - center_figure.x
                figure[i].x = center_figure.x - x
                figure[i].y = center_figure.y + y
                if not check_coord():
                    figure = deepcopy(figure_old)
                    break

        # Проверка на сложенную линию
        line, lines = h - 1, 0
        for row in range(h - 1, -1, -1):
            count = 0
            for i in range(w):
                if field[row][i]:
                    count += 1
                field[line][i] = field[row][i]
            if count < w:
                line -= 1
            else:
                step_speed += 3
                lines += 1

        score += scores[lines]

        # Отрисовка фигуры которая падает
        for i in range(4):
            figure_rect.x = figure[i].x * size
            figure_rect.y = figure[i].y * size
            pygame.draw.rect(surface, color, figure_rect)

        # Отрисовка всего клеточного поля
        for y, raw in enumerate(field):
            for x, col in enumerate(raw):
                if col:
                    figure_rect.x, figure_rect.y = x * size, y * size
                    pygame.draw.rect(surface, col, figure_rect)

        # Отрисовка фигуры которая будет следующая
        for i in range(4):
            figure_rect.x = next_figure[i].x * size + 380
            figure_rect.y = next_figure[i].y * size + 350
            pygame.draw.rect(screen, next_color, figure_rect)

        # Отрисовка необхожимых надписей
        screen.blit(title_tetris, (480, 0))

        screen.blit(title_score, (470, 840))
        screen.blit(font2.render(str(score), True, pygame.Color('green')), (500, 900))

        screen.blit(title_record, (600, 840))
        screen.blit(font2.render(str(record), True, pygame.Color('blue')), (620, 900))

        screen.blit(title_next, (480, 100))
        screen.blit(title_figure, (520, 150))
        screen.blit(title_down, (580, 200))

        # Проверка на конец игры
        for i in range(w):
            if field[0][i]:
                running = False
                print('Game over')
                field = [[0 for i2 in range(w)] for i1 in range(h)]
                step_count, step_speed, step_limit = 0, 60, 2000
                if score > record:
                    record_save = True
                    save_record('record.txt', score)
                score = 0
                for i1 in grid:
                    pygame.draw.rect(surface, get_color(), i1)
                    screen.blit(surface, (20, 20))
                    pygame.display.flip()
                    clock.tick(200)
        clock.tick(fps)
        pygame.display.flip()
    # Рестарт игры
    if record_save:
        restart_screen(record=True)
    else:
        restart_screen()
    running = True

# В случаи закрытия окна завершаем программу
pygame.quit()
sys.exit()
