from p_global import *
from colors import *
from p_friends import friend_screen
from p_game_select import *
from p_notifications import *

########################################################################################################################
#   MAIN MENU   ########################################################################################################

def main_menu(user_name):
    point = 0

    x = 0
    y = 0
    h = WINDOWHEIGHT
    x1 = 0
    y1 = -h

    count = 0   # notifications will only be checked when count is 0.

    while 1:

        if count == 0 :
            notifications_driver(user_name)
            count = 1

        #DISPLAY.blit(background_image, [0, 0])
        y1 += 2
        y += 2

        DISPLAY.blit(background_image, (x, y))
        DISPLAY.blit(background_image, (x1, y1))

        if y > h:
            y = -h
        if y1 > h:
            y1 = -h

        game_title = titlefont.render("AlternitY", True, red)
        message1 = headingfont.render('Main Menu', True, green)

        DISPLAY.blit(message1, (600, 350))
        DISPLAY.blit(game_title, (1.3 * WINDOWWIDTH / 5, 100))

        if point == 0:
            start = menufont.render('SELECT GAME - choose a game', True, cyan)
            friend = menufont.render('FRIENDS', True, white)
            quit = menufont.render('QUIT', True, white)

        elif point == 1 :
            start = menufont.render('SELECT GAME', True, white)
            friend = menufont.render('FRIENDS - manage friends and requests', True, cyan)
            quit = menufont.render('QUIT', True, white)

        elif point == 2:
            start = menufont.render('SELECT GAME', True, white)
            friend = menufont.render('FRIENDS', True, white)
            quit = menufont.render('QUIT - quit game', True, cyan)

        DISPLAY.blit(start, (500,450))
        DISPLAY.blit(friend, (500,500))
        DISPLAY.blit(quit, (500,550))

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

                    count = 0

                    if point == 0:
                        ########    calling selection screen ############
                        select_game_page(user_name)

                    elif point == 1 :
                        ########    calling friend screen ###########

                        friend_screen(user_name, 0)

                    elif point == 2:
                        ########    quit ############
                        db_manager.delete_from_online(connection, user_name)
                        pygame.quit()
                        sys.exit()

        point = point % 3
        clock.tick(FPS)
        pygame.display.update()