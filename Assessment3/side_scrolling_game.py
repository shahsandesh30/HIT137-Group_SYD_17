# import pygame to create 2d game
import pygame
import random
import os

# initialize Pygame
pygame.init()

# screen width and height
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 30

# different colors to be used within the game
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# Get the directory of the current script to run the program
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# defining player class
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        # dynamic path to image
        image_path = os.path.join(BASE_DIR, "assets", "player.png")
        self.original_image = pygame.image.load(image_path).convert_alpha()  # Keep the original image
        self.image = pygame.transform.scale(self.original_image, (80, 100))
        self.rect = self.image.get_rect()
        self.rect.x = 100
        self.rect.y = SCREEN_HEIGHT - 100

        self.speed_x = 0
        self.speed_y = 0
        self.jump_speed = -15
        self.gravity = 0.8
        self.is_jumping = False
        self.last_direction = "right"

        self.health = 100
        self.lives = 3
        self.move_speed = 5
        self.score = 0

    def move(self, direction):
        if direction == "left":
            self.speed_x = -self.move_speed
            self.last_direction = "left"
            self.image = pygame.transform.flip(
                pygame.transform.scale(self.original_image, (80, 100)), True, False
            )  # Flip horizontally
        elif direction == "right":
            self.speed_x = self.move_speed
            self.last_direction = "right"
            self.image = pygame.transform.scale(self.original_image, (80, 100))  # Reset to original
        else:
            self.speed_x = 0

    def set_speed(self, speed):
        self.move_speed = speed

    def jump(self):
        if not self.is_jumping:
            self.speed_y = self.jump_speed
            self.is_jumping = True

    def take_damage(self, amount):
        self.health -= amount
        if self.health <= 0:
            self.health = 100
            self.lose_life()

    def lose_life(self):
        self.lives -= 1

    def update(self):
        self.speed_y += self.gravity
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y

        if self.rect.bottom > SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT
            self.speed_y = 0
            self.is_jumping = False

        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH

# define projectile class
class Projectile(pygame.sprite.Sprite):
    def __init__(self, x, y, direction="right"):
        super().__init__()

        # bullet surface with colour red
        self.image = pygame.Surface((10, 5))
        self.image.fill(RED)
        self.rect = self.image.get_rect()

        # bullet starting position
        offset = 30 if direction == "right" else -30
        self.rect.x = x + offset
        self.rect.y = y + 5  # Slight vertical adjustment to align with the gun

        # Set movement speed and damage
        self.speed = 10 if direction == "right" else -10
        self.damage = 25


    def update(self):
        self.rect.x += self.speed
        if self.rect.right < 0 or self.rect.left > SCREEN_WIDTH:
            self.kill()

# define enemy class
class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y, health, enemy_type):
        super().__init__()
        # Load enemy image based on type
        image_path = os.path.join(BASE_DIR, "assets", f"{enemy_type}.png")
        original_image = pygame.image.load(image_path).convert_alpha()

        # Get original dimensions
        original_width, original_height = original_image.get_size()

        # Desired dimensions
        max_width, max_height = 80, 100

        # Calculate scaling factor to maintain aspect ratio
        scale_factor = min(max_width / original_width, max_height / original_height)

        # Calculate new dimensions
        new_width = int(original_width * scale_factor)
        new_height = int(original_height * scale_factor)

        # Scale the image proportionally
        self.image = pygame.transform.scale(original_image, (new_width, new_height))
        self.rect = self.image.get_rect()

        # Adjust position to ensure the enemy is fully visible
        self.rect.x = x
        self.rect.y = SCREEN_HEIGHT - new_height + 5  # Lower the enemy by increasing the offset

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


class Collectible(pygame.sprite.Sprite):
    def __init__(self, x, y, kind):
        super().__init__()
        # Load collectible image based on type
        if kind == 'health':
            image_path = os.path.join(BASE_DIR, "assets", "apple.png")
        elif kind == 'life':
            image_path = os.path.join(BASE_DIR, "assets", "health.png")
        else:  # score
            image_path = os.path.join(BASE_DIR, "assets", "berry.png")
        self.image = pygame.image.load(image_path).convert_alpha()
        self.image = pygame.transform.scale(self.image, (30, 30))
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


class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Side Scrolling Game")
        self.clock = pygame.time.Clock()
        self.running = True
        self.level = 1

        self.all_sprites = pygame.sprite.Group()
        self.projectiles = pygame.sprite.Group()
        self.enemies = pygame.sprite.Group()
        self.collectibles = pygame.sprite.Group()

        self.player = Player()
        self.all_sprites.add(self.player)

        self.spawn_level()

    def level_start_screen(self):
        """Show the current level number before the level begins."""
        self.screen.fill(BLACK)

        # Create and render the level text
        font = pygame.font.SysFont(None, 72)
        text = font.render(f"Level {self.level}", True, WHITE)
        self.screen.blit(text, (SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 - 50))

        pygame.display.flip()

        # Wait 2 seconds before starting the level
        pygame.time.delay(2000)


    def spawn_level(self):
        """Spawn enemies and collectibles for the current level."""
        self.enemies.empty()
        self.collectibles.empty()

        # Start a timer to display the level number briefly
        self.level_start_timer = 60  # Display for 60 frames (1 second at 60 FPS)

        # Enemy types and health scaling
        enemy_types = {1: "enemy1", 2: "enemy2", 3: "enemy3"}
        enemy_health = {1: 50, 2: 100, 3: 150}

        # Spawn enemies
        for i in range(3 * self.level):
            enemy = Enemy(
                random.randint(400, 700),
                SCREEN_HEIGHT - 80,
                health=enemy_health[self.level],
                enemy_type=enemy_types[self.level]
            )
            self.enemies.add(enemy)
            self.all_sprites.add(enemy)

        # Spawn collectibles
        for i in range(2):
            kind = random.choice(['health', 'life'])
            item = Collectible(random.randint(200, 700), SCREEN_HEIGHT - 100, kind)
            self.collectibles.add(item)
            self.all_sprites.add(item)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:  # Change from SPACEBAR to UP ARROW
                    self.player.jump()
                if event.key == pygame.K_f:
                    proj = Projectile(self.player.rect.centerx, self.player.rect.centery, self.player.last_direction)
                    self.projectiles.add(proj)
                    self.all_sprites.add(proj)

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.player.move("left")
        elif keys[pygame.K_RIGHT]:
            self.player.move("right")
        else:
            self.player.move("stop")

    def draw_health_bar(self, surface, x, y, health, max_health):
        BAR_WIDTH = 200
        BAR_HEIGHT = 20
        fill = (health / max_health) * BAR_WIDTH
        outline_rect = pygame.Rect(x, y, BAR_WIDTH, BAR_HEIGHT)
        fill_rect = pygame.Rect(x, y, fill, BAR_HEIGHT)
        pygame.draw.rect(surface, RED, outline_rect)
        pygame.draw.rect(surface, GREEN, fill_rect)
        pygame.draw.rect(surface, WHITE, outline_rect, 2)

    def update(self):
        """Handle game updates for all elements each frame."""
        self.all_sprites.update()

        # Countdown delay before level starts
        if self.level_start_timer > 0:
            self.level_start_timer -= 1

        # Check if any projectile hits an enemy
        for projectile in self.projectiles:
            hits = pygame.sprite.spritecollide(projectile, self.enemies, False)
            for enemy in hits:
                enemy.take_damage(projectile.damage)
                projectile.kill()
                self.player.score += 10

        # Check if the player touches any collectible
        for item in pygame.sprite.spritecollide(self.player, self.collectibles, False):
            item.apply_to_player(self.player)

        # Check if the player collides with any enemy
        for enemy in pygame.sprite.spritecollide(self.player, self.enemies, False):
            self.player.take_damage(10)

        # Move to next level if all enemies are defeated
        if not self.enemies:
            self.level += 1
            if self.level > 3:
                self.you_win_screen()
                return
            self.spawn_level()

        # End the game if the player has no lives left
        if self.player.lives <= 0:
            self.running = False


    def draw(self):
        """Draw all game elements, including the level number."""
        self.screen.fill(BLACK)
        self.all_sprites.draw(self.screen)
        self.draw_health_bar(self.screen, 10, 10, self.player.health, 100)

        # Display score, lives, and level
        font = pygame.font.SysFont(None, 36)
        score_text = font.render(f"Score: {self.player.score}", True, WHITE)
        lives_text = font.render(f"Lives: {self.player.lives}", True, WHITE)
        level_text = font.render(f"Level: {self.level}", True, WHITE)

        self.screen.blit(score_text, (10, 40))
        self.screen.blit(lives_text, (10, 70))
        self.screen.blit(level_text, (10, 100))  # Display level number at the top-left corner

        # Optionally, display the level number in the center of the screen
        if self.level_start_timer > 0:
            level_font = pygame.font.SysFont(None, 72)
            level_center_text = level_font.render(f"Level {self.level}", True, WHITE)
            self.screen.blit(level_center_text, (SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 - 50))

        pygame.display.flip()

    def game_over_screen(self):
        self.screen.fill(BLACK)
        font = pygame.font.SysFont(None, 72)
        text = font.render("Game Over", True, RED)
        self.screen.blit(text, (SCREEN_WIDTH//2 - 150, SCREEN_HEIGHT//2 - 100))
        font_small = pygame.font.SysFont(None, 36)
        restart_text = font_small.render("Press R to Restart or Q to Quit", True, WHITE)
        self.screen.blit(restart_text, (SCREEN_WIDTH//2 - 180, SCREEN_HEIGHT//2))
        pygame.display.flip()

        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    waiting = False
                    self.running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        self.__init__()
                        self.run()
                        waiting = False
                    if event.key == pygame.K_q:
                        waiting = False
                        self.running = False

    def you_win_screen(self):
        self.screen.fill(BLACK)
        font = pygame.font.SysFont(None, 72)
        text = font.render("You Win!", True, GREEN)
        self.screen.blit(text, (SCREEN_WIDTH//2 - 150, SCREEN_HEIGHT//2 - 100))
        font_small = pygame.font.SysFont(None, 36)
        restart_text = font_small.render("Press R to Restart or Q to Quit", True, WHITE)
        self.screen.blit(restart_text, (SCREEN_WIDTH//2 - 180, SCREEN_HEIGHT//2))
        pygame.display.flip()

        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    waiting = False
                    self.running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        self.__init__()
                        self.run()
                        waiting = False
                    if event.key == pygame.K_q:
                        waiting = False
                        self.running = False

    def run(self):
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
