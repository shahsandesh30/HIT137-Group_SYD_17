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
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("shooting-game.png").convert_alpha()  # Load the image
        self.image = pygame.transform.scale(self.image, (100, 100))     # Resize image
        self.rect = self.image.get_rect()
        self.rect.x = 100
        self.rect.y = SCREEN_HEIGHT - 100

        self.speed_x = 0
        self.speed_y = 0
        self.jump_speed = -15
        self.gravity = 0.8
        self.is_jumping = False

        self.health = 0  # start with empty health bar
        self.max_health = 100

        self.lives = 3
        self.move_speed = 5
        self.score = 0

    def move(self, direction):
        if direction == "left":
            self.speed_x = -self.move_speed
        elif direction == "right":
            self.speed_x = self.move_speed
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

# Projectile Class
class Projectile(pygame.sprite.Sprite):
    def __init__(self, x, y, speed=10, damage=25):
        super().__init__()
        self.image = pygame.Surface([10, 5])
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = speed
        self.damage = damage

    def set_speed(self, new_speed):
        self.speed = new_speed

    def get_speed(self):
        return self.speed

    def get_damage(self):
        return self.damage

    def move(self):
        self.rect.x += self.speed
        if self.rect.right > SCREEN_WIDTH:
            self.kill()

    def update(self):
        self.move()


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

    def spawn_level(self):
        self.enemies.empty()
        self.collectibles.empty()
        if self.level == 3:
            boss = Enemy(600, SCREEN_HEIGHT - 80, health=150)
            self.enemies.add(boss)
            self.all_sprites.add(boss)
        else:
            for i in range(3 * self.level):
                enemy = Enemy(random.randint(400, 700), SCREEN_HEIGHT - 80)
                self.enemies.add(enemy)
                self.all_sprites.add(enemy)

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
                if event.key == pygame.K_SPACE:
                    self.player.jump()
                if event.key == pygame.K_f:
                    proj = Projectile(self.player.rect.centerx, self.player.rect.centery)
                    self.projectiles.add(proj)
                    self.all_sprites.add(proj)

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.player.move("left")
        elif keys[pygame.K_RIGHT]:
            self.player.move("right")
        else:
            self.player.move("stop")

    def draw_health_bar(self, surface, x, y, current_health, max_health):
        bar_width = 100
        bar_height = 10
        fill = (current_health / max_health) * bar_width
        outline_rect = pygame.Rect(x, y, bar_width, bar_height)
        fill_rect = pygame.Rect(x, y, fill, bar_height)
        pygame.draw.rect(surface, (0, 255, 0), fill_rect)
        pygame.draw.rect(surface, (255, 255, 255), outline_rect, 2)



    def update(self):
        self.all_sprites.update()

        for proj in self.projectiles:
            hits = pygame.sprite.spritecollide(proj, self.enemies, False)
            for enemy in hits:
                enemy.take_damage(proj.get_damage())
                proj.kill()

                self.player.score += 10
                self.player.health = min(self.player.max_health, self.player.health + 10)

        collectible_hits = pygame.sprite.spritecollide(self.player, self.collectibles, False)
        for item in collectible_hits:
            item.apply_to_player(self.player)

        if not self.enemies:
            self.level += 1
            if self.level > 3:
                self.running = False
            else:
                self.spawn_level()

        if self.player.lives <= 0:
            self.running = False


    def draw(self):
        self.screen.fill(BLACK)
        self.all_sprites.draw(self.screen)
        self.draw_health_bar(self.screen, 10, 10, self.player.health, 100)
        font = pygame.font.SysFont(None, 36)
        score_text = font.render(f"Score: {self.player.score}", True, WHITE)
        lives_text = font.render(f"Lives: {self.player.lives}", True, WHITE)
        level_text = font.render(f"Level: {self.level}", True, WHITE)
        self.screen.blit(score_text, (10, 40))
        self.screen.blit(lives_text, (10, 70))
        self.screen.blit(level_text, (10, 100))
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
