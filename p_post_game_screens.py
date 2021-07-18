from p_global import *
from colors import *
from p_leaderboards import *

#both functions return 0 for play again and -1 for exit to main menu

########################################################################################################################
#   GAME OVER SCREEN     ###############################################################################################

def post_game_screen(user_name, score, hs_score, hs_name, flag, game):

    #flag 1 --> highscore
    #flag 0 --> not highscore

    point = 0

    x = 0
    y = 0
    h = WINDOWHEIGHT
    x1 = 0
    y1 = -h

    if flag == 0 :
        message1 = italicfont.render('SCORE - ' + str(score), True, red)
        message2 = italicfont.render('score to beat -> ' + str(hs_score) + ' set by ' + hs_name, True, green)

    else :
        message1 = italicfont.render('SCORE - ' + str(score) + ' HIGHSCORE !!!', True, red)
        message2 = italicfont.render('YOU JUST BEAT ' + hs_name, True, green)


    while 1:
        #DISPLAY.blit(background_image, [0, 0])
        y1 += 2
        y += 2

        DISPLAY.blit(background_image, (x, y))
        DISPLAY.blit(background_image, (x1, y1))

        if y > h:
            y = -h
        if y1 > h:
            y1 = -h

        if point == 0:
            start = menufont.render('PLAY AGAIN', True, cyan)
            leaderboard = menufont.render('LEADERBOARD', True, white)
            mainmenu = menufont.render('MAIN MENU', True, white)
            quit = menufont.render('QUIT GAME', True, white)
        elif point == 1:
            start = menufont.render('PLAY AGAIN', True, white)
            leaderboard = menufont.render('LEADERBOARD', True, cyan)
            mainmenu = menufont.render('MAIN MENU', True, white)
            quit = menufont.render('QUIT GAME', True, white)
        elif point == 2:
            start = menufont.render('PLAY AGAIN', True, white)
            leaderboard = menufont.render('LEADERBOARD', True, white)
            mainmenu = menufont.render('MAIN MENU', True, cyan)
            quit = menufont.render('QUIT GAME', True, white)

        elif point == 3:
            start = menufont.render('PLAY AGAIN', True, white)
            leaderboard = menufont.render('LEADERBOARD', True, white)
            mainmenu = menufont.render('MAIN MENU', True, white)
            quit = menufont.render('QUIT GAME', True, cyan)

        DISPLAY.blit(message1, (650, 100))
        DISPLAY.blit(message2, (400, 2 * WINDOWHEIGHT / 10))
        DISPLAY.blit(start, (WINDOWWIDTH / 10, WINDOWHEIGHT * 8 / 20))
        DISPLAY.blit(leaderboard, (WINDOWWIDTH / 10,  9 * WINDOWHEIGHT / 20))
        DISPLAY.blit(mainmenu, (WINDOWWIDTH / 10, 10 * WINDOWHEIGHT / 20))
        DISPLAY.blit(quit, (WINDOWWIDTH / 10, 11 * WINDOWHEIGHT / 20))

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
                    #play again
                    if point == 0:
                        return 0
                    elif point == 1:
                        #leaderboard
                        leaderboard_selector(user_name, game)

                    elif point == 2:
                        #main menu
                        return -1

                    elif point == 3:
                        db_manager.delete_from_online(connection, user_name)
                        pygame.quit()
                        sys.exit()

        point = point % 4
        clock.tick(FPS)
        pygame.display.update()

