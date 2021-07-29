import sys
import time

import pygame
import random

FPS = 10
FPS_Clock = pygame.time.Clock()

window_width = 640
window_length = 480
cell_size = 20
pygame.init()
display = pygame.display.set_mode((window_width, window_length))
pygame.display.set_caption("Snake")

up = 'up'
down = 'down'
left = 'left'
right = 'right'
# position of the snake head
SNAKE_HEAD = 0

black = (0, 0, 0)
white = (255, 255, 255)
blue = (0, 0, 255)
red = (255, 0, 0)


def draw_snake(snake_body):
    for body in snake_body:
        x = body['x'] * cell_size
        y = body['y'] * cell_size
        pygame.draw.rect(display, blue, (x, y, cell_size, cell_size))


def draw_fruit(fruit):
    x = fruit['x'] * cell_size
    y = fruit['y'] * cell_size
    pygame.draw.rect(display, red, (x, y, cell_size, cell_size))


def draw_grid():
    for i in range(int(window_width / cell_size)):
        # the below if removes the line that's drawn on the left side
        if i != 0:
            pygame.draw.line(display, white, (i * cell_size, 0), (i * cell_size, window_length))
    for i in range(int(window_length / cell_size)):
        if i != 0:
            pygame.draw.line(display, white, (0, i * cell_size), (window_width, i * cell_size))


def game_over_message():
    you_died_text = pygame.font.Font(None, 30).render("you died", False, red)
    play_again_text = pygame.font.Font(None, 30).render("Press p to play again", False, red)
    display.blit(you_died_text, (window_length / 2 + 20, window_length / 2))
    display.blit(play_again_text, (window_length / 2 - 30, window_length / 2 + 30))
    pygame.display.update()


def game_loop():
    run = True
    game_over = False
    direction = right
    #time.sleep(2)
    start_x = random.randint(5, cell_size - 5)
    start_y = random.randint(5, cell_size - 5)
    snake_body = [
        {'x': start_x, 'y': start_y},
        {'x': start_x - 1, 'y': start_y},
        {'x': start_x - 2, 'y': start_y}
    ]

    # draw snake

    fruit = {'x': random.randint(0, cell_size - 1), 'y': random.randint(0, cell_size - 1)}

    while run:

        while game_over:
            game_over_message()
            pygame.display.update()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_p:
                        game_over = False
                        game_loop()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and direction != down:
                    direction = up
                elif event.key == pygame.K_DOWN and direction != up:
                    direction = down
                elif event.key == pygame.K_RIGHT and direction != left:
                    direction = right
                elif event.key == pygame.K_LEFT and direction != right:
                    direction = left
                elif event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    run = False

        # check if the snake hits the edge
        # window_width / cell size because when the snake is drawn, its x and y value has been
        # multiplied by cell_size to match the length of each cells
        if snake_body[0]['x'] == -1 or snake_body[0]['x'] == window_width / cell_size\
                or snake_body[0]['y'] == -1 or snake_body[0]['y'] == window_length / cell_size:
            # game over
            game_over = True
        # check if the snake hits itself:
        # snake_body[1:] tells python to skip the first element in the list
        for body in snake_body[1:]:
            if snake_body[0]['x'] == body['x'] and snake_body[0]['y'] == body['y']:
                game_over = True

        # check if fruit is eaten, if eaten, simply generate a new fruit, the snake becomes longer by not dropping
        # the last x and y entry in the snake_body dictionary
        # if fruit is not eaten then delete the last entry of the dictionary
        if fruit['x'] == snake_body[0]['x'] and fruit['y'] == snake_body[0]['y']:
            fruit = {'x': random.randint(0, cell_size - 1), 'y': random.randint(0, cell_size - 1)}
        else:
            del snake_body[-1]

        # inserting a new head to the snake and if no fruit eaten, the tail will be dropped from the list
        # so that it looks like the snake is moving
        if direction == up:
            new_head = {'x': snake_body[0]['x'], 'y': snake_body[0]['y'] - 1}
        elif direction == down:
            new_head = {'x': snake_body[0]['x'], 'y': snake_body[0]['y'] + 1}
        elif direction == left:
            new_head = {'x': snake_body[0]['x'] - 1, 'y': snake_body[0]['y']}
        elif direction == right:
            new_head = {'x': snake_body[0]['x'] + 1, 'y': snake_body[0]['y']}

        snake_body.insert(0, new_head)
        display.fill(black)
        draw_snake(snake_body)
        draw_fruit(fruit)
        #draw_grid()
        pygame.display.update()
        FPS_Clock.tick(FPS)


game_loop()
pygame.quit()
