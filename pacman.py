# pacman_game.py

import pygame
import sys
import random
import math

# Initialize Pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 560, 620
FPS = 60

# Colors
BLACK = (0, 0, 0)
YELLOW = (255, 255, 0)
DARK_YELLOW = (155, 155, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
PINK = (255, 192, 203)
ORANGE = (255, 165, 0)
CYAN = (0, 255, 255)
RED = (255, 0, 0)

# Create the screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pacman")

clock = pygame.time.Clock()

# Fonts
pygame.font.init()
font = pygame.font.SysFont('arial', 24)
big_font = pygame.font.SysFont('arial', 36)

# Global variables
TILE_SIZE = 20
WALLS = []
DOTS = []
POWER_PELLETS = []
PORTALS = []
SCORE = 0
LIVES = 3
LEVEL = 1

# Directions as tuples
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# Corrected Level Layout
LEVEL_LAYOUT = [
    "XXXXXXXXXXXXXXXXXXXXXXXXXXXX",
    "X............XX............X",
    "X.XXXX.XXXXX.XX.XXXXX.XXXX.X",
    "X.XXXX.XXXXX.XX.XXXXX.XXXX.X",
    "X..........................X",
    "X.XXXX.XX.XXXXXXXX.XX.XXXX.X",
    "X......XX....XX....XX......X",
    "XXXXXX.XXXXX.XX.XXXXX.XXXXXX",
    "X......XXXXX.XX.XXXXX......X",
    "X......XX..........XX......X",
    "X......XX.XXXXXXXX.XX......X",
    "XXXXXX.XX.X      X.XX.XXXXXX",
    "X     .  X      X  .     X",
    "XXXXXX.XX.X      X.XX.XXXXXX",
    "X......XX.XXXXXXXX.XX......X",
    "X......XX..........XX......X",
    "X......XX.XXXXXXXX.XX......X",
    "XXXXXX.XX.XXXXXXXX.XX.XXXXXX",
    "X............XX............X",
    "X.XXXX.XXXXX.XX.XXXXX.XXXX.X",
    "X...XX................XX...X",
    "XXX.XX.XX.XXXXXXXX.XX.XX.XXX",
    "X......XX....XX....XX......X",
    "X.XXXXXXXXXX.XX.XXXXXXXXXX.X",
    "X..........................X",
    "XXXXXXXXXXXXXXXXXXXXXXXXXXXX"
]

# Game Objects
class Wall(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.rect = pygame.Rect(x, y, TILE_SIZE, TILE_SIZE)

    def draw(self):
        pygame.draw.rect(screen, BLUE, self.rect)

class Dot(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.rect = pygame.Rect(x + TILE_SIZE//2 - 2, y + TILE_SIZE//2 - 2, 4, 4)

    def draw(self):
        pygame.draw.circle(screen, WHITE, self.rect.center, 2)

class PowerPellet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.rect = pygame.Rect(x + TILE_SIZE//2 - 6, y + TILE_SIZE//2 - 6, 12, 12)

    def draw(self):
        pygame.draw.circle(screen, WHITE, self.rect.center, 6)

class Pacman(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.position = pygame.Vector2(x, y)
        self.direction = LEFT  # Now a tuple
        self.next_direction = LEFT  # Now a tuple
        self.speed = 2
        self.radius = TILE_SIZE // 2 - 2
        self.alive = True

    def update(self):
        if self.alive:
            self.move()
            self.eat()
            self.check_collision_with_ghosts()

    def move(self):
        # Handle direction change
        if self.can_move(self.next_direction):
            self.direction = self.next_direction

        # Move in current direction
        if self.can_move(self.direction):
            dir_vector = pygame.Vector2(self.direction)
            self.position += dir_vector * self.speed
        else:
            # Snap to grid
            self.position.x = round(self.position.x / TILE_SIZE) * TILE_SIZE
            self.position.y = round(self.position.y / TILE_SIZE) * TILE_SIZE

        # Screen wrapping
        if self.position.x < 0:
            self.position.x = WIDTH - TILE_SIZE
        elif self.position.x >= WIDTH:
            self.position.x = 0

    def can_move(self, direction):
        dir_vector = pygame.Vector2(direction)
        next_pos = self.position + dir_vector * self.speed
        next_rect = pygame.Rect(next_pos.x, next_pos.y, TILE_SIZE, TILE_SIZE)
        for wall in WALLS:
            if wall.rect.colliderect(next_rect):
                return False
        return True

    def eat(self):
        global SCORE
        # Check collision with dots
        pacman_rect = pygame.Rect(self.position.x, self.position.y, TILE_SIZE, TILE_SIZE)
        for dot in DOTS[:]:
            if pacman_rect.colliderect(dot.rect):
                DOTS.remove(dot)
                SCORE += 10

        # Check collision with power pellets
        for pellet in POWER_PELLETS[:]:
            if pacman_rect.colliderect(pellet.rect):
                POWER_PELLETS.remove(pellet)
                SCORE += 50
                for ghost in ghosts:
                    ghost.frightened = True
                    ghost.frightened_start = pygame.time.get_ticks()

    def check_collision_with_ghosts(self):
        pacman_rect = pygame.Rect(self.position.x, self.position.y, TILE_SIZE, TILE_SIZE)
        for ghost in ghosts:
            ghost_rect = pygame.Rect(ghost.position.x, ghost.position.y, TILE_SIZE, TILE_SIZE)
            if pacman_rect.colliderect(ghost_rect):
                if ghost.frightened:
                    ghost.reset_position()
                    global SCORE
                    SCORE += 200
                else:
                    self.die()

    def die(self):
        global LIVES
        self.alive = False
        LIVES -= 1
        if LIVES > 0:
            pygame.time.wait(1000)  # Wait a moment before resetting
            reset_level()
        else:
            game_over()

    def draw(self):
        # Draw Pacman as a circle with a mouth (using an arc)
        x = int(self.position.x + TILE_SIZE // 2)
        y = int(self.position.y + TILE_SIZE // 2)
        pygame.draw.circle(screen, YELLOW, (x, y), self.radius)
        # Mouth
        mouth_angle = {
            (1, 0): (math.pi / 4, -math.pi / 4),
            (-1, 0): (3 * math.pi / 4, 5 * math.pi / 4),
            (0, -1): (5 * math.pi / 4, 7 * math.pi / 4),
            (0, 1): (7 * math.pi / 4, 9 * math.pi / 4)
        }
        start_angle, end_angle = mouth_angle.get(self.direction, (0, 0))
        if start_angle != end_angle:
            pygame.draw.polygon(screen, BLACK, [
                (x, y),
                (x + self.radius * math.cos(start_angle), y - self.radius * math.sin(start_angle)),
                (x + self.radius * math.cos(end_angle), y - self.radius * math.sin(end_angle))
            ])

class Ghost(pygame.sprite.Sprite):
    def __init__(self, x, y, color, target_func):
        super().__init__()
        self.position = pygame.Vector2(x, y)
        self.start_position = pygame.Vector2(x, y)
        self.direction = LEFT  # Now a tuple
        self.speed = 2
        self.color = color
        self.frightened = False
        self.frightened_start = None
        self.radius = TILE_SIZE // 2 - 2
        self.target_func = target_func

    def update(self):
        self.move()
        self.check_frightened()

    def move(self):
        # Ghost AI: Move towards target
        if self.can_move(self.direction):
            dir_vector = pygame.Vector2(self.direction)
            self.position += dir_vector * self.speed
        else:
            # Choose new direction
            possible_directions = [UP, DOWN, LEFT, RIGHT]
            opposite_direction = (-self.direction[0], -self.direction[1])
            if opposite_direction in possible_directions:
                possible_directions.remove(opposite_direction)
            valid_directions = []
            for direction in possible_directions:
                if self.can_move(direction):
                    valid_directions.append(direction)
            if valid_directions:
                # Select direction closest to target
                target_pos = self.target_func()
                min_distance = None
                for direction in valid_directions:
                    dir_vector = pygame.Vector2(direction)
                    next_pos = self.position + dir_vector * TILE_SIZE
                    distance = (next_pos - target_pos).length_squared()
                    if min_distance is None or distance < min_distance:
                        min_distance = distance
                        self.direction = direction
                dir_vector = pygame.Vector2(self.direction)
                self.position += dir_vector * self.speed
            else:
                # No valid direction; reverse
                self.direction = opposite_direction

        # Screen wrapping
        if self.position.x < 0:
            self.position.x = WIDTH - TILE_SIZE
        elif self.position.x >= WIDTH:
            self.position.x = 0

    def can_move(self, direction):
        dir_vector = pygame.Vector2(direction)
        next_pos = self.position + dir_vector * self.speed
        next_rect = pygame.Rect(next_pos.x, next_pos.y, TILE_SIZE, TILE_SIZE)
        for wall in WALLS:
            if wall.rect.colliderect(next_rect):
                return False
        return True

    def check_frightened(self):
        if self.frightened and pygame.time.get_ticks() - self.frightened_start > 7000:
            self.frightened = False

    def reset_position(self):
        self.position = self.start_position.copy()
        self.direction = LEFT
        self.frightened = False

    def draw(self):
        x = int(self.position.x + TILE_SIZE // 2)
        y = int(self.position.y + TILE_SIZE // 2)
        color = BLUE if self.frightened else self.color
        # Body
        pygame.draw.circle(screen, color, (x, y - self.radius // 2), self.radius)
        pygame.draw.rect(screen, color, (x - self.radius, y - self.radius // 2, self.radius * 2, self.radius))
        # Eyes
        eye_offset = self.radius // 2
        pygame.draw.circle(screen, WHITE, (x - eye_offset, y - eye_offset), 3)
        pygame.draw.circle(screen, WHITE, (x + eye_offset, y - eye_offset), 3)
        # Pupils
        pygame.draw.circle(screen, BLACK, (x - eye_offset, y - eye_offset), 1)
        pygame.draw.circle(screen, BLACK, (x + eye_offset, y - eye_offset), 1)

# Build the level
def build_level():
    WALLS.clear()
    DOTS.clear()
    POWER_PELLETS.clear()
    PORTALS.clear()
    for row_index, row in enumerate(LEVEL_LAYOUT):
        for col_index, col in enumerate(row):
            x = col_index * TILE_SIZE
            y = row_index * TILE_SIZE + TILE_SIZE * 2
            if col == 'X':
                WALLS.append(Wall(x, y))
            elif col == '.':
                DOTS.append(Dot(x, y))
            elif col == 'O':
                POWER_PELLETS.append(PowerPellet(x, y))
            elif col == ' ':
                pass
            # You can add portal handling if needed

def reset_level():
    global pacman, ghosts
    pacman.position = pygame.Vector2(14 * TILE_SIZE, (17 * TILE_SIZE) + TILE_SIZE * 2)
    pacman.direction = LEFT
    pacman.next_direction = LEFT
    pacman.alive = True
    for ghost in ghosts:
        ghost.reset_position()

def game_over():
    game_over_text = big_font.render("GAME OVER", True, RED)
    screen.blit(game_over_text, (WIDTH // 2 - 100, HEIGHT // 2 - 50))
    pygame.display.flip()
    pygame.time.wait(3000)
    pygame.quit()
    sys.exit()

def main():
    global pacman, ghosts
    build_level()
    # Pacman's starting position
    pacman = Pacman(14 * TILE_SIZE, (17 * TILE_SIZE) + TILE_SIZE * 2)

    # Ghost target functions
    def blinky_target():
        return pacman.position

    def pinky_target():
        return pacman.position + pygame.Vector2(pacman.direction) * TILE_SIZE * 4

    def inky_target():
        vec = pacman.position + pygame.Vector2(pacman.direction) * TILE_SIZE * 2
        blinky_vec = ghosts[0].position
        return vec * 2 - blinky_vec

    def clyde_target():
        distance = (pacman.position - ghosts[3].position).length()
        if distance > TILE_SIZE * 8:
            return pacman.position
        else:
            return pygame.Vector2(0, HEIGHT)

    # Ghosts' starting positions
    ghosts_list = [
        {'x': 14 * TILE_SIZE, 'y': (11 * TILE_SIZE) + TILE_SIZE * 2, 'color': RED, 'target': blinky_target},
        {'x': 13 * TILE_SIZE, 'y': (13 * TILE_SIZE) + TILE_SIZE * 2, 'color': PINK, 'target': pinky_target},
        {'x': 14 * TILE_SIZE, 'y': (13 * TILE_SIZE) + TILE_SIZE * 2, 'color': CYAN, 'target': inky_target},
        {'x': 15 * TILE_SIZE, 'y': (13 * TILE_SIZE) + TILE_SIZE * 2, 'color': ORANGE, 'target': clyde_target},
    ]

    # Initialize ghosts
    global ghosts
    ghosts = []
    for ghost_info in ghosts_list:
        ghost = Ghost(ghost_info['x'], ghost_info['y'], ghost_info['color'], ghost_info['target'])
        ghosts.append(ghost)

    main_loop()

def main_loop():
    global SCORE, LEVEL, LIVES
    running = True
    while running:
        try:
            clock.tick(FPS)
            screen.fill(BLACK)
            # Event handling
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        pacman.next_direction = LEFT
                    elif event.key == pygame.K_RIGHT:
                        pacman.next_direction = RIGHT
                    elif event.key == pygame.K_UP:
                        pacman.next_direction = UP
                    elif event.key == pygame.K_DOWN:
                        pacman.next_direction = DOWN

            # Update game objects
            pacman.update()
            for ghost in ghosts:
                ghost.update()

            # Check for level completion
            if not DOTS and not POWER_PELLETS:
                LEVEL += 1
                reset_level()
                build_level()
                pacman.speed += 0.5
                for ghost in ghosts:
                    ghost.speed += 0.5

            # Draw game objects
            for wall in WALLS:
                wall.draw()
            for dot in DOTS:
                dot.draw()
            for pellet in POWER_PELLETS:
                pellet.draw()
            pacman.draw()
            for ghost in ghosts:
                ghost.draw()

            # Draw UI
            score_text = font.render(f"Score: {SCORE}", True, WHITE)
            lives_text = font.render(f"Lives: {LIVES}", True, WHITE)
            level_text = font.render(f"Level: {LEVEL}", True, WHITE)
            screen.blit(score_text, (10, 10))
            screen.blit(lives_text, (WIDTH - 100, 10))
            screen.blit(level_text, (WIDTH // 2 - 40, 10))

            pygame.display.flip()
        except Exception as e:
            print(f"An error occurred: {e}")
            pygame.quit()
            sys.exit()

if __name__ == '__main__':
    main()
