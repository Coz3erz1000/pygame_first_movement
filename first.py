import pygame
import random

# Initialize Pygame
pygame.init()

# Screen settings
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Infinite Top-Down World")
clock = pygame.time.Clock()

# Colors
GREEN = (34, 139, 34)  # Grass
BROWN = (139, 69, 19)  # Trees
RED = (255, 0, 0)      # Player

# Tile size
TILE_SIZE = 40

# Player
player_x, player_y = 0, 0
player_speed = 20

# Camera offset
camera_x, camera_y = 0, 0

# Tree generation seed and storage
random.seed(12345)  # Use fixed seed for consistent world
generated_trees = {}

def get_tree_positions(chunk_x, chunk_y):
    """Generate pseudo-random trees for a chunk using hash-like randomness."""
    if (chunk_x, chunk_y) not in generated_trees:
        trees = []
        for i in range(15):  # ~15 trees per chunk
            rand = random.Random(abs(hash((chunk_x, chunk_y, i)) % 0xFFFFFFFF))
            x = chunk_x * 20 + rand.randint(0, 19)
            y = chunk_y * 20 + rand.randint(0, 19)
            trees.append((x, y))
        generated_trees[(chunk_x, chunk_y)] = trees
    return generated_trees[(chunk_x, chunk_y)]

# Main game loop
running = True
while running:
    dt = clock.tick(60) / 1000  # Delta time in seconds

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Real-time movement (held keys)
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        player_x -= player_speed
    if keys[pygame.K_RIGHT]:
        player_x += player_speed
    if keys[pygame.K_UP]:
        player_y -= player_speed
    if keys[pygame.K_DOWN]:
        player_y += player_speed

    # Smooth camera follow (fractional tracking)
    target_camera_x = -player_x + SCREEN_WIDTH // 2
    target_camera_y = -player_y + SCREEN_HEIGHT // 2
    camera_x += (target_camera_x - camera_x) * 0.1
    camera_y += (target_camera_y - camera_y) * 0.1

    # Clear screen
    screen.fill(GREEN)

    # Determine visible chunks
    min_chunk_x = int((camera_x - TILE_SIZE) // (20 * TILE_SIZE)) - 1
    max_chunk_x = int((camera_x + SCREEN_WIDTH + TILE_SIZE) // (20 * TILE_SIZE)) + 1
    min_chunk_y = int((camera_y - TILE_SIZE) // (20 * TILE_SIZE)) - 1
    max_chunk_y = int((camera_y + SCREEN_HEIGHT + TILE_SIZE) // (20 * TILE_SIZE)) + 1

    # Draw trees in visible area
    for cx in range(min_chunk_x, max_chunk_x + 1):
        for cy in range(min_chunk_y, max_chunk_y + 1):
            for tx, ty in get_tree_positions(cx, cy):
                screen_x = tx * TILE_SIZE + camera_x
                screen_y = ty * TILE_SIZE + camera_y
                if -TILE_SIZE <= screen_x <= SCREEN_WIDTH + TILE_SIZE and \
                   -TILE_SIZE <= screen_y <= SCREEN_HEIGHT + TILE_SIZE:
                    pygame.draw.rect(screen, BROWN, (screen_x, screen_y, TILE_SIZE, TILE_SIZE))

    # Draw player
    pygame.draw.rect(screen, RED, (
        player_x + camera_x,
        player_y + camera_y,
        TILE_SIZE,
        TILE_SIZE
    ))

    # Update display
    pygame.display.flip()

pygame.quit()