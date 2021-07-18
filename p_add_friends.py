from p_global import *
from colors import *
import db_manager

########################################################################################################################
#   ADD FRIENDS   ######################################################################################################

def add_friend_screen(error, user_name) :

    friend = friend_input(user_name, error)
    if friend == "" :
        return 0
    flag = db_manager.validate_friend(connection, friend)

    # success
    if flag == 0 :
        return db_manager.insert_into_pending(connection, user_name, friend)

        #main_menu(user_name, 1)

    else :
        return add_friend_screen(1, user_name)

########################################################################################################################
#   GET FRIEND INPUT  ##################################################################################################

def friend_input(user_name, error) :

    clock = pygame.time.Clock()
    input = ''

    exit_message = smallfont.render('press esc to exit', True, red)

    done = False

    x = 0
    y = 0
    h = WINDOWHEIGHT
    x1 = 0
    y1 = -h

    while not done:
        for event in pygame.event.get() :
            if done :
                break
            if event.type == pygame.QUIT:
                db_manager.delete_from_online(connection, user_name)
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:

                if event.key == pygame.K_ESCAPE :
                    return ""

                elif event.key == pygame.K_RETURN:
                    # Do something with the password and reset it.
                    user_name = input  # I just print it to see if it works.
                    print(user_name)
                    input = ''
                    done = True

                elif event.key == pygame.K_BACKSPACE :
                    input = '' if len(input) == 1 else input[0 : len(input) - 1]

                else:  # Add the character to the password string.h
                    input += event.unicode

        #DISPLAY.fill((30, 30, 30))
        #DISPLAY.blit(background_image, [0, 0])
        y1 += 2
        y += 2

        DISPLAY.blit(background_image, (x, y))
        DISPLAY.blit(background_image, (x1, y1))

        if y > h:
            y = -h
        if y1 > h:
            y1 = -h

        DISPLAY.blit(exit_message, (7.5 * WINDOWWIDTH / 10, 9 * WINDOWHEIGHT / 10))

        # Render the asterisks and blit them.
        lol_prompt = headfont.render("ADD FRIENDS ", True, red)
        user_name_prompt = menufont.render("ENTER FRIEND NAME : ", True, lime)
        username_surface = menufont.render(input, True, white)
        error_prompt = menufont.render("player does not exist", True, red)

        DISPLAY.blit(lol_prompt, (500, 100))
        DISPLAY.blit(user_name_prompt, (450, 300))
        DISPLAY.blit(username_surface, (900, 300))
        if error == 1 :
            DISPLAY.blit(error_prompt, (600, 400))

        pygame.display.flip()
        clock.tick(30)

    return user_name