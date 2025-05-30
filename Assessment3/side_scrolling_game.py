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

# different colors to be used in the game
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# Get the directory of the current script
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Player Class 
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        # Load and scale player image
        image_path = os.path.join(BASE_DIR, "assets", "images", "player.png")
        self.original_image = pygame.image.load(image_path).convert_alpha()
        self.image = pygame.transform.scale(self.original_image, (80, 100))
        self.rect = self.image.get_rect()
        self.rect.x = 100
        self.rect.y = SCREEN_HEIGHT - 240  # Set initial position higher

        # Initialize player movement and physics attributes
        self.speed_x = 0
        self.speed_y = 0
        self.jump_speed = -15
        self.gravity = 0.8
        self.is_jumping = False
        self.last_direction = "right"

        # Initialize player stats
        self.health = 100
        self.lives = 3
        self.move_speed = 5
        self.score = 0

    def move(self, direction):
        # Handles player movement left, right, or stop
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
        # Sets the player's movement speed
        self.move_speed = speed

    def jump(self):
        # Initiates a player jump if not already jumping
        if not self.is_jumping:
            self.speed_y = self.jump_speed
            self.is_jumping = True

    def take_damage(self, amount):
        # Reduces player health and handles health depletion
        self.health -= amount
        if self.health <= 0:
            self.health = 100
            self.lose_life()

    def lose_life(self):
        # Decrements player lives
        self.lives -= 1

    def update(self):
        # Updates player position, handles gravity and screen boundaries
        self.speed_y += self.gravity
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y

        # Adjust ground collision to match the new height
        if self.rect.bottom > SCREEN_HEIGHT - 90:  # New ground level
            self.rect.bottom = SCREEN_HEIGHT - 90
            self.speed_y = 0
            self.is_jumping = False

        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH

# Projectile Class
class Projectile(pygame.sprite.Sprite):
    def __init__(self, x, y, direction="right"):
        super().__init__()
        # Create a simple rectangular projectile
        self.image = pygame.Surface([10, 5])
        self.image.fill(RED)
        self.rect = self.image.get_rect()

        # Adjust the starting position of the bullet to avoid immediate collision with the shooter
        if direction == "right":
            self.rect.x = x + 30  
        else:  
            self.rect.x = x - 30  

        self.rect.y = y + 5  # Adjust vertically to align with the gunpoint
        self.speed = 10 if direction == "right" else -10
        self.damage = 25

    def update(self):
        # Moves the projectile and removes it if off-screen
        self.rect.x += self.speed
        if self.rect.right < 0 or self.rect.left > SCREEN_WIDTH:
            self.kill()

# Enemy Class 
class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y, health, enemy_type):
        super().__init__()
        # Load enemy image based on type
        image_path = os.path.join(BASE_DIR, "assets", "images", f"{enemy_type}.png")
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
        self.rect.y = SCREEN_HEIGHT - new_height - 90  # Move the enemy up by 50 pixels

        # Initialize enemy attributes
        self.speed = 2
        self.direction = 1
        self.health = health
        self.enemy_type = enemy_type  # Add enemy_type attribute

        # Jumping attributes
        self.is_jumping = False
        self.jump_speed = -10
        self.gravity = 0.5

    def update(self):
        # Updates enemy position and handles screen boundaries and jumping
        self.rect.x += self.speed * self.direction
        if self.rect.left < 0 or self.rect.right > SCREEN_WIDTH:
            self.direction *= -1

        # Random jump logic for enemy3
        if self.enemy_type == 'enemy3' and not self.is_jumping:
            if random.random() < 0.01:  # Adjust probability as needed
                self.is_jumping = True
                self.speed_y = self.jump_speed

        # Apply gravity
        if self.is_jumping:
            self.speed_y += self.gravity
            self.rect.y += self.speed_y

            # Check if enemy has landed
            if self.rect.bottom >= SCREEN_HEIGHT - 90:
                self.rect.bottom = SCREEN_HEIGHT - 90
                self.is_jumping = False
                self.speed_y = 0

    def take_damage(self, amount):
        # Reduces enemy health and removes enemy if health is depleted
        self.health -= amount
        if self.health <= 0:
            self.kill()

# Collectible Class 
class Collectible(pygame.sprite.Sprite):
    def __init__(self, x, y, kind):
        super().__init__()
        # Load collectible image based on type
        if kind == 'health':
            image_path = os.path.join(BASE_DIR, "assets", "images", "apple.png")
        elif kind == 'life':
            image_path = os.path.join(BASE_DIR, "assets", "images", "heart.png")
        else:  # score
            image_path = os.path.join(BASE_DIR, "assets", "images", "berry.png")
        self.image = pygame.image.load(image_path).convert_alpha()
        self.image = pygame.transform.scale(self.image, (30, 30))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y - 50  # Move the collectible up by 50 pixels
        self.kind = kind

    def apply_to_player(self, player):
        # Applies the collectible's effect to the player
        if self.kind == 'health':
            player.health = min(100, player.health + 25)
        elif self.kind == 'life':
            player.lives += 1
        player.score += 5
        self.kill()

# Game Class 
class Game:
    def __init__(self):
        # Initialize screen and display
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Side Scrolling Game")
        self.clock = pygame.time.Clock()
        self.running = True
        self.level = 1

        # Initialize game clock and running state
        self.all_sprites = pygame.sprite.Group()
        self.projectiles = pygame.sprite.Group()
        self.enemies = pygame.sprite.Group()
        self.collectibles = pygame.sprite.Group()

        # Create player instance
        self.player = Player()
        self.all_sprites.add(self.player)

        # Initialize level start timer
        self.level_start_timer = 0  # Set to 0 initially

        # Load sound effects
        self.jump_sound = pygame.mixer.Sound(os.path.join(BASE_DIR, "assets", "sound", "jump.mp3"))
        self.shoot_sound = pygame.mixer.Sound(os.path.join(BASE_DIR, "assets", "sound", "gun.mp3"))
        self.enemy_hit_sound = pygame.mixer.Sound(os.path.join(BASE_DIR, "assets", "sound", "footstep.mp3"))
        self.collectible_sound = pygame.mixer.Sound(os.path.join(BASE_DIR, "assets", "sound", "health_pick.mp3"))
        self.extra_life_sound = pygame.mixer.Sound(os.path.join(BASE_DIR, "assets", "sound", "extralife.mp3"))
        self.game_over_sound = pygame.mixer.Sound(os.path.join(BASE_DIR, "assets", "sound", "gameover.mp3"))
        self.level_up_sound = pygame.mixer.Sound(os.path.join(BASE_DIR, "assets", "sound", "levelup.mp3"))

        # Load and play background music
        pygame.mixer.music.load(os.path.join(BASE_DIR, "assets", "sound", "background.mp3"))
        pygame.mixer.music.set_volume(0.5)  # Set background music volume
        pygame.mixer.music.play(-1)  # Loop the background music

        # Load and scale background image
        background_path = os.path.join(BASE_DIR, "assets", "images", "background.png")
        self.background_image = pygame.image.load(background_path).convert()
        self.background_image = pygame.transform.scale(self.background_image, (SCREEN_WIDTH, SCREEN_HEIGHT))

        # Spawn initial level elements
        self.spawn_level()

        # Initialize shooting cooldown
        self.shoot_cooldown = 0  # Cooldown timer for shooting

    def level_start_screen(self):
        # Displays the current level number at the start of a level
        self.screen.fill(BLACK)
        font = pygame.font.SysFont(None, 72)
        text = font.render(f"Level {self.level}", True, WHITE)
        self.screen.blit(text, (SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 - 50))
        pygame.display.flip()

        # Pause for a moment to display the level
        pygame.time.delay(2000)  # 2000 milliseconds = 2 seconds

    def spawn_level(self):
        # Spawns enemies and collectibles for the current level
        self.enemies.empty()
        self.collectibles.empty()

        # Set the level start timer (e.g., 60 frames for 2 seconds at 30 FPS)
        self.level_start_timer = 60

        # Enemy types and health scaling
        enemy_types = {1: "enemy1", 2: "enemy2", 3: "enemy3"}
        enemy_health = {1: 50, 2: 100, 3: 150}

        # Increase the number of enemies to make levels longer
        if self.level == 2:
            total_enemies = 4 * self.level  # Increased from 3 to 4
            num_enemy2 = (2 * total_enemies) // 3
            num_enemy3 = total_enemies - num_enemy2

            for _ in range(num_enemy2):
                enemy = Enemy(
                    random.randint(400, 700),
                    SCREEN_HEIGHT - 150,
                    health=enemy_health[2],
                    enemy_type=enemy_types[2]
                )
                self.enemies.add(enemy)
                self.all_sprites.add(enemy)

            for _ in range(num_enemy3):
                enemy = Enemy(
                    random.randint(400, 700),
                    SCREEN_HEIGHT - 150,
                    health=enemy_health[3],
                    enemy_type=enemy_types[3]
                )
                self.enemies.add(enemy)
                self.all_sprites.add(enemy)
        else:
            # Spawn more enemies for other levels
            for i in range(4 * self.level):  # Increased from 3 to 4
                enemy = Enemy(
                    random.randint(400, 700),
                    SCREEN_HEIGHT - 150,
                    health=enemy_health[self.level],
                    enemy_type=enemy_types[self.level]
                )
                self.enemies.add(enemy)
                self.all_sprites.add(enemy)

        # Spawn collectibles
        for i in range(2):
            kind = random.choice(['health', 'life'])
            # Place collectibles at a height where the player can only reach them by jumping
            y_position = random.randint(SCREEN_HEIGHT - 300, SCREEN_HEIGHT - 150)
            item = Collectible(random.randint(200, 700), y_position, kind)
            self.collectibles.add(item)
            self.all_sprites.add(item)

        # Reset player's position to the initial starting point
        self.player.rect.x = 100
        self.player.rect.y = SCREEN_HEIGHT - 240  # Initial vertical position

    def handle_events(self):
        # Handles user input events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:  # Jump sound
                    self.player.jump()
                    self.jump_sound.play()

        # Continuous shooting with cooldown
        keys = pygame.key.get_pressed()
        if keys[pygame.K_f] and self.shoot_cooldown == 0:
            proj = Projectile(self.player.rect.centerx, self.player.rect.centery, self.player.last_direction)
            self.projectiles.add(proj)
            self.all_sprites.add(proj)
            self.shoot_sound.play()
            self.shoot_cooldown = 5  # Set cooldown to 15 frames (adjust as needed)

        # Movement controls
        if keys[pygame.K_LEFT]:
            self.player.move("left")
        elif keys[pygame.K_RIGHT]:
            self.player.move("right")
        else:
            self.player.move("stop")

    def draw_health_bar(self, surface, x, y, health, max_health):
        # Draws the player's health bar
        BAR_WIDTH = 200
        BAR_HEIGHT = 20
        fill = (health / max_health) * BAR_WIDTH
        outline_rect = pygame.Rect(x, y, BAR_WIDTH, BAR_HEIGHT)
        fill_rect = pygame.Rect(x, y, fill, BAR_HEIGHT)
        pygame.draw.rect(surface, RED, outline_rect)
        pygame.draw.rect(surface, GREEN, fill_rect)
        pygame.draw.rect(surface, WHITE, outline_rect, 2)

    def update(self):
        # Updates all game elements and checks for game conditions
        self.all_sprites.update()

        # Decrease the level start timer
        if self.level_start_timer > 0:
            self.level_start_timer -= 1

        # Decrease the shoot cooldown
        if self.shoot_cooldown > 0:
            self.shoot_cooldown -= 1

        # Handle collisions between player's projectiles and enemies
        for proj in self.projectiles:
            if isinstance(proj, Projectile):
                hits = pygame.sprite.spritecollide(proj, self.enemies, False)
                for enemy in hits:
                    enemy.take_damage(proj.damage)
                    proj.kill()
                    self.player.score += 10
                    self.enemy_hit_sound.play()  # Play enemy hit sound

        collectible_hits = pygame.sprite.spritecollide(self.player, self.collectibles, False)
        for item in collectible_hits:
            item.apply_to_player(self.player)
            if item.kind == "life":
                self.extra_life_sound.play()  # Play extra life sound
            else:
                self.collectible_sound.play()  # Play health pickup sound

        enemy_hits = pygame.sprite.spritecollide(self.player, self.enemies, False)
        for enemy in enemy_hits:
            self.player.take_damage(3)  # Reduced damage from 5 to 3

        # Check if all enemies are defeated
        if not self.enemies:
            self.level += 1
            self.level_up_sound.play()  # Play level-up sound
            if self.level > 3:
                self.you_win_screen()
                return
            else:
                self.spawn_level()

        # Check if the player is out of lives
        if self.player.lives <= 0:
            self.running = False
            self.game_over_sound.play()  # Play game over sound

    def draw(self):
        # Draw the background image
        self.screen.blit(self.background_image, (0, 0))

        # Draw all sprites
        self.all_sprites.draw(self.screen)

        # Draw the health bar
        self.draw_health_bar(self.screen, 10, 10, self.player.health, 100)

        # Display score, lives, and level
        font = pygame.font.SysFont(None, 36)
        score_text = font.render(f"Score: {self.player.score}", True, WHITE)
        lives_text = font.render(f"Lives: {self.player.lives}", True, WHITE)
        level_text = font.render(f"Level: {self.level}", True, WHITE)

        self.screen.blit(score_text, (10, 40))
        self.screen.blit(lives_text, (10, 70))
        self.screen.blit(level_text, (10, 100)) 

        # Optionally, display the level number in the center of the screen
        if self.level_start_timer > 0:
            level_font = pygame.font.SysFont(None, 72)
            level_center_text = level_font.render(f"Level {self.level}", True, WHITE)
            self.screen.blit(level_center_text, (SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 - 50))

        pygame.display.flip()

    def game_over_screen(self):
        # Draw the background image
        self.screen.blit(self.background_image, (0, 0))
        font = pygame.font.SysFont(None, 72)
        text = font.render("Game Over", True, RED)
        self.screen.blit(text, (SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2 - 100))
        font_small = pygame.font.SysFont(None, 36)
        restart_text = font_small.render("Press R to Restart or Q to Quit", True, WHITE)
        self.screen.blit(restart_text, (SCREEN_WIDTH // 2 - 180, SCREEN_HEIGHT // 2))
        pygame.display.flip()

        self.game_over_sound.play()  # Play game over sound

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
        # Draw the background image
        self.screen.blit(self.background_image, (0, 0))
        font = pygame.font.SysFont(None, 72)
        text = font.render("You Win!", True, GREEN)
        self.screen.blit(text, (SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2 - 100))
        font_small = pygame.font.SysFont(None, 36)
        restart_text = font_small.render("Press R to Restart or Q to Quit", True, WHITE)
        self.screen.blit(restart_text, (SCREEN_WIDTH // 2 - 180, SCREEN_HEIGHT // 2))
        pygame.display.flip()

        self.level_up_sound.play()  # Play win sound

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
        # Main game loop
        while self.running:
            self.clock.tick(FPS)
            self.handle_events()
            self.update()
            self.draw()
        self.game_over_screen()


if __name__ == "__main__":
    # Create a game instance and start the game loop
    game = Game()
    game.run()
    pygame.quit()  

