from p_global import *
from colors import *

########################################################################################################################
#   GLOBAL LEADERBOARD  ################################################################################################

def global_leaderboard(user_name, game) :

    global_message = headfont.render('Global leaderboarD', True, red)
    exit_message = smallfont.render('press esc to exit', True, red)

    result = db_manager.get_leaderboard_global(connection, game)

    DISPLAY.blit(background_image, [0,0])

    DISPLAY.blit(global_message, (400, 100))
    DISPLAY.blit(exit_message, (7.5 * WINDOWWIDTH / 10, 9 *WINDOWHEIGHT / 10))

    y_mult = 5
    x_offset = 30

    printed = False

    while 1 :

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                db_manager.delete_from_online(connection, user_name)
                pygame.quit()
                sys.exit()

            elif event.type == pygame.KEYDOWN :
                if event.key == pygame.K_ESCAPE :
                    return

            if not printed :
                for next_row in result :
                    name = next_row[0]
                    score = str(next_row[1])

                    if(name == user_name) :
                        name = scorefont.render(name, True, green)
                        score = scorefont.render(score, True, green)
                    else :
                        name = scorefont.render(name, True, white)
                        score = scorefont.render(score, True, white)

                    DISPLAY.blit(name, (x_offset + 500, y_mult * 60))
                    DISPLAY.blit(score, (x_offset + 850 , y_mult * 60))

                    y_mult += 1
                    pygame.display.flip()
                    pygame.event.pump()
                    pygame.time.delay(500)

            printed = True

        clock.tick(FPS)
        pygame.display.update()

########################################################################################################################
#   FRIENDS LEADERBOARD  ###############################################################################################

def friends_leaderboard(user_name, game) :
    local_message = headfont.render('Friends leaderboarD', True, red)
    exit_message = smallfont.render('press esc to exit', True, red)

    result = db_manager.get_leaderboard_friends(connection, user_name, game)

    DISPLAY.blit(background_image, [0, 0])

    DISPLAY.blit(local_message, (375, 100))
    DISPLAY.blit(exit_message, (7.5 * WINDOWWIDTH / 10, 9 * WINDOWHEIGHT / 10))

    y_mult = 5
    x_offset = 30

    printed = False

    x = 0
    y = 0
    h = WINDOWHEIGHT
    x1 = 0
    y1 = -h

    while 1:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                db_manager.delete_from_online(connection, user_name)
                pygame.quit()
                sys.exit()

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return

            if not printed:
                for next_row in result:
                    name = next_row[0]
                    score = str(next_row[1])

                    if (name == user_name):
                        name = scorefont.render(name, True, green)
                        score = scorefont.render(score, True, green)
                    else:
                        name = scorefont.render(name, True, white)
                        score = scorefont.render(score, True, white)

                    DISPLAY.blit(name, (x_offset + 500, y_mult * 60))
                    DISPLAY.blit(score, (x_offset + 850, y_mult * 60))

                    y_mult += 1
                    pygame.display.flip()
                    pygame.event.pump()
                    pygame.time.delay(500)

            printed = True

        clock.tick(FPS)
        pygame.display.update()