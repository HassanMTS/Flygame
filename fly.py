# Import necessary libraries and modules
import pygame
from pygame.locals import *
import random
import sys

# Initialize Pygame
pygame.init()

# Game settings
clock = pygame.time.Clock()  # Create a clock object to control the frame rate
fps = 60  # Set the desired frames per second
screen_width = 864
screen_height = 936
screen = pygame.display.set_mode((screen_width, screen_height))  # Create the game window
pygame.display.set_caption('Flight')  # Set the window caption

# Fonts and colors
font = pygame.font.SysFont('Bauhaus 93', 60)  # Set the main font for larger text
small_font = pygame.font.SysFont('Bauhaus 93', 30)  # Set a smaller font for certain text
white = (255, 255, 255)  # Define a white color

alt_bg = pygame.image.load('img/alternate_bg.png')  # Load the alternative background image
alt_pipe_img = pygame.image.load('img/alternate_pipe.png')  # Load the alternative pipe image
alt_music = 'sound/alternate_music.mp3'  # Set the alternative background music file
pipe_img = pygame.image.load('img/pipe.png')  # Load the default pipe image

# Game variables
ground_scroll = 0
scroll_speed = 4
flying = False
game_over = False
pipe_gap = 150
pipe_frequency = 1500
last_pipe = pygame.time.get_ticks() - pipe_frequency
score = 0
high_score = 0
pass_pipe = False
collision_sound_played = False
restart_clicks = 0

# Load images and initialize mixer
bg = pygame.image.load('img/bg.png')  # Load the background image
ground_img = pygame.image.load('img/ground.png')  # Load the ground image
pygame.mixer.init()  # Initialize the sound mixer
point_sound = pygame.mixer.Sound('sound/sound.wav')  # Load the point sound effect
point_sound.set_volume(0.5)  # Set the volume level for the point sound
pygame.mixer.music.load('sound/background_music.mp3')  # Load the background music
pygame.mixer.music.set_volume(0.3)  # Set the volume level for the background music
pygame.mixer.music.play(-1)  # Play the background music continuously
collision_sound = pygame.mixer.Sound('sound/collision.wav')  # Load the collision sound effect
collision_sound.set_volume(0.5)  # Set the volume level for the collision sound

# Function to draw text on the screen
def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    screen.blit(img, (x, y))

# Function to reset the game state
def reset_game():
    global score, game_over, collision_sound_played, high_score, restart_clicks, flying
    pipe_group.empty()
    flappy.rect.x = 100
    flappy.rect.y = int(screen_height / 2)
    game_over = False
    collision_sound_played = False
    flying = False
    if score > high_score:
        high_score = score
    score = 0
    restart_clicks += 1
    return score

def customization_menu():
    global bg, pipe_img, alt_bg, alt_pipe_img, alt_music
    background_options = [bg, alt_bg]
    pipe_options = [pipe_img, alt_pipe_img]
    music_options = [pygame.mixer.music.get_busy(), alt_music]

    bg_index = (background_options.index(bg) + 1) % len(background_options)
    pipe_index = (pipe_options.index(pipe_img) + 1) % len(pipe_options)
    music_index = (music_options.index(pygame.mixer.music.get_busy()) + 1) % len(music_options)

    bg = background_options[bg_index]
    pipe_img = pipe_options[pipe_index]
    if pygame.mixer.music.get_busy():
        pygame.mixer.music.stop()
        pygame.mixer.music.load(music_options[music_index])
        pygame.mixer.music.play(-1)

    # Redraw the screen with new options
    screen.blit(bg, (0, 0))
    pipe_group.draw(screen)
    screen.blit(ground_img, (ground_scroll, 768))
    draw_text(f"Score: {score}", font, white, int(screen_width / 2) - 150, 20)

    pygame.display.update()
    pygame.time.delay(1000)  # Add a delay to visually confirm the changes

class Bird(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.images = [pygame.image.load(f'img/bird{num}.png') for num in range(1, 4)]  # Load bird animation frames
        self.index = 0
        self.counter = 0
        self.image = self.images[self.index]
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]
        self.vel = 0
        self.clicked = False
        self.clicked_sound = pygame.mixer.Sound('sound/up.wav')  # Load the click sound
        self.clicked_sound.set_volume(0.5)  # Set the volume level for the click sound

    def update(self):
        global score, game_over, collision_sound_played, high_score, flying
        if flying:
            self.vel += 0.5
            if self.vel > 8:
                self.vel = 8
            if self.rect.bottom < 768:
                self.rect.y += int(self.vel)

        if not game_over:
            if pygame.mouse.get_pressed()[0] == 1 and not self.clicked:
                self.clicked = True
                self.vel = -10
                self.clicked_sound.play()
            if pygame.mouse.get_pressed()[0] == 0:
                self.clicked = False

            # Draw "hassanmts" button
            customize_group.draw(screen)

            self.counter += 1
            flap_cooldown = 5

            if self.counter > flap_cooldown:
                self.counter = 0
                self.index += 1
                if self.index >= len(self.images):
                    self.index = 0
            self.image = pygame.transform.rotate(self.images[self.index], self.vel * -2)
        else:
            self.image = pygame.transform.rotate(self.images[self.index], -90)

class Pipe(pygame.sprite.Sprite):
    def __init__(self, x, y, position):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('img/pipe.png')  # Load the pipe image
        self.rect = self.image.get_rect()
        if position == 1:
            self.image = pygame.transform.flip(self.image, False, True)
            self.rect.bottomleft = [x, y - int(pipe_gap / 2)]
        if position == -1:
            self.rect.topleft = [x, y + int(pipe_gap / 2)]

    def update(self):
        global game_over, collision_sound_played
        self.rect.x -= scroll_speed
        if self.rect.right < 0:
            self.kill()
        if pygame.sprite.spritecollide(flappy, pipe_group, False) and not collision_sound_played:
            collision_sound.play()
            collision_sound_played = True
            game_over = True

class Button(pygame.sprite.Sprite):
    def __init__(self, x, y, image, callback=None):
        pygame.sprite.Sprite.__init__(self)
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.callback = callback

    def draw(self, surface):
        mouse_pos = pygame.mouse.get_pos()

        if self.rect.collidepoint(mouse_pos):
            if pygame.mouse.get_pressed()[0]:  # Check for button down
                if self.callback:
                    self.callback()
                return True

        surface.blit(self.image, (self.rect.x, self.rect.y))
        return False

# New sprite groups
bird_group = pygame.sprite.Group()
pipe_group = pygame.sprite.Group()
customize_group = pygame.sprite.Group()
button_group = pygame.sprite.Group()

# Initialize bird and button
flappy = Bird(100, int(screen_height / 2))
bird_group.add(flappy)
button_img = pygame.image.load('img/restart.png')
button = Button(screen_width // 2 - 50, screen_height // 2 - 100, button_img, reset_game)
button_group.add(button)

# Initialize "hassanmts" button
hassanmts_img = pygame.image.load('img/hassanmts.png')
hassanmts_button = Button(20, screen_height - 70, hassanmts_img, customization_menu)
customize_group.add(hassanmts_button)

# Main game loop
run = True
while run:
    clock.tick(fps)

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if not flying and not game_over:
                # Make the bird fly on mouse click
                flappy.vel = -10
                flappy.clicked_sound.play()
                flying = True  # Start the game when the user clicks the mouse
            elif game_over:
                # Check if the restart button is clicked
                if button.draw(screen):
                    score = reset_game()

    # Update game elements
    if not game_over:
        bird_group.update()
        pipe_group.update()

        # Check for collisions and score
        if len(pipe_group) > 0:
            if (
                bird_group.sprites()[0].rect.left > pipe_group.sprites()[0].rect.left
                and bird_group.sprites()[0].rect.right < pipe_group.sprites()[0].rect.right
                and not pass_pipe
            ):
                pass_pipe = True
            if (
                pass_pipe
                and bird_group.sprites()[0].rect.left > pipe_group.sprites()[0].rect.right
            ):
                score += 1
                pass_pipe = False
                point_sound.play()

        if pygame.sprite.groupcollide(
            bird_group, pipe_group, False, False
        ) and not collision_sound_played:
            collision_sound.play()
            collision_sound_played = True
            game_over = True

        if flappy.rect.top < 0 or flappy.rect.bottom >= 768:
            game_over = True
            flying = False

        # Generate pipes
        time_now = pygame.time.get_ticks()
        if time_now - last_pipe > pipe_frequency:
            pipe_height = random.randint(-100, 100)
            btm_pipe = Pipe(screen_width, int(screen_height / 2) + pipe_height, -1)
            top_pipe = Pipe(screen_width, int(screen_height / 2) + pipe_height, 1)
            pipe_group.add(btm_pipe)
            pipe_group.add(top_pipe)
            last_pipe = time_now

        ground_scroll -= scroll_speed
        if abs(ground_scroll) > 35:
            ground_scroll = 0

    # Drawing
    screen.blit(bg, (0, 0))
    pipe_group.draw(screen)
    bird_group.draw(screen)
    screen.blit(ground_img, (ground_scroll, 768))

    # Draw "hassanmts" button
    customize_group.draw(screen)

    # Draw text and update display
    draw_text(f"Times Restarted: {restart_clicks}", small_font, white, 20, 20)
    draw_text(f"Score: {score}", font, white, int(screen_width / 2) - 150, 20)
    draw_text(f"High Score: {high_score}", small_font, white, screen_width - 250, 20)
    constant_text = "Made by HassanMTS on Github"
    draw_text(constant_text, small_font, (0, 0, 0), int(screen_width / 2), screen_height - 30)

    # Update the display
    pygame.display.update()

# Quit the game
pygame.quit()
sys.exit()
