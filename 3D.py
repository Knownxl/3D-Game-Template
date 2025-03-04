import pygame
import math

# Initialize Pygame
pygame.init()

# Screen settings
WIDTH, HEIGHT = 800, 600
FOV = math.pi / 3  # 60-degree field of view
NUM_RAYS = 120
MAX_DEPTH = 800
SCALE = WIDTH // NUM_RAYS

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
DARK_BLUE = (0, 0, 139)

# Map settings (1 = Wall, 0 = Empty space)
MAP = [
    "111111111111111111111111111",
    "100000000000000000000000001",
    "100000000000000000000000001",
    "100000001100000011000000011",
    "100000000000000000000000001",
    "100000000000000000000000001",
    "110011110001111100011110011",
    "100000000000000000000000001",
    "100000000000000000000000001",
    "100011000111001110001100001",
    "100000000000000000000000001",
    "100000000000000000000000001",
    "111110001111001111111111101",
    "100000000000000000000000001",
    "100000000000000000000000001",
    "111111111111111111111111111",
]
MAP_WIDTH = len(MAP[0])
MAP_HEIGHT = len(MAP)
TILE_SIZE = 100

# Player settings
player_x, player_y = 150, 150
player_angle = 0
player_speed = 3
rot_speed = 0.05

# Initialize screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
running = True

# Raycasting function
def cast_rays():
    for ray in range(NUM_RAYS):
        angle = player_angle - FOV / 2 + (ray / NUM_RAYS) * FOV
        sin_a = math.sin(angle)
        cos_a = math.cos(angle)
        
        # Cast the ray
        for depth in range(1, MAX_DEPTH, 5):
            target_x = int(player_x + depth * cos_a)
            target_y = int(player_y + depth * sin_a)
            
            if 0 <= target_x // TILE_SIZE < MAP_WIDTH and 0 <= target_y // TILE_SIZE < MAP_HEIGHT:
                if MAP[target_y // TILE_SIZE][target_x // TILE_SIZE] == '1':
                    depth *= math.cos(player_angle - angle)  # Fix fisheye effect
                    wall_height = min(50000 / (depth + 0.0001), HEIGHT)
                    color = BLUE if depth < MAX_DEPTH / 2 else DARK_BLUE
                    pygame.draw.rect(screen, color, (ray * SCALE, HEIGHT // 2 - wall_height // 2, SCALE, wall_height))
                    break

# Game loop
while running:
    screen.fill(BLACK)
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        player_angle -= rot_speed
    if keys[pygame.K_RIGHT]:
        player_angle += rot_speed
    if keys[pygame.K_UP]:
        player_x += player_speed * math.cos(player_angle)
        player_y += player_speed * math.sin(player_angle)
    if keys[pygame.K_DOWN]:
        player_x -= player_speed * math.cos(player_angle)
        player_y -= player_speed * math.sin(player_angle)
    
    cast_rays()
    pygame.display.flip()
    clock.tick(60)
    
pygame.quit()
