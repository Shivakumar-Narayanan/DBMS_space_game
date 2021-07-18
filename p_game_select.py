import pygame
from p_global import *
from colors import *
from p_car_game import car_game_driver
from p_snake import *
from p_global import *
from p_flappy import *

def select_game_page(user_name):

    point=0

    x = 0
    y = 0
    h = WINDOWHEIGHT
    x1 = 0
    y1 = -h

    while 1:
        game_title = titlefont.render("AlternitY", True, red)
        #DISPLAY.blit(background_image, [0, 0])
        y1 += 2
        y += 2

        DISPLAY.blit(background_image, (x, y))
        DISPLAY.blit(background_image, (x1, y1))

        if y > h:
            y = -h
        if y1 > h:
            y1 = -h

        message1 = headingfont.render('SELECT GAME', True, green)

        DISPLAY.blit(game_title, (1.3 * WINDOWWIDTH / 5, 100))
        DISPLAY.blit(message1, (600, 350))

        if point == 0:
            snake = menufont.render('SNAKE', True, cyan)
            car_game = menufont.render('SPACE INVADER', True, white)
            tetris = menufont.render('FLAPPY BIRD', True, white)
            back = menufont.render('GO BACK', True, white)

        elif point == 1 :
            snake = menufont.render('SNAKE', True, white)
            car_game = menufont.render('SPACE INVADER', True, cyan)
            tetris = menufont.render('FLAPPY BIRD', True, white)
            back = menufont.render('GO BACK', True, white)

        elif point == 2:
            snake = menufont.render('SNAKE', True, white)
            car_game = menufont.render('SPACE INVADER', True, white)
            tetris = menufont.render('FLAPPY BIRD', True, cyan)
            back = menufont.render('GO BACK', True, white)

        elif point == 3:
            snake = menufont.render('SNAKE', True, white)
            car_game = menufont.render('SPACE INVADER', True, white)
            tetris = menufont.render('FLAPPY BIRD', True, white)
            back = menufont.render('GO BACK', True, cyan)

        DISPLAY.blit(snake, (500, 450))
        DISPLAY.blit(car_game, (500, 500))
        DISPLAY.blit(tetris, (500, 550))
        DISPLAY.blit(back, (500, 650))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                db_manager.delete_from_online(connection, user_name)
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DOWN:
                    point += 1
                elif event.key == pygame.K_UP:
                    point -= 1
                elif event.key == pygame.K_RETURN:
                    if point == 0:
                        #OPEN SNAKE PAGE
                        flag = snake_driver(user_name)
                        if flag == -1 :
                            return
                        status = 0

                    elif point == 1 :
                        #OPEN CAR GAME PAGE
                        flag = car_game_driver(user_name, 0)
                        if flag == -1 :
                            return
                        status = 0

                    elif point == 2:
                        #OPEN FLAPPY BIRD
                        flag = flappy_driver(user_name)
                        if flag == -1 :
                            return
                        status = 0

                    elif point == 3:
                        return


        point = point % 4
        clock.tick(FPS)
        pygame.display.update()