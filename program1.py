import pygame
import time
import random

# Initialize pygame
pygame.init()

# Screen dimensions and block size
WIDTH, HEIGHT = 600, 400
BLOCK_SIZE = 20
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake Game")
clock = pygame.time.Clock()

# Define colors and font
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLACK = (0, 0, 0)
font = pygame.font.SysFont("Arial", 25)

# Function to draw snake
def draw_snake(snake_list):
    for block in snake_list:
        pygame.draw.rect(screen, GREEN, [block[0], block[1], BLOCK_SIZE, BLOCK_SIZE])

# Function to generate food at a random position
def generate_food():
    return [random.randrange(0, WIDTH - BLOCK_SIZE, BLOCK_SIZE),
            random.randrange(0, HEIGHT - BLOCK_SIZE, BLOCK_SIZE)]

# Function to display messages
def message(msg, color):
    text = font.render(msg, True, color)
    screen.blit(text, [WIDTH / 3, HEIGHT / 3])

# Function to read high score from file
def read_high_score():
    try:
        with open("highscore.txt", "r") as file:
            return int(file.read())
    except:
        return 0

# Function to update high score in file
def write_high_score(score):
    with open("highscore.txt", "w") as file:
        file.write(str(score))

# Main game loop
def game_loop():
    game_over = False
    game_close = False

    x, y = WIDTH // 2, HEIGHT // 2
    x_change, y_change = 0, 0

    snake_list = []
    length = 1

    food = generate_food()

    # Read high score
    high_score = read_high_score()

    while not game_over:

        while game_close:
            screen.fill(BLACK)
            message("Game Over! Press Q-Quit or R-Restart", RED)

            # Display high score
            high_score_msg = font.render(f"High Score: {high_score}", True, WHITE)
            screen.blit(high_score_msg, [WIDTH / 3, HEIGHT / 2 + 30])

            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        game_over = True
                        game_close = False
                    if event.key == pygame.K_r:
                        game_loop()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    x_change = -BLOCK_SIZE
                    y_change = 0
                elif event.key == pygame.K_RIGHT:
                    x_change = BLOCK_SIZE
                    y_change = 0
                elif event.key == pygame.K_UP:
                    y_change = -BLOCK_SIZE
                    x_change = 0
                elif event.key == pygame.K_DOWN:
                    y_change = BLOCK_SIZE
                    x_change = 0
                elif event.key == pygame.K_p:  # Pause functionality
                    game_close = True
                    while game_close:
                        for event in pygame.event.get():
                            if event.type == pygame.QUIT:
                                game_over = True
                                game_close = False
                            if event.type == pygame.KEYDOWN and event.key == pygame.K_p:
                                game_close = False

        x += x_change
        y += y_change

        if x < 0 or x >= WIDTH or y < 0 or y >= HEIGHT:
            game_close = True

        screen.fill(BLACK)
        pygame.draw.rect(screen, RED, [food[0], food[1], BLOCK_SIZE, BLOCK_SIZE])

        snake_head = [x, y]
        snake_list.append(snake_head)
        if len(snake_list) > length:
            del snake_list[0]

        for block in snake_list[:-1]:
            if block == snake_head:
                game_close = True

        draw_snake(snake_list)

        score = font.render("Score: " + str(length - 1), True, WHITE)
        screen.blit(score, [0, 0])

        pygame.display.update()

        if x == food[0] and y == food[1]:
            food = generate_food()
            length += 1

        # Increase speed as the snake grows
        speed = 10 + (length // 5)
        clock.tick(speed)

        # Update high score if necessary
        if length - 1 > high_score:
            high_score = length - 1
            write_high_score(high_score)

    pygame.quit()
    quit()

# Start the game
game_loop()
