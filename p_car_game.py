from p_global import *
from colors import *
from p_post_game import *

########################################################################################################################
#   INITIALIZATIONS   ##################################################################################################

CARWIDTH = 100
CARHEIGHT = 150
RECTWIDTH = WINDOWWIDTH / 32
RECTHEIGHT = WINDOWHEIGHT / 16
COINSIZE = WINDOWWIDTH / 20
YDIFF = WINDOWHEIGHT / 8

ENEMYSIZE = 75


STEP = 5

car = pygame.image.load('Assets/paceship_2.png')
road = pygame.image.load('Assets/spaacebg.jpg')
coin = pygame.image.load('Assets/coin.png')
inc = pygame.image.load('Assets/enemy.png')

point_sound = pygame.mixer.Sound('Assets/eat.ogg')

game_FPS = 60

########################################################################################################################
#   GAME LOOP   ########################################################################################################

def gamedloop(user_name, status):
    # points
    points = 0

    RECTX, RECTY = WINDOWWIDTH / 2, 0
    CARX, CARY = WINDOWWIDTH / 2, WINDOWHEIGHT / 2 + CARHEIGHT
    COINX, COINY = random.randrange(0.2 * WINDOWWIDTH, 0.8 * WINDOWWIDTH, STEP), 0
    INCX, INCY = random.randrange(0.2 * WINDOWWIDTH, 0.8 * WINDOWWIDTH, STEP), 0
    INCX2, INCY2 = random.randrange(0.2 * WINDOWWIDTH, 0.8 * WINDOWWIDTH, STEP), -400

    # initial direction
    direction = -1  # -1 is left,1 is right

    x = 0
    y = 0

    h = WINDOWHEIGHT

    x1 = 0
    y1 = -h

    ####################################################################################################################
    #   GAME PHYSICS    ################################################################################################
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                db_manager.delete_from_online(connection, user_name)
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    direction = -1
                elif event.key == pygame.K_RIGHT:
                    direction = 1
                elif event.key == pygame.K_UP:
                    direction = 0
                elif event.key == pygame.K_ESCAPE:
                    db_manager.delete_from_online(connection, user_name)
                    pygame.quit()
                    sys.exit()
        if direction == -1:
            CARX -= STEP
        elif direction == 1:
            CARX += STEP
        #displaying background

        y1 += 2
        y += 2

        DISPLAY.blit(road, (x, y))
        DISPLAY.blit(road, (x1, y1))
        if y > h:
            y = -h
        if y1 > h:
            y1 = -h

        if (check_coin(CARX, CARY, COINX, COINY)):
            COINX, COINY = random.randrange(0.2 * WINDOWWIDTH, 0.8 * WINDOWWIDTH, STEP), 0
            points += 1

        RECTY += STEP
        RECTY = RECTY % YDIFF
        COINY += STEP
        INCY += 2 * STEP
        INCY2 += 2 * STEP

        if COINY >= WINDOWHEIGHT:
            COINX, COINY = random.randrange(0.2 * WINDOWWIDTH, 0.8 * WINDOWWIDTH, STEP), 0
        if INCY >= WINDOWHEIGHT:
            INCX, INCY = random.randrange(0.2 * WINDOWWIDTH, 0.8 * WINDOWWIDTH, STEP), 0
        if INCY2 >=  WINDOWHEIGHT:
            INCX2, INCY2 = random.randrange(0.2 * WINDOWWIDTH, 0.8 * WINDOWWIDTH, STEP), -300

        #for i in range(-1, 8):
            #pygame.draw.rect(DISPLAY, black, [RECTX, RECTY + i * YDIFF, RECTWIDTH, RECTHEIGHT])
        DISPLAY.blit(coin, (COINX, COINY))
        DISPLAY.blit(car, (CARX, CARY))

        DISPLAY.blit(inc, (INCX, INCY))
        DISPLAY.blit(inc, (INCX2, INCY2))

        text = smallfont.render('Score: ' + str(points), True, black)
        DISPLAY.blit(text, (0, 0))

        car_crash_flag1 = car_crash(CARX, CARY, INCX, INCY, points, user_name)
        car_crash_flag2 = car_crash(CARX, CARY, INCX2, INCY2, points, user_name)

        if not car_crash_flag1 == -1 or not car_crash_flag2 == -1 :
            return points

        if check_step_out(CARX):
            if CARX < 0.1 * WINDOWWIDTH:
                for i in range(0, 20):

                    DISPLAY.blit(road, (0, 0))
                    if (check_coin(CARX, CARY, COINX, COINY)):
                        COINX, COINY = random.randrange(0.2 * WINDOWWIDTH, 0.8 * WINDOWWIDTH, STEP), 0
                        points += 1

                    RECTY += STEP
                    RECTY = RECTY % YDIFF
                    COINY += STEP
                    INCY += 2 * STEP
                    INCY2 += 2 * STEP
                    CARX -= STEP
                    CARY -= STEP

                    if COINY >= WINDOWHEIGHT:
                        COINX, COINY = random.randrange(0.2 * WINDOWWIDTH, 0.8 * WINDOWWIDTH, STEP), 0
                    if INCY >= WINDOWHEIGHT:
                        INCX, INCY = random.randrange(0.2 * WINDOWWIDTH, 0.8 * WINDOWWIDTH, STEP), 0
                    if INCY2 >= WINDOWHEIGHT:
                        INCX2, INCY2 = random.randrange(0.2 * WINDOWWIDTH, 0.8 * WINDOWWIDTH, STEP), -400

                    new_car = pygame.transform.rotate(car, 10 + 3 * i)

                    #for i in range(-1, 8):
                        #pygame.draw.rect(DISPLAY, black, [RECTX, RECTY + i * YDIFF, RECTWIDTH, RECTHEIGHT])
                    DISPLAY.blit(coin, (COINX, COINY))
                    DISPLAY.blit(new_car, (CARX, CARY))

                    DISPLAY.blit(inc, (INCX, INCY))
                    DISPLAY.blit(inc, (INCX2, INCY2))

                    text = smallfont.render('Score: ' + str(points), True, black)
                    DISPLAY.blit(text, (0, 0))
                    clock.tick(game_FPS)
                    pygame.display.update()
            if CARX > 0.78 * WINDOWWIDTH:
                for i in range(0, 20):

                    DISPLAY.blit(road, (0, 0))
                    if (check_coin(CARX, CARY, COINX, COINY)):
                        COINX, COINY = random.randrange(0.2 * WINDOWWIDTH, 0.8 * WINDOWWIDTH, STEP), 0
                        points += 1

                    RECTY += STEP
                    RECTY = RECTY % YDIFF
                    COINY += STEP
                    INCY += 2 * STEP
                    INCY2 += 2 * STEP
                    CARX += STEP
                    CARY -= STEP

                    if COINY >= WINDOWHEIGHT:
                        COINX, COINY = random.randrange(0.2 * WINDOWWIDTH, 0.8 * WINDOWWIDTH, STEP), 0
                    if INCY >= WINDOWHEIGHT:
                        INCX, INCY = random.randrange(0.2 * WINDOWWIDTH, 0.8 * WINDOWWIDTH, STEP), 0
                    if INCY2 >= 9 / 10 * WINDOWHEIGHT:
                        INCX2, INCY2 = random.randrange(0.2 * WINDOWWIDTH, 0.8 * WINDOWWIDTH, STEP), -350

                    new_car = pygame.transform.rotate(car, -(10 + 3 * i))

                    #for i in range(-1, 8):
                        #pygame.draw.rect(DISPLAY, black, [RECTX, RECTY + i * YDIFF, RECTWIDTH, RECTHEIGHT])
                    DISPLAY.blit(coin, (COINX, COINY))
                    DISPLAY.blit(new_car, (CARX, CARY))

                    DISPLAY.blit(inc, (INCX, INCY))
                    DISPLAY.blit(inc, (INCX2, INCY2))

                    text = smallfont.render('Score: ' + str(points), True, black)
                    DISPLAY.blit(text, (0, 0))
                    clock.tick(game_FPS)
                    pygame.display.update()

            ############################################################################################################
            #   CALLING GAME OVER   ####################################################################################
            return points
            #post_game_processing(user_name, points)
            ############################################################################################################

        clock.tick(game_FPS)
        pygame.display.update()


#   GAME LOOP DRIVER ###################################################################################################

def car_game_driver(user_name, status) :

    points = gamedloop(user_name, 0)
    status = post_game_processing(user_name, points, "car")
    #exit to main menu
    if status == -1 :
        return -1

    #play again
    else :
        car_game_driver(user_name, 0)

########################################################################################################################
#   GAME LOOP HELPERS   ################################################################################################

def check_coin(CARX, CARY, COINX, COINY):
    if (CARX - COINX) <= COINSIZE and (COINX - CARX) <= CARWIDTH:
        if (CARY - COINY) <= COINSIZE and (COINY - CARY) <= CARHEIGHT:
            #point_sound.play()
            return True


def car_crash(CARX, CARY, INCX, INCY, points, user_name):
    if (CARX - INCX) <= ENEMYSIZE and (INCX - CARX) <= ENEMYSIZE:
        if (CARY - INCY) <= ENEMYSIZE and (INCY - CARY) <= ENEMYSIZE:
            return points
            #post_game_processing(user_name, points)

    return -1

def check_step_out(CARX):
    """if CARX < 0.1 * WINDOWWIDTH or CARX > 0.78 * WINDOWWIDTH:
        return True"""
    if CARX < 0 or CARX > 0.85 * WINDOWWIDTH :
        return True
    return False