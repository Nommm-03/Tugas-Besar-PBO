import pygame
import math

# Color definitions
BLUE = (10, 10, 128)
RED = (255, 0, 0)
BLACK = (0, 0, 0)

# Screen width
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

pygame.init()

class Player:
    def __init__(self, x, y):
        self.image = pygame.Surface([50, 45])
        self.image.fill(BLUE)
        self.rect = self.image.get_rect()
        self.rect.y = y
        self.rect.x = x
        self.score = 0
        self.speed = 5  # Initial speed

        self.change_x = 0
        self.change_y = 0
        self.walls = None

    def changespeed(self, x, y):
        self.change_x += x * self.speed
        self.change_y += y * self.speed

    def update(self):
        self.rect.x += self.change_x

        block_hit_list = [wall for wall in self.walls if self.rect.colliderect(wall.rect)]
        for block in block_hit_list:
            if self.change_x > 0:
                self.rect.right = block.rect.left
            elif self.change_x < 0:
                self.rect.left = block.rect.right

        self.rect.y += self.change_y

        block_hit_list = [wall for wall in self.walls if self.rect.colliderect(wall.rect)]
        for block in block_hit_list:
            if self.change_y > 0:
                self.rect.bottom = block.rect.top
            elif self.change_y < 0:
                self.rect.top = block.rect.bottom

    def draw(self, screen):
        screen.blit(self.image, self.rect.topleft)

class Player2:
    def __init__(self, x, y, player, speed):
        original_image = pygame.image.load("ENEMY/Ghost2.png").convert_alpha()
        scaled_width = 100
        scaled_height = 100
        self.image = pygame.transform.scale(original_image, (scaled_width, scaled_height))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.player = player
        self.speed = speed

    def update(self):
        dx = self.player.rect.centerx - self.rect.centerx
        dy = self.player.rect.centery - self.rect.centery
        distance = math.sqrt(dx ** 2 + dy ** 2)
        if distance != 0:
            dx /= distance
            dy /= distance

        self.rect.x += dx * self.speed
        self.rect.y += dy * self.speed

    def draw(self, screen):
        screen.blit(self.image, self.rect.topleft)

class Wall:
    def __init__(self, x, y, width, height):
        self.image = pygame.Surface([width, height])
        self.image.fill(BLUE)
        self.rect = self.image.get_rect()
        self.rect.y = y
        self.rect.x = x

    def draw(self, screen):
        screen.blit(self.image, self.rect.topleft)

# Wall init
wall_list = []

# Pygame definitions
screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])
pygame.display.set_caption('test!')

# Left wall
wall = Wall(0, 0, 10, 600)
wall_list.append(wall)

# Top wall
wall = Wall(10, 0, 790, 10)
wall_list.append(wall)

# Right wall
wall = Wall(790, 0, 10, 600)
wall_list.append(wall)

# Bottom wall
wall = Wall(0, 590, 1000, 300)
wall_list.append(wall)

# Create the player
player = Player(50, 50)
player.walls = wall_list

# Create the first enemy
enemy1 = Player2(100, 100, player, 2)

# Create the second enemy with a different speed
enemy2 = Player2(200, 200, player, 3)

enemies = [enemy1, enemy2]

clock = pygame.time.Clock()

# Loop
done = False

while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:
                player.changespeed(-1, 0)
            elif event.key == pygame.K_d:
                player.changespeed(1, 0)
            elif event.key == pygame.K_w:
                player.changespeed(0, -1)
            elif event.key == pygame.K_s:
                player.changespeed(0, 1)
            elif event.key == pygame.K_UP:  # Increase speed
                player.speed += 1
            elif event.key == pygame.K_DOWN:  # Decrease speed
                player.speed -= 1
                if player.speed < 1:
                    player.speed = 1

        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_a:
                player.changespeed(1, 0)
            elif event.key == pygame.K_d:
                player.changespeed(-1, 0)
            elif event.key == pygame.K_w:
                player.changespeed(0, 1)
            elif event.key == pygame.K_s:
                player.changespeed(0, -1)

    player.update()
    for enemy in enemies:
        enemy.update()

    screen.fill(BLACK)
    player.draw(screen)
    for enemy in enemies:
        enemy.draw(screen)
    for wall in wall_list:
        wall.draw(screen)

    pygame.display.flip()
    clock.tick(100)

pygame.quit()
