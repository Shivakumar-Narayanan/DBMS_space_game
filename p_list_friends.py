import pygame
from p_global import *
from colors import *
import db_manager

def list_friends_driver(user_name, start) :

    # start = offset
    # function queries friend and gets the next 5 rows starting from offset
    # if result is none, then return -3
    # otherwise flag = list_friends(start, result)
    # if flag is -1, then return -1
    # if flag is -2, then return -2

    # if start is -1, then we are trying to check if there is another page of friends
    # so cehck and return -3 if none and return 1 if there is

    if start < 0 :
        result = db_manager.get_friends_list(connection, user_name, -start)
        if result == [] or result == None :
            return -3
        else :
            return 1

    result = db_manager.get_friends_list(connection, user_name, start)

    if result == [] :
        if start == 0 :
            #   no friends  #
            print("no friends")
        else :
            return -3

    if start == -1 :
        return 1

    flag = list_friends(user_name, start, result)

    return flag

def list_friends(user_name, start, tuples) :

    #prints tuples
    # if right arrow, flag =  a(start + 10)
    # if left, return -1
    # if escape is pressed, -2 is returned and thats a signal to return -2 again to exit all the way back
    # if flag = -2, return -2

    global_message = headfont.render('YOUR FRIENDS', True, red)
    exit_message = smallfont.render('press esc to exit', True, red)
    online_message = menufont.render('*online*', True, green)
    offline_message = menufont.render('*offline*', True, red)
    prev_message = smallfont.render('<---- prev page', True, green)
    next_message = smallfont.render('next page ---->', True, green)

    DISPLAY.blit(background_image, [0, 0])

    DISPLAY.blit(global_message, (450,100))
    DISPLAY.blit(exit_message, (7.5 * WINDOWWIDTH / 10, 9 * WINDOWHEIGHT / 10))

    y_mult = 5
    x_offset = 30

    flag = -1

    hasNextPage = list_friends_driver(user_name, -start - 5)

    print(hasNextPage)

    printed = False

    x = 0
    y = 0
    h = WINDOWHEIGHT
    x1 = 0
    y1 = -h

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

                if event.key == pygame.K_RIGHT:
                    print("right")

                    #DISPLAY.blit(background_image, [0, 0])
                    flag = list_friends_driver(user_name, start + 5)
                    if flag == -2 :
                        return -2
                    if not flag == -3 :
                        printed = False
                        y_mult = 3

                if event.key == pygame.K_LEFT and not start == 0:
                    #DISPLAY.blit(background_image, [0, 0])

                    DISPLAY.blit(global_message, (450, 100))
                    DISPLAY.blit(exit_message, (7.5 * WINDOWWIDTH / 10, 9 * WINDOWHEIGHT / 10))
                    print("left")
                    return -1

            if not printed:
                for next_row in tuples:
                    name = next_row[0]

                    if (name == user_name):
                        continue
                    else:
                        print(name)
                        name = mediumfont.render(name, True, lime)

                    DISPLAY.blit(name, (x_offset + 450, y_mult * 60))

                    #checking if friend is online
                    online_flag = db_manager.check_if_online(connection, next_row[0])

                    if online_flag :
                        DISPLAY.blit(online_message, (x_offset + 800, y_mult * 60))
                    else :
                        DISPLAY.blit(offline_message, (x_offset + 800, y_mult * 60))

                    #print prev for pages 2 - n and back for first page
                    if not start == 0 :
                        DISPLAY.blit(prev_message, (x_offset + WINDOWWIDTH / 10, 8 *WINDOWHEIGHT / 10))

                    #print next page only if next page exists
                    if hasNextPage == 1 :
                        DISPLAY.blit(next_message, (x_offset + WINDOWWIDTH * 6 / 10, 8 * WINDOWHEIGHT / 10))

                    y_mult += 1
                    pygame.display.flip()
                    pygame.event.pump()
                    pygame.time.delay(0)

            printed = True

        clock.tick(FPS)
        pygame.display.update()



