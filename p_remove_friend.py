import pygame
from p_global import *
from colors import *
import db_manager

def friend_remove_driver(user_name, start) :

    # start = offset
    # function queries friend and gets the next 10 rows starting from offset
    # if result is none, then return -3
    # otherwise flag = remove_friends(start, result)
    # if flag is -1, then return -1
    # if flag is -2, then return -2

    # if start is -1, then we are trying to check if there is another page of friends
    # so cehck and return -3 if none and return 1 if there is

    if start < 0:
        result = db_manager.get_friends_list(connection, user_name, -start)
        if result == [] or result == None:
            return -3
        else:
            return 1

    result = db_manager.get_friends_list(connection, user_name, start)


    if result == [] :
        if start == 0 :
            #   no friends  #
            return -5
        else :
            return -3

    flag = remove_friends(user_name, start, result)

    return flag

def remove_friends(user_name, start, tuples) :

    # prints tuples
    # if right arrow, flag =  a(start + 10)
    # if left, return -1
    # if flag = -2, return -2

    if tuples == [] or tuples == None :
        return -5

    global_message = headfont.render('REMOVE FRIENDS', True, red)
    exit_message = smallfont.render('press esc to exit', True, red)
    remove_message_red = menufont.render('remove', True, green)
    remove_message_white = menufont.render('remove', True, white)
    prev_message = smallfont.render('<---- prev page', True, green)
    next_message = smallfont.render('next page ---->', True, green)

    DISPLAY.blit(background_image, [0, 0])

    DISPLAY.blit(global_message, (400, 100))
    DISPLAY.blit(exit_message, (7.5 * WINDOWWIDTH / 10, 9 * WINDOWHEIGHT / 10))

    y_mult = 5
    x_offset = 30

    flag = -1

    point = 0
    length = len(tuples)

    change = True

    printed = False

    x = 0
    y = 0
    h = WINDOWHEIGHT
    x1 = 0
    y1 = -h

    hasNextPage = friend_remove_driver(user_name, -start - 5)

    while 1:

        for event in pygame.event.get():
            #quit
            if event.type == pygame.QUIT:
                db_manager.delete_from_online(connection, user_name)
                pygame.quit()
                sys.exit()

            #exit
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return -2

                elif event.key == pygame.K_UP:
                    point -= 1
                    change = True

                if event.key == pygame.K_DOWN:
                    point += 1
                    change = True

                if event.key == pygame.K_RIGHT:
                    #right
                    flag = friend_remove_driver(user_name, start + 5)
                    if flag == -2:
                        return -2
                    if flag == -7 :
                        return -7
                    if not flag == -3:
                        change = True
                        y_mult = 3

                if event.key == pygame.K_RETURN :
                    #remove friend
                    db_manager.delete_from_friends(connection, user_name, tuples[point][0])
                    db_manager.delete_from_friends(connection, tuples[point][0], user_name)
                    return -7

                if event.key == pygame.K_LEFT and not start == 0:
                    #left
                    DISPLAY.blit(background_image, [0, 0])
                    DISPLAY.blit(global_message, (400,100))
                    DISPLAY.blit(exit_message, (7.5 * WINDOWWIDTH / 10, 9 * WINDOWHEIGHT / 10))
                    print("left")
                    return -1

        if not start == 0:
            DISPLAY.blit(prev_message, (x_offset + WINDOWWIDTH / 10, 8 * WINDOWHEIGHT / 10))

        # print next page only if next page exists
        if hasNextPage == 1:
            DISPLAY.blit(next_message, (x_offset + WINDOWWIDTH * 6 / 10, 8 * WINDOWHEIGHT / 10))

        point %= length
        if change:
            DISPLAY.blit(background_image, [0, 0])
            DISPLAY.blit(global_message, (400,100))
            DISPLAY.blit(exit_message, (7.5 * WINDOWWIDTH / 10, 9 * WINDOWHEIGHT / 10))
            i = 0
            y_mult = 5
            for next_row in tuples:
                name = next_row[0]

                if (name == user_name):
                    continue
                else:
                    name = mediumfont.render(name, True, white)

                DISPLAY.blit(name, (x_offset + 470, y_mult * 60))
                if i == point :
                    DISPLAY.blit(remove_message_red, (x_offset + 875, y_mult * 60))
                else :
                    DISPLAY.blit(remove_message_white, (x_offset + 875, y_mult * 60))

                i += 1
                y_mult += 1
                pygame.display.flip()
                pygame.event.pump()
                #pygame.time.delay(200)

        change = False

        clock.tick(FPS)
        pygame.display.update()



