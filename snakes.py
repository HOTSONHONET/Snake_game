import pygame as pg
import random
from sys import exit

# Intializing of pygame and audio
pg.mixer.init()
pg.init()

# Colors
white = (255, 255, 255)
Blue = (0, 0, 255)
Red = (255, 0, 0)
green = (0, 255, 0)
black = (0, 0, 0)
head_color = (0, 255, 255)
hs_color = (120, 50, 39)

# Initial Display
pg.display.set_caption('SNAKES')
width = 1200
height = 600
game_window = pg.display.set_mode((width, height))
pg.display.update()

# Instantiating variables
clock = pg.time.Clock()
font = pg.font.SysFont(None, 45)


# Loading Image
opening_img = pg.image.load("images/opening.jpg")
bg_img = pg.image.load('images/jungle.jpg')
opening_img = pg.transform.scale(opening_img, (width, height)).convert_alpha()
bg_img = pg.transform.scale(bg_img, (width, height)).convert_alpha()

# opening music
pg.mixer.music.load("music/Nagin.mp3")
pg.mixer.music.play()


def screen_text(text, color, x, y):
    text_screen = font.render(text, True, color)
    game_window.blit(text_screen, [x, y])


def plot_snake(game_window, color, snk_list, snake_size):
    for x, y in snk_list:
        pg.draw.rect(game_window, color, [x, y, snake_size, snake_size])


def welcome():
    exit_game1 = True

    # Opening events management
    while exit_game1:
        game_window.blit(opening_img, (0, 0))
        screen_text("Press Space To Play", white, 1.12*width//3, height/2)
        for event in pg.event.get():
            if event.type == pg.QUIT:
                exit_game1 = False
                pg.quit()
                exit()

            if event.type == pg.KEYDOWN:
                if event.key == pg.K_SPACE:
                    gameloop()

        pg.display.update()
        clock.tick(40)


def gameloop():

    # Initializing Game variables
    food_x = random.randint(20, width)
    food_y = random.randint(30, height)
    snake_x = width/2
    snake_y = height/2
    exit_game2 = True
    game_over = False
    Vx = 0
    Vy = 0
    d = 20
    score = 0
    fps = 40
    v = 8
    snake_size = 25
    snk_list = []
    snk_length = 1
    wall = False
    eaten = True

    # Infinte loop
    while exit_game2:

        # To read the previous highscore
        with open('highscore.txt', 'r+') as f:
            high_score = f.read()

        # game over background
        if game_over:
            game_window.fill(black)
            pg.display.update()
            screen_text("GAME OVER ", Red, width/3, height/3)

            # If current is greater than previous highscore
            if score > int(high_score):
                high_score = str(score)
                screen_text(
                    "Congratulation !! You broke the previous highscore", green, width/4, height/1.7)
                with open("highscore.txt", 'w') as f:
                    f.write(high_score)

            # gameover by hitting the wall
            elif wall:
                screen_text('You hit the wall !!', Red, width/3, height/2)

            # gameover by bitting itself
            elif eaten:
                screen_text('Stop eating yourself !!', Red, width/3, height/2)

            # game over message
            screen_text("PRESS ENTER TO START AGAIN ",
                        green, width/3, 4*height/5)

            # To start the game again after game over or to close it
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    exit_game2 = False
                    pg.quit()
                    exit()

                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_RETURN:
                        welcome()

        # If its not game-over
        else:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    exit_game2 = False
                    pg.quit()
                    exit()

                # snake movements
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_RIGHT:
                        Vx = v
                        Vy = 0

                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_LEFT:
                        Vx = -v
                        Vy = 0

                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_UP:
                        Vx = 0
                        Vy = -v

                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_DOWN:
                        Vx = 0
                        Vy = v

            snake_x = snake_x + Vx
            snake_y = snake_y + Vy

            # music when the snake bit itself, score updating, genrating the food, inc
            if (((snake_y-food_y)**2+(snake_x-food_x)**2)**0.5 < d):
                pg.mixer.music.load('music/eating.mp3')
                pg.mixer.music.play()
                score += 1
                food_x = random.randint(20, 0.6*width)
                food_y = random.randint(20, 0.6*height)
                snk_length += 3

            # to display the highscore at the top left and top right
            game_window.blit(bg_img, (0, 0))
            screen_text('Score = '+str(score), green, 0, 0)
            screen_text("HighSCORE = "+str(high_score),
                        hs_color, 0.75*width, 0)

            # Snake increament logic
            head = []
            head.append(snake_x)
            head.append(snake_y)
            snk_list.append(head)

            plot_snake(game_window, Blue, snk_list, snake_size)

            if len(snk_list) > snk_length:
                del snk_list[0]

            if (snake_x <= 0) or (snake_x >= width) or (snake_y <= 0) or (snake_y >= height):
                game_over = True
                wall = True
                pg.mixer.music.load('music/game_over.mp3')
                pg.mixer.music.play()

            if head in snk_list[:-1]:
                pg.mixer.music.load("music/snake_bite.mp3")
                pg.mixer.music.play()
                game_over = True
                eaten = True

            pg.draw.rect(game_window, Red, [
                         food_x, food_y, snake_size, snake_size])

        pg.display.update()
        clock.tick(fps)


welcome()
