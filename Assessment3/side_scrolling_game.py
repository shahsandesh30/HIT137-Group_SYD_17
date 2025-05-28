import pygame
import os
import random

# Initialize Pygame
pygame.init()

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface([40, 60])
        self.image.fill(BLUE)
        self.rect = self.image.get_rect()
        
        # Position
        self.rect.x = 100
        self.rect.y = SCREEN_HEIGHT - 100
        
        # Movement
        self.speed_x = 0
        self.speed_y = 0
        self.jump_speed = -15
        self.move_speed = 5
        
        # Physics
        self.gravity = 0.8
        self.is_jumping = False
        
        # Stats
        self.health = 100
        self.lives = 3
        self.score = 0

    def update(self):
        # Apply gravity
        self.speed_y += self.gravity
        
        # Update position
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y
        
        # Keep player on screen
        if self.rect.bottom > SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT
            self.speed_y = 0
            self.is_jumping = False
        
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH

    def jump(self):
        if not self.is_jumping:
            self.speed_y = self.jump_speed
            self.is_jumping = True

    def move_left(self):
        self.speed_x = -self.move_speed

    def move_right(self):
        self.speed_x = self.move_speed

    def stop(self):
        self.speed_x = 0

    def shoot(self):
        projectile = Projectile(self.rect.centerx, self.rect.centery)
        return projectile

class Projectile(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface([10, 5])
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        
        # Position
        self.rect.x = x
        self.rect.y = y
        
        # Movement
        self.speed = 10
        self.damage = 25

    def update(self):
        self.rect.x += self.speed
        
        # Remove if off screen
        if self.rect.right > SCREEN_WIDTH:
            self.kill()

class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Side Scrolling Game")
        self.clock = pygame.time.Clock()
        self.running = True
        
        # Sprite groups
        self.all_sprites = pygame.sprite.Group()
        self.projectiles = pygame.sprite.Group()
        
        # Create player
        self.player = Player()
        self.all_sprites.add(self.player)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.player.jump()
                if event.key == pygame.K_f:
                    projectile = self.player.shoot()
                    self.all_sprites.add(projectile)
                    self.projectiles.add(projectile)

        # Continuous movement
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.player.move_left()
        elif keys[pygame.K_RIGHT]:
            self.player.move_right()
        else:
            self.player.stop()

    def update(self):
        self.all_sprites.update()

    def draw(self):
        self.screen.fill(BLACK)
        self.all_sprites.draw(self.screen)
        pygame.display.flip()

    def run(self):
        while self.running:
            self.clock.tick(FPS)
            self.handle_events()
            self.update()
            self.draw()

if __name__ == "__main__":
    game = Game()
    game.run()
    pygame.quit()
