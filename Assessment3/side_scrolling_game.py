# import pygame to create 2D game
import pygame

# initialize Pygame
pygame.init()

# draw screen with dimension 800 by 600
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Side Scrolling Game")


# define a class called Player to handle player movement and jumping
class Player:
    def __init__(self, x, y, image_path):
        # load character image and if not found throw error and exit the program
        try:
            self.image = pygame.image.load(image_path)
            self.image = pygame.transform.scale(self.image, (100, 100))  # resize image to 100x100
        except pygame.error as e:
            print(f"Error loading image: {e}")
            pygame.quit()
            raise SystemExit

        # set initial player position and movement-related variables
        self.x = x
        self.y = y
        self.y_vel = 0  # vertical velocity
        self.jumping = False  # whether the character is in the air
        self.gravity = 0.5  # gravity force pulling character down
        self.jump_strength = -10  # force of upward movement when jumping
        self.ground_y = y  # the y-coordinate representing the ground

    # check for key press to trigger jump
    def handle_input(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and not self.jumping:
                self.y_vel = self.jump_strength  # apply upward velocity
                self.jumping = True  # character is now in air

    # update character's vertical position each frame
    def update(self):
        self.y_vel += self.gravity  # apply gravity to vertical velocity
        self.y += self.y_vel  # move character vertically

        # stop falling when character lands back on ground
        if self.y >= self.ground_y:
            self.y = self.ground_y
            self.y_vel = 0
            self.jumping = False  # allow jumping again

    # draw character image on the screen
    def draw(self, surface):
        surface.blit(self.image, (self.x, self.y))


# create a player object at position (15, 497) with image file
player = Player(15, 497, "shooting-game.png")

# keep the screen awake until the user quits
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False  # exit game loop when window is closed
        player.handle_input(event)  # check for jump input

    # apply movement logic (e.g., gravity and jumping)
    player.update()

    # fill background with light blue color (RGB)
    screen.fill((135, 206, 235))  # Light sky blue background

    # draw character image at the current position
    player.draw(screen)

    # show the update on the display
    pygame.display.flip()

# quit Pygame successfully
pygame.quit()
