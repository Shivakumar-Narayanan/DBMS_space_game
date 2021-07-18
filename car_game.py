import sys, pygame, random, time
import db_manager

########################################################################################################################
#   GLOBAL VARIABLES    ################################################################################################

pw = "6yzKjs3Mdu"
uname = "sql6411632"
connection = db_manager.create_server_connection("sql6.freemysqlhosting.net", uname, pw)

pygame.init()
WINDOWWIDTH = 800
WINDOWHEIGHT = 512
FPS = 30

user_id = 0
user_name = None

CARWIDTH = WINDOWWIDTH / 9
CARHEIGHT = WINDOWHEIGHT / 4
RECTWIDTH = WINDOWWIDTH / 32
RECTHEIGHT = WINDOWHEIGHT / 16
COINSIZE = WINDOWWIDTH / 16
YDIFF = WINDOWHEIGHT / 8

STEP = 5

white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)

clock = pygame.time.Clock()
DISPLAY = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))

car = pygame.image.load('Assets/car.png')
road = pygame.image.load('Assets/road.png')
coin = pygame.image.load('Assets/coin.png')
inc = pygame.image.load('Assets/inc.png')

point_sound = pygame.mixer.Sound('Assets/eat.ogg')

smallfont = pygame.font.Font(None, 28)
menufont = pygame.font.Font(None, 48)
overfont = pygame.font.Font(None, 60)

pygame.display.set_caption("CAR GAME")

########################################################################################################################
#   GAME LOOP   ########################################################################################################

def gamedloop():

    #   CALLING START MENU  ############################################################################################
    startmenu()
    ####################################################################################################################

    # points
    points = 0

    RECTX, RECTY = WINDOWWIDTH / 2, 0
    CARX, CARY = WINDOWWIDTH / 2, WINDOWHEIGHT / 2 + CARHEIGHT
    COINX, COINY = random.randrange(0.2 * WINDOWWIDTH, 0.8 * WINDOWWIDTH, STEP), 0
    INCX, INCY = random.randrange(0.2 * WINDOWWIDTH, 0.8 * WINDOWWIDTH, STEP), 0

    #initial direction
    direction = -1  # -1 is left,1 is right

    ####################################################################################################################
    #   GAME PHYSICS    ################################################################################################
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
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
                    pause()
        if direction == -1:
            CARX -= STEP
        elif direction == 1:
            CARX += STEP
        DISPLAY.fill(white)
        DISPLAY.blit(road, (0, 0))
        if (check_coin(CARX, CARY, COINX, COINY)):
            COINX, COINY = random.randrange(0.2 * WINDOWWIDTH, 0.8 * WINDOWWIDTH, STEP), 0
            points += 1

        RECTY += STEP
        RECTY = RECTY % YDIFF
        COINY += STEP
        INCY += 2 * STEP

        if COINY >= WINDOWHEIGHT:
            COINX, COINY = random.randrange(0.2 * WINDOWWIDTH, 0.8 * WINDOWWIDTH, STEP), 0
        if INCY >= WINDOWHEIGHT:
            INCX, INCY = random.randrange(0.2 * WINDOWWIDTH, 0.8 * WINDOWWIDTH, STEP), 0

        for i in range(-1, 8):
            pygame.draw.rect(DISPLAY, black, [RECTX, RECTY + i * YDIFF, RECTWIDTH, RECTHEIGHT])
        DISPLAY.blit(coin, (COINX, COINY))
        DISPLAY.blit(car, (CARX, CARY))

        DISPLAY.blit(inc, (INCX, INCY))

        text = smallfont.render('Score: ' + str(points), True, black)
        DISPLAY.blit(text, (0, 0))

        car_crash(CARX, CARY, INCX, INCY)
        if check_step_out(CARX):
            if CARX < 0.1 * WINDOWWIDTH:
                for i in range(0, 20):
                    DISPLAY.fill(white)
                    DISPLAY.blit(road, (0, 0))
                    if (check_coin(CARX, CARY, COINX, COINY)):
                        COINX, COINY = random.randrange(0.2 * WINDOWWIDTH, 0.8 * WINDOWWIDTH, STEP), 0
                        points += 1

                    RECTY += STEP
                    RECTY = RECTY % YDIFF
                    COINY += STEP
                    INCY += 2 * STEP
                    CARX -= STEP
                    CARY -= STEP

                    if COINY >= WINDOWHEIGHT:
                        COINX, COINY = random.randrange(0.2 * WINDOWWIDTH, 0.8 * WINDOWWIDTH, STEP), 0
                    if INCY >= WINDOWHEIGHT:
                        INCX, INCY = random.randrange(0.2 * WINDOWWIDTH, 0.8 * WINDOWWIDTH, STEP), 0

                    new_car = pygame.transform.rotate(car, 10 + 3 * i)

                    for i in range(-1, 8):
                        pygame.draw.rect(DISPLAY, black, [RECTX, RECTY + i * YDIFF, RECTWIDTH, RECTHEIGHT])
                    DISPLAY.blit(coin, (COINX, COINY))
                    DISPLAY.blit(new_car, (CARX, CARY))

                    DISPLAY.blit(inc, (INCX, INCY))

                    text = smallfont.render('Score: ' + str(points), True, black)
                    DISPLAY.blit(text, (0, 0))
                    clock.tick(FPS)
                    pygame.display.update()
            if CARX > 0.78 * WINDOWWIDTH:
                for i in range(0, 20):
                    DISPLAY.fill(white)
                    DISPLAY.blit(road, (0, 0))
                    if (check_coin(CARX, CARY, COINX, COINY)):
                        COINX, COINY = random.randrange(0.2 * WINDOWWIDTH, 0.8 * WINDOWWIDTH, STEP), 0
                        points += 1

                    RECTY += STEP
                    RECTY = RECTY % YDIFF
                    COINY += STEP
                    INCY += 2 * STEP
                    CARX += STEP
                    CARY -= STEP

                    if COINY >= WINDOWHEIGHT:
                        COINX, COINY = random.randrange(0.2 * WINDOWWIDTH, 0.8 * WINDOWWIDTH, STEP), 0
                    if INCY >= WINDOWHEIGHT:
                        INCX, INCY = random.randrange(0.2 * WINDOWWIDTH, 0.8 * WINDOWWIDTH, STEP), 0

                    new_car = pygame.transform.rotate(car, -(10 + 3 * i))

                    for i in range(-1, 8):
                        pygame.draw.rect(DISPLAY, black, [RECTX, RECTY + i * YDIFF, RECTWIDTH, RECTHEIGHT])
                    DISPLAY.blit(coin, (COINX, COINY))
                    DISPLAY.blit(new_car, (CARX, CARY))

                    DISPLAY.blit(inc, (INCX, INCY))

                    text = smallfont.render('Score: ' + str(points), True, black)
                    DISPLAY.blit(text, (0, 0))
                    clock.tick(FPS)
                    pygame.display.update()

            ############################################################################################################
            #   CALLING GAME OVER   ####################################################################################
            game_over()
            ############################################################################################################

        clock.tick(FPS)
        pygame.display.update()

########################################################################################################################
#   IGNORE IMPLEMENTATION DETAILS   ####################################################################################

def check_coin(CARX, CARY, COINX, COINY):
    if (CARX - COINX) <= COINSIZE and (COINX - CARX) <= CARWIDTH:
        if (CARY - COINY) <= COINSIZE and (COINY - CARY) <= CARHEIGHT:
            point_sound.play()
            return True


def car_crash(CARX, CARY, INCX, INCY):
    if (CARX - INCX) <= CARWIDTH and (INCX - CARX) <= CARWIDTH:
        if (CARY - INCY) <= CARHEIGHT and (INCY - CARY) <= CARHEIGHT:
            game_over()

########################################################################################################################
########################################      GAME SCREENS                            ##################################

########################################################################################################################
#   LOGIN   ############################################################################################################

def login(error) :
    
    instruction_label1 = pygame.makeLabel("Enter Player name", 40, 10, 10, white)
    pygame.showLabel(instruction_label1)
    

########################################################################################################################
#   START MENU  ########################################################################################################

def startmenu():
    point = 0
    while 1:
        DISPLAY.fill(white)
        if point == 0:
            start = menufont.render('START GAME', True, red)
            quit = menufont.render('QUIT GAME', True, black)
        elif point == 1:
            start = menufont.render('START GAME', True, black)
            quit = menufont.render('QUIT GAME', True, red)
        DISPLAY.blit(start, (WINDOWWIDTH / 10, WINDOWHEIGHT / 10))
        DISPLAY.blit(quit, (WINDOWWIDTH / 10, 3 * WINDOWHEIGHT / 10))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DOWN:
                    point += 1
                elif event.key == pygame.K_UP:
                    point -= 1
                elif event.key == pygame.K_RETURN:
                    if point == 0:
                        return True
                    elif point == 1:
                        pygame.quit()
                        sys.exit()

        point = point % 2
        clock.tick(FPS)
        pygame.display.update()

########################################################################################################################
#   GAME OVER SCREEN    ################################################################################################

def game_over():
    DISPLAY.fill(red)
    crashed = overfont.render('YOU CRASHED', True, black)
    gameover = overfont.render('GAME OVER', True, black)
    DISPLAY.blit(crashed, (WINDOWWIDTH / 10, WINDOWHEIGHT / 10))
    DISPLAY.blit(gameover, (WINDOWWIDTH / 10, 5 * WINDOWHEIGHT / 10))
    pygame.display.update()
    wait_for_key_press()
    gameloop()

########################################################################################################################
########################################################################################################################
########################################################################################################################
#   PAUSE GAME  ########################################################################################################

def pause():
    pause = overfont.render('PAUSED', True, red)
    DISPLAY.blit(pause, (0.4 * WINDOWWIDTH, WINDOWHEIGHT / 3))
    pygame.display.update()
    while 1:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return

########################################################################################################################
########################################################################################################################

def check_step_out(CARX):
    if CARX < 0.1 * WINDOWWIDTH or CARX > 0.78 * WINDOWWIDTH:
        return True
    return False

########################################################################################################################
#   WAIT FOR KEY PRESS  ################################################################################################

def wait_for_key_press() :
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN :
                return

########################################################################################################################
#   AFTER INITIAIZATION     ############################################################################################

gameloop()