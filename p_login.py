import sys, pygame , random, time
import db_manager
import colors
import p_global
from p_main_menu import main_menu

########################################################################################################################
#   LOGIN   ############################################################################################################

def login(error):

    user_name, password = user_input(error)

    # validate user_name and password and proceed appropriately
    # -1 = wrong password, 0 = success, 1 = name not found
    flag = db_manager.validate_password(p_global.connection, user_name, password)

    if flag == 0 :
        ################ main menu #####################
        db_manager.insert_into_online(p_global.connection, user_name)
        main_menu(user_name)

    elif flag == -1 :
        ############### login(1) ######################
        login(1)

    elif flag == 1 :
        ############## user doesnt exist ################
        user_doesnt_exist(user_name, password)
        
########################################################################################################################
#   USER DOESNT EXIST   ################################################################################################

def user_doesnt_exist(user_name,password):
    point = 1

    #### init

    x = 0
    y = 0
    h = p_global.WINDOWHEIGHT
    x1 = 0
    y1 = -h

    y1 += 2
    y += 2

    ####

    while 1:

        y1 += 2
        y += 2

        p_global.DISPLAY.blit(p_global.background_image, (x, y))
        p_global.DISPLAY.blit(p_global.background_image, (x1, y1))

        if y > h:
            y = -h
        if y1 > h:
            y1 = -h

        game_title = p_global.titlefont.render("AlternitY", True, colors.red)
        message1 = p_global.headingfont.render('User does not exist.', True, colors.green)
        message2 = p_global.mediumfont.render('Select YES to signup, NO to go back', True, colors.green)

        p_global.DISPLAY.blit(game_title, (p_global.WINDOWWIDTH * 1.3 / 5, 100))
        p_global.DISPLAY.blit(message1, (475, 350))
        p_global.DISPLAY.blit(message2, (375, 400))

        if point == 0:
            yes = p_global.menufont.render('YES', True, colors.cyan)
            no = p_global.menufont.render('NO', True, colors.white)
        elif point == 1:
            yes = p_global.menufont.render('YES', True, colors.white)
            no = p_global.menufont.render('NO', True, colors.cyan)

        p_global.DISPLAY.blit(yes, (690, 500))
        p_global.DISPLAY.blit(no, (700, 550))

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
                    #IF YES
                    if point == 0:
                    # SAVE THE USER ID AND PASSWORD
                        db_manager.insert_into_user(p_global.connection, user_name, password)
                    # GO TO START MENU OF THE GAME PAGE
                        db_manager.insert_into_online(p_global.connection, user_name)
                        main_menu(user_name)

                    #IF NO
                    elif point == 1:
                    # GO TO LOGIN PAGE
                        login(0)

        point = point % 2
        p_global.clock.tick(p_global.FPS)
        pygame.display.update()
        
########################################################################################################################
#   USER INPUT  ########################################################################################################

def user_input(error) :

    p_global.clock = pygame.time.Clock()
    input = ''

    done = False

    counter = 0

    #### init

    x = 0
    y = 0
    h = p_global.WINDOWHEIGHT
    x1 = 0
    y1 = -h
    ####

    while not done:

        for event in pygame.event.get() :
            if done :
                break
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE :
                    pygame.quit()
                    sys.exit()

                if event.key == pygame.K_RETURN:
                    # Do something with the password and reset it.
                    user_name = input  # I just print it to see if it works.
                    print(user_name)
                    input = ''
                    done = True

                elif event.key == pygame.K_BACKSPACE :
                    input = '' if len(input) == 1 else input[0 : len(input) - 1]

                else:  # Add the character to the password string.h
                    input += event.unicode

        #p_global.DISPLAY.fill((30, 30, 30))
        y1 += 2
        y += 2

        p_global.DISPLAY.blit(p_global.background_image, (x, y))
        p_global.DISPLAY.blit(p_global.background_image, (x1, y1))

        if y > h:
            y = -h
        if y1 > h:
            y1 = -h


        # Render the asterisks and blit them.
        game_title = p_global.titlefont.render("AlternitY", True, colors.red)
        user_name_prompt = p_global.menufont.render("ENTER PLAYER NAME : ", True, colors.lime)
        username_surface = p_global.menufont.render(input, True, colors.white)
        error_prompt = p_global.menufont.render("password doesnt match username", True, colors.red)

        p_global.DISPLAY.blit(game_title, (1.3 * p_global.WINDOWWIDTH / 5, 100))
        p_global.DISPLAY.blit(user_name_prompt, (400, 400))
        p_global.DISPLAY.blit(username_surface, (2.75 * p_global.WINDOWWIDTH / 5, 400))
        if error == 1 :
            p_global.DISPLAY.blit(error_prompt, (400, 9 * p_global.WINDOWHEIGHT / 10))

        pygame.display.flip()
        p_global.clock.tick(30)

    #   password    #######################

    done = False

    password = ''

    while not done:
        for event in pygame.event.get():
            if done:
                break
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    # Do something with the password and reset it.
                    password = input  # I just print it to see if it works.
                    print(password)
                    input = ''
                    done = True

                elif event.key == pygame.K_BACKSPACE:
                    input = '' if len(input) == 1 else input[0: len(input) - 1]

                else:  # Add the character to the password string.h
                    input += event.unicode

        #p_global.DISPLAY.fill((30, 30, 30))
        y1 += 2
        y += 2

        p_global.DISPLAY.blit(p_global.background_image, (x, y))
        p_global.DISPLAY.blit(p_global.background_image, (x1, y1))

        if y > h:
            y = -h
        if y1 > h:
            y1 = -h

        # Render the asterisks and blit them.
        #(70, 200, 150)
        game_title = p_global.titlefont.render("AlternitY", True, colors.red)
        user_name_prompt = p_global.menufont.render("ENTER PLAYER NAME : ", True, colors.lime)
        password_prompt = p_global.menufont.render("ENTER PASSWORD : ", True, colors.lime)
        username_surface = p_global.menufont.render(user_name, True, colors.white)
        password_surface = p_global.menufont.render('*' * len(input), True, colors.white)
        error_prompt = p_global.menufont.render("password doesnt match username", True, colors.red)

        p_global.DISPLAY.blit(game_title, (1.3 * p_global.WINDOWWIDTH / 5, 100))
        p_global.DISPLAY.blit(user_name_prompt, (400, 400))
        p_global.DISPLAY.blit(username_surface, (2.75 * p_global.WINDOWWIDTH / 5, 400))
        p_global.DISPLAY.blit(password_prompt, (400, 450))
        p_global.DISPLAY.blit(password_surface, (2.75 * p_global.WINDOWWIDTH / 5, 450))
        if error == 1:
            p_global.DISPLAY.blit(error_prompt, (400, 9 * p_global.WINDOWHEIGHT / 10))

        pygame.display.flip()
        p_global.clock.tick(30)

    print("user input successfull")
    return user_name, password