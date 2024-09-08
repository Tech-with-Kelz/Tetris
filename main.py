import pygame
import random

# Initialize Pygame
pygame.init()

# Define global variables
GAME_WIDTH, GAME_HEIGHT = 300, 600  # Size of the game window
SCORE_WIDTH, SCORE_HEIGHT = 200, 100  # Size of the score window
BLOCK_SIZE = 30  # Size of each block (for the grid and tetrominoes)

# Create a combined window that includes space for both game and score
SCREEN_WIDTH = GAME_WIDTH + SCORE_WIDTH
SCREEN_HEIGHT = GAME_HEIGHT

GRID_WIDTH, GRID_HEIGHT = GAME_WIDTH // BLOCK_SIZE, GAME_HEIGHT // BLOCK_SIZE

# Colors (R, G, B)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
CYAN = (0, 255, 255)
BLUE = (0, 0, 255)
ORANGE = (255, 165, 0)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)
PURPLE = (160, 32, 240)
RED = (255, 0, 0)

# Font for displaying score and new shape heading
font = pygame.font.SysFont("bahnschrift", 25)
heading_font = pygame.font.SysFont("bahnschrift", 20)

# Define Tetromino shapes
TETROMINOES = [
    [[1, 1, 1, 1]],  # I
    [[1, 1, 1], [0, 1, 0]],  # T
    [[1, 1], [1, 1]],  # O
    [[0, 1, 1], [1, 1, 0]],  # S
    [[1, 1, 0], [0, 1, 1]],  # Z
    [[1, 1, 1], [1, 0, 0]],  # L
    [[1, 1, 1], [0, 0, 1]],  # J
]

# Colors for each tetromino
TETROMINO_COLORS = [CYAN, PURPLE, YELLOW, GREEN, RED, ORANGE, BLUE]

# Function to rotate a shape
def rotate_shape(shape):
    return [[shape[y][x] for y in range(len(shape))] for x in range(len(shape[0]) - 1, -1, -1)]

# Class for the Tetris Game
class TetrisGame:
    def __init__(self):
        self.grid = [[0] * GRID_WIDTH for _ in range(GRID_HEIGHT)]
        self.current_tetromino, self.current_color = self.get_new_tetromino()
        self.next_tetromino, self.next_color = self.get_new_tetromino()  # Store the next tetromino
        self.tetromino_x = GRID_WIDTH // 2 - len(self.current_tetromino[0]) // 2
        self.tetromino_y = 0
        self.score = 0
        self.game_over = False

    def get_new_tetromino(self):
        """Get a random new tetromino."""
        shape = random.choice(TETROMINOES)
        color = TETROMINO_COLORS[TETROMINOES.index(shape)]
        return shape, color

    def draw_grid(self, screen):
        """Draw the grid and filled blocks."""
        for y in range(GRID_HEIGHT):
            for x in range(GRID_WIDTH):
                if self.grid[y][x]:
                    pygame.draw.rect(screen, self.grid[y][x], (x * BLOCK_SIZE, y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE))
                pygame.draw.rect(screen, WHITE, (x * BLOCK_SIZE, y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE), 1)

    def draw_tetromino(self, screen):
        """Draw the current falling tetromino."""
        shape = self.current_tetromino
        for y, row in enumerate(shape):
            for x, cell in enumerate(row):
                if cell:
                    pygame.draw.rect(screen, self.current_color, ((self.tetromino_x + x) * BLOCK_SIZE, (self.tetromino_y + y) * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE))

    def draw_next_tetromino(self, surface):
        """Draw the next tetromino in the score window."""
        shape = self.next_tetromino
        for y, row in enumerate(shape):
            for x, cell in enumerate(row):
                if cell:
                    pygame.draw.rect(surface, self.next_color, (50 + x * BLOCK_SIZE, 80 + y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE))

    def move_tetromino(self, dx, dy):
        """Move the tetromino and check for collisions."""
        self.tetromino_x += dx
        self.tetromino_y += dy
        if not self.is_valid_position():
            self.tetromino_x -= dx
            self.tetromino_y -= dy
            return False
        return True

    def rotate_tetromino(self):
        """Rotate the tetromino and check for collisions."""
        shape = self.current_tetromino
        self.current_tetromino = rotate_shape(shape)
        if not self.is_valid_position():
            self.current_tetromino = rotate_shape(rotate_shape(rotate_shape(shape)))

    def is_valid_position(self):
        """Check if the tetromino is in a valid position."""
        shape = self.current_tetromino
        for y, row in enumerate(shape):
            for x, cell in enumerate(row):
                if cell:
                    if x + self.tetromino_x < 0 or x + self.tetromino_x >= GRID_WIDTH or y + self.tetromino_y >= GRID_HEIGHT:
                        return False
                    if self.grid[y + self.tetromino_y][x + self.tetromino_x]:
                        return False
        return True

    def freeze_tetromino(self):
        """Freeze the current tetromino in the grid and check for line clears."""
        shape = self.current_tetromino
        for y, row in enumerate(shape):
            for x, cell in enumerate(row):
                if cell:
                    self.grid[y + self.tetromino_y][x + self.tetromino_x] = self.current_color
        self.clear_lines()
        self.current_tetromino, self.current_color = self.next_tetromino, self.next_color  # Move the next tetromino to current
        self.next_tetromino, self.next_color = self.get_new_tetromino()  # Get a new next tetromino
        self.tetromino_x = GRID_WIDTH // 2 - len(self.current_tetromino[0]) // 2
        self.tetromino_y = 0
        if not self.is_valid_position():
            self.game_over = True

    def clear_lines(self):
        """Check for and clear completed lines."""
        new_grid = [row for row in self.grid if any(cell == 0 for cell in row)]
        lines_cleared = GRID_HEIGHT - len(new_grid)
        self.score += lines_cleared * 10  # Score increases by 10 for each line cleared
        self.grid = [[0] * GRID_WIDTH for _ in range(lines_cleared)] + new_grid

    def update(self):
        """Update the game state (move tetromino down)."""
        if not self.move_tetromino(0, 1):
            self.freeze_tetromino()

# Game loop
def main():
    # Create the combined screen that includes both game and score display
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption('Tetris')

    clock = pygame.time.Clock()

    game = TetrisGame()
    fall_speed = 500  # Milliseconds
    last_fall_time = pygame.time.get_ticks()

    # Create a surface for the score display
    score_surface = pygame.Surface((SCORE_WIDTH, SCREEN_HEIGHT))

    while not game.game_over:
        screen.fill(BLACK)
        score_surface.fill((50, 50, 50))  # Gray background for the score window

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    game.move_tetromino(-1, 0)
                elif event.key == pygame.K_RIGHT:
                    game.move_tetromino(1, 0)
                elif event.key == pygame.K_DOWN:
                    game.move_tetromino(0, 1)
                elif event.key == pygame.K_UP:
                    game.rotate_tetromino()

        # Update the game state (move tetromino down every fall_speed milliseconds)
        if pygame.time.get_ticks() - last_fall_time > fall_speed:
            game.update()
            last_fall_time = pygame.time.get_ticks()

        # Draw the game grid and tetromino on the game portion of the screen
        game.draw_grid(screen)
        game.draw_tetromino(screen)

        # Display the score in the separate score window
        score_text = font.render(f"Score: {game.score}", True, WHITE)
        score_surface.blit(score_text, [10, 10])  # Draw score on score surface

        # Draw the "New Shape" heading
        new_shape_heading = heading_font.render("Next Shape", True, WHITE)
        score_surface.blit(new_shape_heading, (50, 50))

        # Draw the next tetromino in the score window
        game.draw_next_tetromino(score_surface)

        # Blit the score window onto the main screen (right side)
        screen.blit(score_surface, (GAME_WIDTH, 0))

        pygame.display.update()
        clock.tick(60)

    print(f"Game Over! Final Score: {game.score}")

if __name__ == "__main__":
    main()
