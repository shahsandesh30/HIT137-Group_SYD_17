# import pygame to create 2d game
import pygame
import random

# initialize Pygame
pygame.init()
# screen width and height
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 30

# different colors to be used in the game
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# Player Class
import pygame

import pygame

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        # Load and scale the player image
        self.image = pygame.image.load("shooting-game.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (100, 100))

        # Set initial position
        self.rect = self.image.get_rect()
        self.rect.x = 100
        self.rect.y = SCREEN_HEIGHT - 100

        # Movement and physics attributes
        self.speed_x = 0
        self.speed_y = 0
        self.move_speed = 5
        self.jump_speed = -15
        self.gravity = 0.8
        self.is_jumping = False

        # Player status
        self.health = 100
        self.lives = 3
        self.score = 0

    def move(self, direction):
        """Move the player left or right based on direction."""
        directions = {
            "left": -self.move_speed,
            "right": self.move_speed
        }
        self.speed_x = directions.get(direction, 0)

    def set_speed(self, speed):
        """Update player's horizontal movement speed."""
        self.move_speed = speed

    def jump(self):
        """Make the player jump if not already in the air."""
        if not self.is_jumping:
            self.speed_y = self.jump_speed
            self.is_jumping = True

    def take_damage(self, amount):
        """Reduce player's health and handle life loss."""
        self.health -= amount
        if self.health <= 0:
            self.health = 100
            self.lose_life()

    def lose_life(self):
        """Decrease player's lives by one."""
        self.lives -= 1

    def update(self):
        """Update player's position based on movement and physics."""
        # Apply gravity
        self.speed_y += self.gravity

        # Update position
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y

        # Floor collision
        if self.rect.bottom > SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT
            self.speed_y = 0
            self.is_jumping = False

        # Horizontal bounds
        self.rect.left = max(0, self.rect.left)
        self.rect.right = min(SCREEN_WIDTH, self.rect.right)

#projectile classa
class Projectile(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface([10, 5])
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = 10
        self.damage = 25

    def update(self):
        self.rect.x += self.speed
        if self.rect.right > SCREEN_WIDTH:
            self.kill()

# Enemy Class
class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y, health=50):
        super().__init__()
        self.image = pygame.Surface([40, 40])
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = 2
        self.direction = 1
        self.health = health

    def update(self):
        self.rect.x += self.speed * self.direction
        if self.rect.left < 0 or self.rect.right > SCREEN_WIDTH:
            self.direction *= -1

    def take_damage(self, amount):
        self.health -= amount
        if self.health <= 0:
            self.kill()

# Collectible Class
class Collectible(pygame.sprite.Sprite):
    def __init__(self, x, y, kind):
        super().__init__()
        self.image = pygame.Surface([20, 20])
        self.image.fill(GREEN if kind == 'health' else WHITE)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.kind = kind

    def apply_to_player(self, player):
        if self.kind == 'health':
            player.health = min(100, player.health + 25)
        elif self.kind == 'life':
            player.lives += 1
        player.score += 5
        self.kill()

# Game Class
import pygame
import random

class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Side Scrolling Game")
        self.clock = pygame.time.Clock()
        self.running = True
        self.level = 1

        # Sprite groups
        self.all_sprites = pygame.sprite.Group()
        self.projectiles = pygame.sprite.Group()
        self.enemies = pygame.sprite.Group()
        self.collectibles = pygame.sprite.Group()

        # Player setup
        self.player = Player()
        self.all_sprites.add(self.player)

        # Initial level spawn
        self.spawn_level()

    def spawn_level(self):
        """Set up enemies and collectibles for the current level."""
        self.enemies.empty()
        self.collectibles.empty()

        if self.level == 3:
            boss = Enemy(600, SCREEN_HEIGHT - 80, health=150)
            self.enemies.add(boss)
            self.all_sprites.add(boss)
        else:
            for _ in range(3 * self.level):
                enemy = Enemy(random.randint(400, 700), SCREEN_HEIGHT - 80)
                self.enemies.add(enemy)
                self.all_sprites.add(enemy)

        for _ in range(2):
            kind = random.choice(['health', 'life'])
            item = Collectible(random.randint(200, 700), SCREEN_HEIGHT - 100, kind)
            self.collectibles.add(item)
            self.all_sprites.add(item)

    def handle_events(self):
        """Handle user input events."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.player.jump()
                elif event.key == pygame.K_f:
                    self.fire_projectile()

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.player.move("left")
        elif keys[pygame.K_RIGHT]:
            self.player.move("right")
        else:
            self.player.move("stop")

    def fire_projectile(self):
        """Create and fire a projectile from the player."""
        proj = Projectile(self.player.rect.centerx, self.player.rect.centery)
        self.projectiles.add(proj)
        self.all_sprites.add(proj)

    def draw_health_bar(self, surface, x, y, health, max_health):
        """Draw the health bar."""
        BAR_WIDTH = 200
        BAR_HEIGHT = 20
        fill = (health / max_health) * BAR_WIDTH
        outline_rect = pygame.Rect(x, y, BAR_WIDTH, BAR_HEIGHT)
        fill_rect = pygame.Rect(x, y, fill, BAR_HEIGHT)
        pygame.draw.rect(surface, RED, outline_rect)
        pygame.draw.rect(surface, GREEN, fill_rect)
        pygame.draw.rect(surface, WHITE, outline_rect, 2)

    def update(self):
        """Update all game elements and check for collisions."""
        self.all_sprites.update()

        # Projectile-enemy collisions
        for proj in self.projectiles:
            hits = pygame.sprite.spritecollide(proj, self.enemies, False)
            for enemy in hits:
                enemy.take_damage(proj.damage)
                proj.kill()
                self.player.score += 10

        # Player-collectible collisions
        collectible_hits = pygame.sprite.spritecollide(self.player, self.collectibles, True)
        for item in collectible_hits:
            item.apply_to_player(self.player)

        # Advance level if enemies cleared
        if not self.enemies:
            self.level += 1
            if self.level > 3:
                self.running = False
            else:
                self.spawn_level()

        # End game if player dies
        if self.player.lives <= 0:
            self.running = False

    def display_text(self, text, size, x, y, color=WHITE):
        """Helper to render and display text on screen."""
        font = pygame.font.SysFont(None, size)
        rendered_text = font.render(text, True, color)
        self.screen.blit(rendered_text, (x, y))

    def draw(self):
        """Render all game visuals."""
        self.screen.fill(BLACK)
        self.all_sprites.draw(self.screen)

        self.draw_health_bar(self.screen, 10, 10, self.player.health, 100)

        # UI Texts
        self.display_text(f"Score: {self.player.score}", 36, 10, 40)
        self.display_text(f"Lives: {self.player.lives}", 36, 10, 70)
        self.display_text(f"Level: {self.level}", 36, 10, 100)

        pygame.display.flip()

    def game_over_screen(self):
        """Display the Game Over screen and handle restart/quit."""
        self.screen.fill(BLACK)
        self.display_text("Game Over", 72, SCREEN_WIDTH//2 - 150, SCREEN_HEIGHT//2 - 100, RED)
        self.display_text("Press R to Restart or Q to Quit", 36, SCREEN_WIDTH//2 - 180, SCREEN_HEIGHT//2)

        pygame.display.flip()
        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    waiting = False
                    self.running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        self.__init__()
                        self.run()
                        waiting = False
                    elif event.key == pygame.K_q:
                        waiting = False
                        self.running = False

    def run(self):
        """Main game loop."""
        while self.running:
            self.clock.tick(FPS)
            self.handle_events()
            self.update()
            self.draw()
        self.game_over_screen()


if __name__ == "__main__":
    game = Game()
    game.run()
    pygame.quit()
