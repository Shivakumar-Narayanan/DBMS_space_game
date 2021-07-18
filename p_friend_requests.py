import pygame
from p_global import *
from colors import *
import db_manager

def friend_request(user_name):

    list_of_tuples = db_manager.get_pending_requests(connection, user_name)

    if list_of_tuples == [] or list_of_tuples == None :
        return -4

    point_x = 0
    point_y = 0

    friend_request = headfont.render('Friend Requests', True, red)
    exit_message = smallfont.render('press esc to exit', True, red)

    DISPLAY.blit(background_image, [0, 0])
    DISPLAY.blit(friend_request, (450, 100))
    DISPLAY.blit(exit_message, (7.5 * WINDOWWIDTH / 10, 9 * WINDOWHEIGHT / 10))

    length = len(list_of_tuples)

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
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DOWN:
                    point_y += 1
                elif event.key == pygame.K_UP:
                    point_y -= 1
                elif event.key == pygame.K_RIGHT:
                    point_x += 1
                elif event.key == pygame.K_LEFT:
                    point_x -= 1

                elif event.key == pygame.K_ESCAPE:
                        return
                elif event.key == pygame.K_RETURN:
                    # accept friend request
                    if point_x == 0:
                        request_accepted(list_of_tuples[point_y][0], user_name)

                    elif point_x == 1:
                        #reject friend request
                        request_rejected(list_of_tuples[point_y][0], user_name)

                    list_of_tuples = db_manager.get_pending_requests(connection, user_name)

                    #DISPLAY.blit(background_image, [0, 0])
                    y1 += 2
                    y += 2

                    DISPLAY.blit(background_image, (x, y))
                    DISPLAY.blit(background_image, (x1, y1))

                    if y > h:
                        y = -h
                    if y1 > h:
                        y1 = -h
                    DISPLAY.blit(friend_request, (450, 100))
                    DISPLAY.blit(exit_message, (7.5 * WINDOWWIDTH / 10, 9 * WINDOWHEIGHT / 10))

                    point_y += 1
                    if list_of_tuples == [] or list_of_tuples == None:
                        return
                    length = len(list_of_tuples)



        point_x = point_x % 2
        point_y = point_y % length

        count = 0
        i = 5

        for tup in list_of_tuples:

            if(count==point_y):
                friend_name = mediumfont.render(tup[0], True, lime)
                if point_x == 0:
                    yes = menufont.render('YES', True, cyan)
                    no = menufont.render('NO', True, white)
                if point_x == 1:
                    yes = menufont.render('YES', True, white)
                    no = menufont.render('NO', True, cyan)

            else :
                friend_name = mediumfont.render(tup[0], True, lime)
                yes = menufont.render('YES', True, white)
                no = menufont.render('NO', True, white)

            DISPLAY.blit(friend_name, (450, i * 60))
            DISPLAY.blit(yes, (900, i * 60))
            DISPLAY.blit(no, (1025, i * 60))
            i=i+1
            count += 1

        clock.tick(FPS)
        pygame.display.update()

def request_accepted(user_from, user_to) :
    # add to friends user_from ,user_to
    # remove from pending user_from, user_to
    db_manager.insert_into_friend(connection, user_from, user_to)
    db_manager.remove_from_pending(connection, user_from, user_to)

    #inserting into frind_accepted
    db_manager.insert_into_friend_accepted(connection, user_from, user_to)

def request_rejected(user_from, user_to) :
    # remove from pending user_from, user_to
    db_manager.remove_from_pending(connection, user_from, user_to)
