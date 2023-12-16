import pygame
from pygame.locals import *
import random

pygame.init()

clock = pygame.time.Clock()
fps = 60

screen_width = 864
screen_height = 936

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Flappy Bird')

# define font
font = pygame.font.SysFont('Bauhaus 93', 60)
small_font = pygame.font.SysFont('Bauhaus 93', 30)  # Added a smaller font for high score

# define colours
white = (255, 255, 255)

# define game variables
ground_scroll = 0
scroll_speed = 4
flying = False
game_over = False
pipe_gap = 150
pipe_frequency = 1500  # milliseconds
last_pipe = pygame.time.get_ticks() - pipe_frequency
score = 0
high_score = 0  # Added high score variable
pass_pipe = False
collision_sound_played = False
restart_clicks = 0  # Added restart clicks counter
player_name = ""  # Player's name

# load images
bg = pygame.image.load('img/bg.png')
ground_img = pygame.image.load('img/ground.png')
button_img = pygame.image.load('img/restart.png')

# Initialize mixer
pygame.mixer.init()

# Load sound
point_sound = pygame.mixer.Sound('sound/sound.wav')
point_sound.set_volume(0.5)  # Adjust the volume level (0.5 means half volume)

# Load background music
pygame.mixer.music.load('sound/background_music.mp3')
pygame.mixer.music.set_volume(0.3)  # Adjust the volume level (0.3 means 30% volume)
pygame.mixer.music.play(-1)  # -1 means play continuously

# Load sound for collision
collision_sound = pygame.mixer.Sound('sound/collision.wav')
collision_sound.set_volume(0.5)  # Adjust the volume level (0.5 means half volume)

def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    screen.blit(img, (x, y))

def reset_game():
    global score, game_over, collision_sound_played, high_score, restart_clicks, player_name
    pipe_group.empty()
    flappy.rect.x = 100
    flappy.rect.y = int(screen_height / 2)
    game_over = False
    collision_sound_played = False
    if score > high_score:
        high_score = score  # Update high score
    score = 0  # Move the score reset after updating high score
    restart_clicks += 1  # Increment restart clicks
    return score

class Bird(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.images = []
        self.index = 0
        self.counter = 0
        for num in range(1, 4):
            img = pygame.image.load(f'img/bird{num}.png')
            self.images.append(img)
        self.image = self.images[self.index]
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]
        self.vel = 0
        self.clicked = False
        self.clicked_sound = pygame.mixer.Sound('sound/up.wav')
        self.clicked_sound.set_volume(0.5)

    def update(self):
        global score, game_over, collision_sound_played, high_score
        if flying == True:
            self.vel += 0.5
            if self.vel > 8:
                self.vel = 8
            if self.rect.bottom < 768:
                self.rect.y += int(self.vel)

        if game_over == False:
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                self.clicked = True
                self.vel = -10
                self.clicked_sound.play()  # Play click sound when flying
            if pygame.mouse.get_pressed()[0] == 0:
                self.clicked = False

            self.counter += 1
            flap_cooldown = 5

            if self.counter > flap_cooldown:
                self.counter = 0
                self.index += 1
                if self.index >= len(self.images):
                    self.index = 0
            self.image = self.images[self.index]

            self.image = pygame.transform.rotate(self.images[self.index], self.vel * -2)
        else:
            self.image = pygame.transform.rotate(self.images[self.index], -90)

class Pipe(pygame.sprite.Sprite):
    def __init__(self, x, y, position):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('img/pipe.png')
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
        # Check for collision with the bird
        if pygame.sprite.spritecollide(flappy, pipe_group, False) and not collision_sound_played:
            collision_sound.play()
            collision_sound_played = True
            game_over = True

class Button():
    def __init__(self, x, y, image):
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

    def draw(self):
        action = False
        pos = pygame.mouse.get_pos()

        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1:
                action = True

        screen.blit(self.image, (self.rect.x, self.rect.y))

        return action

def get_input():
    global player_name
    input_box = pygame.Rect(20, 20, 140, 32)
    color_inactive = pygame.Color('lightskyblue3')
    color_active = pygame.Color('dodgerblue2')
    color = color_inactive
    active = False
    text = ''
    font = pygame.font.Font(None, 32)
    clock = pygame.time.Clock()
    input_active = True

    while input_active:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if input_box.collidepoint(event.pos):
                    active = not active
                else:
                    active = False
                color = color_active if active else color_inactive
            if event.type == pygame.KEYDOWN:
                if active:
                    if event.key == pygame.K_RETURN:
                        player_name = text
                        input_active = False
                    elif event.key == pygame.K_BACKSPACE:
                        text = text[:-1]
                    else:
                        text += event.unicode

        screen.fill((30, 30, 30))
        txt_surface = font.render(text, True, color)
        width = max(200, txt_surface.get_width()+10)
        input_box.w = width
        screen.blit(txt_surface, (input_box.x+5, input_box.y+5))
        pygame.draw.rect(screen, color, input_box, 2)
        pygame.display.flip()
        clock.tick(30)

# Get player name before starting the game
get_input()

bird_group = pygame.sprite.Group()
pipe_group = pygame.sprite.Group()

flappy = Bird(100, int(screen_height / 2))
bird_group.add(flappy)

button = Button(screen_width // 2 - 50, screen_height // 2 - 100, button_img)

run = True
while run:
    clock.tick(fps)
    screen.blit(bg, (0, 0))

    bird_group.draw(screen)
    bird_group.update()
    pipe_group.draw(screen)

    screen.blit(ground_img, (ground_scroll, 768))

    if len(pipe_group) > 0:
        if bird_group.sprites()[0].rect.left > pipe_group.sprites()[0].rect.left \
                and bird_group.sprites()[0].rect.right < pipe_group.sprites()[0].rect.right \
                and not pass_pipe:
            pass_pipe = True
        if pass_pipe and bird_group.sprites()[0].rect.left > pipe_group.sprites()[0].rect.right:
            score += 1
            pass_pipe = False
            point_sound.play()

    # Check for collision with pipes
    if pygame.sprite.groupcollide(bird_group, pipe_group, False, False) and not collision_sound_played:
        collision_sound.play()
        collision_sound_played = True
        game_over = True

    if flappy.rect.top < 0:
        game_over = True

    if flappy.rect.bottom >= 768:
        game_over = True
        flying = False

    if game_over == False and flying == True:
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

        pipe_group.update()

    # Draw player name and restart clicks
    draw_text(f"Restart Clicks: {restart_clicks}", small_font, white, 20, 60)
    draw_text(f"Player: {player_name}", small_font, white, 20, 100)
    if game_over == True:
        if button.draw() == True:
            score = reset_game()
            draw_text(f"High Score: {high_score}", small_font, white, screen_width - 250, 20)

    draw_text(f"Score: {score}", font, white, int(screen_width / 2) - 150, 20)
    draw_text(f"High Score: {high_score}", small_font, white, screen_width - 250, 20)

    pygame.display.update()

pygame.quit()
