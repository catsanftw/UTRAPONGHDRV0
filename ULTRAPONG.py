import pygame
from array import array
import random

# Initialize Pygame and its mixer
pygame.init()
pygame.mixer.init(frequency=22050, size=-16, channels=2, buffer=512)

# Screen setup - fixed size window
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Breakout [C] MEOW LLC 20XX  ")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

# Game objects
paddle_width, paddle_height = 100, 10
paddle = pygame.Rect(SCREEN_WIDTH // 2 - paddle_width // 2, SCREEN_HEIGHT - 50, paddle_width, paddle_height)

ball_size = 10
ball = pygame.Rect(SCREEN_WIDTH // 2 - ball_size // 2, SCREEN_HEIGHT // 2 - ball_size // 2, ball_size, ball_size)
ball_speed_x, ball_speed_y = 5, -5

brick_width, brick_height = 80, 30
bricks = [pygame.Rect(col * (brick_width + 5), row * (brick_height + 5), brick_width, brick_height) 
          for row in range(5) for col in range(SCREEN_WIDTH // (brick_width + 5))]

# Define a function to generate beep sounds with varying frequencies
def generate_beep_sound(frequency=440, duration=0.1):
    sample_rate = pygame.mixer.get_init()[0]
    max_amplitude = 2 ** (abs(pygame.mixer.get_init()[1]) - 1) - 1
    samples = int(sample_rate * duration)
    wave = [int(max_amplitude * ((i // (sample_rate // frequency)) % 2)) for i in range(samples)]
    sound = pygame.mixer.Sound(buffer=array('h', wave))
    sound.set_volume(0.1)
    return sound

# Create a list of sound tuples (name, sound object)
sounds = [
    ("SND_1", generate_beep_sound(440, 0.1)),  # A4
    ("SND_2", generate_beep_sound(523.25, 0.1)),  # C5
    ("SND_3", generate_beep_sound(587.33, 0.1)),  # D5
    ("SND_4", generate_beep_sound(659.25, 0.1)),  # E5
]

# Font setup
font = pygame.font.Font(None, 36)

def draw_text(text, font, color, surface, x, y):
    textobj = font.render(text, 1, color)
    textrect = textobj.get_rect()
    textrect.topleft = (x, y)
    surface.blit(textobj, textrect)

def main_menu():
    while True:
        screen.fill(BLACK)
        draw_text('Main Menu', font, WHITE, screen, 20, 20)

        mx, my = pygame.mouse.get_pos()

        button_1 = pygame.Rect(SCREEN_WIDTH // 2 - 100, 100, 200, 50)
        button_2 = pygame.Rect(SCREEN_WIDTH // 2 - 100, 200, 200, 50)
        
        if button_1.collidepoint((mx, my)):
            if click:
                game()
        if button_2.collidepoint((mx, my)):
            if click:
                return
        
        pygame.draw.rect(screen, WHITE, button_1)
        pygame.draw.rect(screen, WHITE, button_2)
        
        draw_text('Play', font, BLACK, screen, SCREEN_WIDTH // 2 - 30, 115)
        draw_text('Quit', font, BLACK, screen, SCREEN_WIDTH // 2 - 30, 215)

        click = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True

        pygame.display.update()
        clock.tick(60)

def game():
    global paddle, ball, ball_speed_x, ball_speed_y, bricks

    # Reset game objects
    paddle = pygame.Rect(SCREEN_WIDTH // 2 - paddle_width // 2, SCREEN_HEIGHT - 50, paddle_width, paddle_height)
    ball = pygame.Rect(SCREEN_WIDTH // 2 - ball_size // 2, SCREEN_HEIGHT // 2 - ball_size // 2, ball_size, ball_size)
    ball_speed_x, ball_speed_y = 5, -5
    bricks = [pygame.Rect(col * (brick_width + 5), row * (brick_height + 5), brick_width, brick_height) 
              for row in range(5) for col in range(SCREEN_WIDTH // (brick_width + 5))]

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return

        # Move paddle
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and paddle.left > 0:
            paddle.x -= 7
        if keys[pygame.K_RIGHT] and paddle.right < SCREEN_WIDTH:
            paddle.x += 7

        # Move ball
        ball.x += ball_speed_x
        ball.y += ball_speed_y

        # Ball collision with walls
        if ball.left <= 0 or ball.right >= SCREEN_WIDTH:
            ball_speed_x = -ball_speed_x
            sounds[2][1].play()  # SND_3 for wall hit
        if ball.top <= 0:
            ball_speed_y = -ball_speed_y
            sounds[2][1].play()  # SND_3 for wall hit

        # Ball collision with paddle
        if ball.colliderect(paddle) and ball_speed_y > 0:
            ball_speed_y = -ball_speed_y
            sounds[0][1].play()  # SND_1 for paddle hit

        # Ball collision with bricks
        for brick in bricks[:]:
            if ball.colliderect(brick):
                bricks.remove(brick)
                ball_speed_y = -ball_speed_y
                sounds[1][1].play()  # SND_2 for brick hit
                break

        # Game over condition
        if ball.bottom >= SCREEN_HEIGHT:
            sounds[3][1].play()  # SND_4 for game over
            return

        # Clear screen
        screen.fill(BLACK)

        # Draw game objects
        pygame.draw.rect(screen, WHITE, paddle)
        pygame.draw.rect(screen, WHITE, ball)
        for brick in bricks:
            pygame.draw.rect(screen, RED, brick)

        # Update display
        pygame.display.flip()

        # Cap the frame rate
        clock.tick(60)

# Main game loop
clock = pygame.time.Clock()
main_menu()

pygame.quit()
