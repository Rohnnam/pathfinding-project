import pygame
import numpy as np
import heapq
import random
import time

# Constants
ROWS, COLS = 40, 50
CELL_SIZE = 20
WIDTH, HEIGHT = COLS * CELL_SIZE, ROWS * CELL_SIZE
ANIMATION_DELAY = 0.01  # 10 milliseconds delay
FONT_SIZE = 30  # Font size for displaying metrics

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

def astar(grid, start, goal):
    def heuristic(a, b):
        return abs(a[0] - b[0]) + abs(a[1] - b[1])

    neighbors = [(0, 1), (0, -1), (1, 0), (-1, 0)]
    close_set = set()
    came_from = {}
    gscore = {start: 0}
    fscore = {start: heuristic(start, goal)}
    oheap = []
    nodes_processed = 0

    heapq.heappush(oheap, (fscore[start], start))

    while oheap:
        current = heapq.heappop(oheap)[1]
        nodes_processed += 1

        if current == goal:
            data = []
            while current in came_from:
                data.append(current)
                current = came_from[current]
            return data, nodes_processed

        close_set.add(current)
        for i, j in neighbors:
            neighbor = current[0] + i, current[1] + j
            tentative_g_score = gscore[current] + heuristic(current, neighbor)
            if 0 <= neighbor[0] < grid.shape[0]:
                if 0 <= neighbor[1] < grid.shape[1]:
                    if grid[neighbor[0]][neighbor[1]] == 1:
                        continue
                else:
                    continue
            else:
                continue

            if neighbor in close_set and tentative_g_score >= gscore.get(neighbor, 0):
                continue

            if tentative_g_score < gscore.get(neighbor, 0) or neighbor not in [i[1] for i in oheap]:
                came_from[neighbor] = current
                gscore[neighbor] = tentative_g_score
                fscore[neighbor] = tentative_g_score + heuristic(neighbor, goal)
                heapq.heappush(oheap, (fscore[neighbor], neighbor))

    return False, nodes_processed

def catmull_rom_spline(p0, p1, p2, p3, num_points=10):
    def interpolate(t, p0, p1, p2, p3):
        return (0.5 * ((2 * p1) +
                        (-p0 + p2) * t +
                        (2*p0 - 5*p1 + 4*p2 - p3) * t**2 +
                        (-p0 + 3*p1 - 3*p2 + p3) * t**3))

    points = []
    for i in range(num_points):
        t = i / (num_points - 1)
        x = interpolate(t, p0[0], p1[0], p2[0], p3[0])
        y = interpolate(t, p0[1], p1[1], p2[1], p3[1])
        points.append((int(x), int(y)))
    return points

def smooth_path(path):
    smoothed_path = []
    if len(path) < 4:
        return path
    for i in range(1, len(path) - 2):
        smoothed_path.extend(catmull_rom_spline(path[i - 1], path[i], path[i + 1], path[i + 2]))
    smoothed_path.append(path[-1])
    return smoothed_path

def draw_grid(win, grid, start, goal):
    for row in range(ROWS):
        for col in range(COLS):
            color = WHITE if grid[row][col] == 0 else BLACK
            if (row, col) == start:
                color = RED
            elif (row, col) == goal:
                color = GREEN
            pygame.draw.rect(win, color, (col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE))
            pygame.draw.rect(win, BLACK, (col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE), 1)

def draw_path(win, path, goal, animate=False):
    if animate:
        for (row, col) in path:
            if (row, col) != goal:
                pygame.draw.rect(win, BLUE, (col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE))
                pygame.draw.rect(win, BLACK, (col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE), 1)
                pygame.display.flip()
                time.sleep(ANIMATION_DELAY)
    else:
        for (row, col) in path:
            if (row, col) != goal:
                pygame.draw.rect(win, BLUE, (col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE))
                pygame.draw.rect(win, BLACK, (col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE), 1)

def draw_metrics(win, nodes_processed, path_length):
    font = pygame.font.SysFont(None, FONT_SIZE)
    metrics_text = f"Nodes Processed: {nodes_processed} | Path Length: {path_length}"
    text_surface = font.render(metrics_text, True, BLUE)
    win.blit(text_surface, (10, HEIGHT + 10))  # Position below the canvas

def main():
    pygame.init()
    win = pygame.display.set_mode((WIDTH, HEIGHT + FONT_SIZE + 20))  # Increase height for metrics
    pygame.display.set_caption("A* Pathfinding")

    grid = np.zeros((ROWS, COLS))
    
    # Set start point to center of the grid
    start = (ROWS // 2, COLS // 2)
    grid[start[0]][start[1]] = 0
    
    goal = None
    path = []
    smoothed_path = []
    nodes_processed = 0

    # Generate initial random obstacles
    for _ in range((ROWS * COLS) // 4):
        row = random.randint(0, ROWS - 1)
        col = random.randint(0, COLS - 1)
        if (row, col) != start:
            grid[row][col] = 1

    running = True
    animating = False
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                col, row = x // CELL_SIZE, y // CELL_SIZE
                if grid[row][col] == 0:
                    goal = (row, col)
                    path, nodes_processed = astar(grid, start, goal) if goal else ([], 0)
                    smoothed_path = smooth_path(path) if path else []
                    animating = True  # Start animation

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:  # Reset grid on 'R' key press
                    grid = np.zeros((ROWS, COLS))
                    for _ in range((ROWS * COLS) // 4):
                        row = random.randint(0, ROWS - 1)
                        col = random.randint(0, COLS - 1)
                        if (row, col) != start:
                            grid[row][col] = 1
                    path = []
                    smoothed_path = []
                    nodes_processed = 0
                    goal = None  # Clear previous goal point
                    animating = False  # Stop animation

        win.fill(WHITE)
        draw_grid(win, grid, start, goal)

        if goal:
            if animating:
                if smoothed_path:
                    draw_path(win, smoothed_path, goal, animate=True)
                    animating = False  # Stop animation once finished
            else:
                if smoothed_path:
                    draw_path(win, smoothed_path, goal, animate=False)
        
        # Draw metrics
        path_length = len(smoothed_path) if smoothed_path else 0
        draw_metrics(win, nodes_processed, path_length)

        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    main()
