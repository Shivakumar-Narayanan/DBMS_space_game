from p_global import *
from colors import *
from p_leaderboard_screen import *

########################################################################################################################
#   LEADERBOARD SELECTOR   #############################################################################################

def leaderboard_selector(user_name, game) :
    point = 0

    prompt = headfont.render('LeaderboarD', True, red)
    exit_message = smallfont.render('press esc to exit', True, red)

    while 1:
        DISPLAY.blit(background_image, [0, 0])
        DISPLAY.blit(exit_message, (7.5 * WINDOWWIDTH / 10, 9 * WINDOWHEIGHT / 10))

        if point == 0:
            global_message = menufont.render('GLOBAL LEADERBOARD', True, cyan)
            local_message = menufont.render('FRIENDS LEADRERBOARD', True, white)
            back = menufont.render('GO BACK', True, white)

        elif point == 1:
            global_message = menufont.render('GLOBAL LEADERBOARD', True, white)
            local_message = menufont.render('FRIENDS LEADRERBOARD', True, cyan)
            back = menufont.render('GO BACK', True, white)

        elif point == 2 :
            global_message = menufont.render('GLOBAL LEADERBOARD', True, white)
            local_message = menufont.render('FRIENDS LEADRERBOARD', True, white)
            back = menufont.render('GO BACK', True, cyan)

        DISPLAY.blit(prompt, (500,100))
        DISPLAY.blit(global_message, (500, 300))
        DISPLAY.blit(local_message, (500, 350))
        DISPLAY.blit(back, (500, 450))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                db_manager.delete_from_online(connection, user_name)
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE :
                    return
                if event.key == pygame.K_DOWN:
                    point += 1
                elif event.key == pygame.K_UP:
                    point -= 1
                elif event.key == pygame.K_RETURN:
                    if point == 0:
                        print()
                        ################# call global leaderboard(user_name)
                        global_leaderboard(user_name, game)

                    elif point == 1:
                        print()
                        ################# call local leaderboarf(user_name)
                        friends_leaderboard(user_name, game)

                    elif point == 2:
                        return

        point = point % 3
        clock.tick(FPS)
        pygame.display.update()
