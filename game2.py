import pygame
import random
import sys

# Инициализация Pygame
pygame.init()

# Размеры окна
SCREEN_WIDTH, SCREEN_HEIGHT = 300, 600
GRID_SIZE = 30
COLUMNS, ROWS = SCREEN_WIDTH // GRID_SIZE, SCREEN_HEIGHT // GRID_SIZE

# Цвета
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (128, 128, 128)
COLORS = [
    (0, 255, 255),  # Циан
    (255, 165, 0),  # Оранжевый
    (0, 0, 255),    # Синий
    (255, 0, 255),  # Фиолетовый
    (255, 255, 0),  # Желтый
    (0, 255, 0),    # Зеленый
    (255, 0, 0)     # Красный
]

# Определение фигур тетриса (координаты ячеек)
SHAPES = [
    [[1, 5, 9, 13]],  # I
    [[1, 2, 5, 6]],   # O
    [[1, 4, 5, 6]],   # T
    [[0, 4, 5, 6]],   # J
    [[2, 4, 5, 6]],   # L
    [[0, 1, 5, 6]],   # S
    [[1, 2, 4, 5]]    # Z
]

# Инициализация экрана
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Тетрис")

# Игровая сетка
grid = [[0] * COLUMNS for _ in range(ROWS)]

# Определение фигуры
class Figure:
    def __init__(self):
        self.type = random.randint(0, len(SHAPES) - 1)
        self.color = COLORS[self.type]
        self.rotation = 0
        self.x = COLUMNS // 2 - 2
        self.y = 0

    def shape(self):
        return SHAPES[self.type][self.rotation]

    def rotate(self):
        self.rotation = (self.rotation + 1) % len(SHAPES[self.type])

# Проверка столкновения фигуры с границами и другими блоками
def check_collision(figure, dx, dy):
    for i in figure.shape():
        x = figure.x + (i % 4) + dx
        y = figure.y + (i // 4) + dy
        if x < 0 or x >= COLUMNS or y >= ROWS or (y >= 0 and grid[y][x]):
            return True
    return False

# Фиксация фигуры на сетке
def fix_figure(figure):
    for i in figure.shape():
        x = figure.x + (i % 4)
        y = figure.y + (i // 4)
        if y >= 0:
            grid[y][x] = figure.color

# Удаление заполненных строк
def clear_rows():
    global grid
    cleared_rows = 0
    new_grid = [row for row in grid if any(cell == 0 for cell in row)]
    cleared_rows = ROWS - len(new_grid)
    new_grid = [[0] * COLUMNS for _ in range(cleared_rows)] + new_grid
    grid = new_grid
    return cleared_rows

# Рендеринг сетки и фигур
def draw_grid():
    screen.fill(BLACK)
    for y in range(ROWS):
        for x in range(COLUMNS):
            if grid[y][x]:
                pygame.draw.rect(screen, grid[y][x], pygame.Rect(x * GRID_SIZE, y * GRID_SIZE, GRID_SIZE, GRID_SIZE))
    for x in range(COLUMNS + 1):
        pygame.draw.line(screen, GRAY, (x * GRID_SIZE, 0), (x * GRID_SIZE, SCREEN_HEIGHT))
    for y in range(ROWS + 1):
        pygame.draw.line(screen, GRAY, (0, y * GRID_SIZE), (SCREEN_WIDTH, y * GRID_SIZE))

# Рендеринг текущей фигуры
def draw_figure(figure):
    for i in figure.shape():
        x = figure.x + (i % 4)
        y = figure.y + (i // 4)
        if y >= 0:
            pygame.draw.rect(screen, figure.color, pygame.Rect(x * GRID_SIZE, y * GRID_SIZE, GRID_SIZE, GRID_SIZE))

# Основной игровой цикл
clock = pygame.time.Clock()
current_figure = Figure()
next_figure = Figure()
fall_time = 0
speed = 500
score = 0

running = True
while running:
    screen.fill(BLACK)
    fall_time += clock.get_rawtime()
    clock.tick()

    # Падение фигуры
    if fall_time > speed:
        fall_time = 0
        if not check_collision(current_figure, 0, 1):
            current_figure.y += 1
        else:
            fix_figure(current_figure)
            score += clear_rows()
            current_figure = next_figure
            next_figure = Figure()
            if check_collision(current_figure, 0, 0):
                running = False

    # Обработка событий
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT and not check_collision(current_figure, -1, 0):
                current_figure.x -= 1
            if event.key == pygame.K_RIGHT and not check_collision(current_figure, 1, 0):
                current_figure.x += 1
            if event.key == pygame.K_DOWN and not check_collision(current_figure, 0, 1):
                current_figure.y += 1
            if event.key == pygame.K_UP:
                current_figure.rotate()
                if check_collision(current_figure, 0, 0):
                    current_figure.rotate()

    # Рендеринг
    draw_grid()
    draw_figure(current_figure)
    pygame.display.flip()

pygame.quit()
print(f"Игра окончена! Ваш счет: {score}")
