import pygame, sys, time, random
from p_post_game import *
from p_global import *
from colors import *

def snake(user_name) :

    # Difficulty settings
    # Easy      ->  10
    # Medium    ->  25
    # Hard      ->  40
    # Harder    ->  60
    # Impossible->  120
    difficulty = 25

    # Window size
    frame_size_x = 1550
    frame_size_y = 790

    # Checks for errors encountered
    check_errors = pygame.init()
    # pygame.init() example output -> (6, 0)
    # second number in tuple gives number of errors
    if check_errors[1] > 0:
        print(f'[!] Had {check_errors[1]} errors when initialising game, exiting...')
        sys.exit(-1)
    else:
        print('[+] Game successfully initialised')


    # Initialise game window
    game_window = pygame.display.set_mode((frame_size_x, frame_size_y))
    road = pygame.image.load('Assets/spaacebg.jpg')

    x = 0
    y = 0

    h = WINDOWHEIGHT

    x1 = 0
    y1 = -h

    # Colors (R, G, B)
    black = pygame.Color(0, 0, 0)
    white = pygame.Color(255, 255, 255)
    red = pygame.Color(255, 0, 0)
    green = pygame.Color(0, 255, 0)
    blue = pygame.Color(0, 0, 255)


    # FPS (frames per second) controller
    fps_controller = pygame.time.Clock()


    # Game variables
    snake_pos = [0, 0]
    snake_body = [[100, 50], [100-10, 50], [100-(2*10), 50]]

    food_pos = [random.randrange(1, (frame_size_x//20)) * 20, random.randrange(1, (frame_size_y//10)) * 10]

    food_spawn = True

    direction = 'RIGHT'
    change_to = direction

    score = 0
    # Score
    def show_score(choice, color, font, size):
        score_font = pygame.font.SysFont(font, size)
        score_surface = score_font.render('Score : ' + str(score), True, color)
        score_rect = score_surface.get_rect()
        if choice == 1:
            score_rect.midtop = (frame_size_x/10, 15)
        else:
            score_rect.midtop = (frame_size_x/2, frame_size_y/1.25)
            game_window.blit(score_surface, score_rect)
            pygame.display.flip()


    # Main logic
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                db_manager.delete_from_online(connection, user_name)
                pygame.quit()
                sys.exit()
            # Whenever a key is pressed down
            elif event.type == pygame.KEYDOWN:
                #leave if escape
                if event.key == pygame.K_ESCAPE :
                    db_manager.delete_from_online(connection, user_name)
                    pygame.quit()
                    sys.exit()
                # W -> Up; S -> Down; A -> Left; D -> Right
                if event.key == pygame.K_UP or event.key == ord('w'):
                    change_to = 'UP'
                if event.key == pygame.K_DOWN or event.key == ord('s'):
                    change_to = 'DOWN'
                if event.key == pygame.K_LEFT or event.key == ord('a'):
                    change_to = 'LEFT'
                if event.key == pygame.K_RIGHT or event.key == ord('d'):
                    change_to = 'RIGHT'
                # Esc -> Create event to quit the game
                if event.key == pygame.K_ESCAPE:
                    pygame.event.post(pygame.event.Event(pygame.QUIT))

        # Making sure the snake cannot move in the opposite direction instantaneously
        if change_to == 'UP' and direction != 'DOWN':
            direction = 'UP'
        if change_to == 'DOWN' and direction != 'UP':
            direction = 'DOWN'
        if change_to == 'LEFT' and direction != 'RIGHT':
            direction = 'LEFT'
        if change_to == 'RIGHT' and direction != 'LEFT':
            direction = 'RIGHT'

        # Moving the snake
        if direction == 'UP':
            snake_pos[1] -= 20
        if direction == 'DOWN':
            snake_pos[1] += 20
        if direction == 'LEFT':
            snake_pos[0] -= 20
        if direction == 'RIGHT':
            snake_pos[0] += 20

        # Snake body growing mechanism
        snake_body.insert(0, list(snake_pos))
        if abs(snake_pos[0] - food_pos[0]) <= 10 and abs(snake_pos[1] - food_pos[1]) <= 10:
            score += 1
            food_spawn = False
        else:
            snake_body.pop()

        # Spawning food on the screen
        if not food_spawn:
            food_pos = [random.randrange(1, (frame_size_x//20)) * 20, random.randrange(1, (frame_size_y//20)) * 20]

        food_spawn = True

        # GFX

        y1 += 2
        y += 2

        DISPLAY.blit(road, (x, y))
        DISPLAY.blit(road, (x1, y1))
        if y > h:
            y = -h
        if y1 > h:
            y1 = -h

        #game_window.fill(black)

        for pos in snake_body:
            # Snake body
            # .draw.rect(play_surface, color, xy-coordinate)
            # xy-coordinate -> .Rect(x, y, size_x, size_y)
            pygame.draw.rect(game_window, green, pygame.Rect(pos[0], pos[1], 20, 20))

        # Snake food
        pygame.draw.rect(game_window, red, pygame.Rect(food_pos[0], food_pos[1], 20, 20))

        # Game Over conditions
        # Getting out of bounds
        if snake_pos[0] < 0 or snake_pos[0] > frame_size_x-10:
            return score
        if snake_pos[1] < 0 or snake_pos[1] > frame_size_y-10:
            return score
        # Touching the snake body
        for block in snake_body[1:]:
            if snake_pos[0] == block[0] and snake_pos[1] == block[1]:
                return score

        show_score(1, white, 'consolas', 20)
        # Refresh game screen
        pygame.display.update()
        # Refresh rate
        fps_controller.tick(difficulty)

def snake_driver(user_name) :

    score = snake(user_name)

    print(score)

    status = post_game_processing(user_name, score, "snake")

    # exit to main menu
    if status == -1:
        return -1

    # play again
    else:
        return snake_driver(user_name)
