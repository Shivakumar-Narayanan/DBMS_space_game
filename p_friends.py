import pygame
from p_global import *
from colors import *
import db_manager
from p_list_friends import *
from p_add_friends import *
from p_friend_requests import *
from p_remove_friend import *
from p_notifications import *

def friend_screen(user_name, status) :

    point = 0
    flag = 0
    friend_added = smallfont.render('friend request sent', True, green)
    already_requested = smallfont.render('request already sent', True, green)
    already_added = smallfont.render('player is already a friend', True, green)
    its_you = smallfont.render('cant add yourself bruh', True, green)
    no_requests = smallfont.render('no pending requests', True, red)
    no_friends = smallfont.render('no friends to remove', True, red)
    check_pending = smallfont.render('check pending requests', True, red)
    friend_removed = smallfont.render('friend removed', True, red)

    x = 0
    y = 0
    h = WINDOWHEIGHT
    x1 = 0
    y1 = -h

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

        game_title = titlefont.render("AlternitY", True, red)
        message1 = headingfont.render('Manage Friends', True, green)

        DISPLAY.blit(message1, (600, 350))
        DISPLAY.blit(game_title, (1.3 * WINDOWWIDTH / 5, 100))

        if status == 1:
            DISPLAY.blit(friend_added, (4 * WINDOWWIDTH / 10, 9 * WINDOWHEIGHT / 10))
        if point == 0:
            view_friends = menufont.render('VIEW FRIENDS', True, cyan)
            add_friends = menufont.render('ADD FRIENDS', True, white)
            friend_requests = menufont.render('FRIEND REQUESTS', True, white)
            remove_friends = menufont.render('REMOVE FRIENDS', True, white)
            back = menufont.render('GO BACK', True, white)

        elif point == 1:
            view_friends = menufont.render('VIEW FRIENDS', True, white)
            add_friends = menufont.render('ADD FRIENDS', True, cyan)
            friend_requests = menufont.render('FRIEND REQUESTS', True, white)
            remove_friends = menufont.render('REMOVE FRIENDS', True, white)
            back = menufont.render('GO BACK', True, white)

        elif point == 2:
            view_friends = menufont.render('VIEW FRIENDS', True, white)
            add_friends = menufont.render('ADD FRIENDS', True, white)
            friend_requests = menufont.render('FRIEND REQUESTS', True, cyan)
            remove_friends = menufont.render('REMOVE FRIENDS', True, white)
            back = menufont.render('GO BACK', True, white)

        elif point == 3:
            view_friends = menufont.render('VIEW FRIENDS', True, white)
            add_friends = menufont.render('ADD FRIENDS', True, white)
            friend_requests = menufont.render('FRIEND REQUESTS', True, white)
            remove_friends = menufont.render('REMOVE FRIENDS', True, cyan)
            back = menufont.render('GO BACK', True, white)

        elif point == 4 :
            view_friends = menufont.render('VIEW FRIENDS', True, white)
            add_friends = menufont.render('ADD FRIENDS', True, white)
            friend_requests = menufont.render('FRIEND REQUESTS', True, white)
            remove_friends = menufont.render('REMOVE FRIENDS', True, white)
            back = menufont.render('GO BACK', True, cyan)

        DISPLAY.blit(view_friends, (500,450))
        DISPLAY.blit(add_friends, (500,500))
        DISPLAY.blit(friend_requests, (500,550))
        DISPLAY.blit(remove_friends, (500,600))
        DISPLAY.blit(back, (500,650))
        if flag == 1 :
            DISPLAY.blit(friend_added, (WINDOWWIDTH * 7 / 10, 9 * WINDOWHEIGHT / 10))
        elif flag == -1 :
            DISPLAY.blit(already_added, (WINDOWWIDTH * 7 / 10, 9 * WINDOWHEIGHT / 10))
        elif flag == -2 :
            DISPLAY.blit(already_requested, (WINDOWWIDTH * 7 / 10, 9 * WINDOWHEIGHT / 10))
        elif flag == -3 :
            DISPLAY.blit(its_you, (WINDOWWIDTH * 7 / 10, 9 * WINDOWHEIGHT / 10))
        elif flag == -4 :
            DISPLAY.blit(no_requests, (WINDOWWIDTH * 7 / 10, 9 * WINDOWHEIGHT / 10))
        elif flag == -5:
            DISPLAY.blit(no_friends, (WINDOWWIDTH * 7 / 10, 9 * WINDOWHEIGHT / 10))
        elif flag == -6 :
            DISPLAY.blit(check_pending, (WINDOWWIDTH * 7 / 10, 9 * WINDOWHEIGHT / 10))
        elif flag == -7:
            DISPLAY.blit(friend_removed, (WINDOWWIDTH * 7 / 10, 9 * WINDOWHEIGHT / 10))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                db_manager.delete_from_online(connection, user_name)
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE :
                    return 0
                elif event.key == pygame.K_DOWN:
                    point += 1
                elif event.key == pygame.K_UP:
                    point -= 1
                elif event.key == pygame.K_RETURN:

                    if point == 0:
                        ########    view friends ############
                        list_friends_driver(user_name, 0)

                    elif point == 1:
                        ########    add friends ###########
                        # if flag is 1, then print request sent
                        flag = add_friend_screen(0, user_name)

                    elif point == 2:
                        ########    friend requests ############
                        flag = friend_request(user_name)

                    elif point == 3 :
                        ######## remove friends ###########
                        flag = friend_remove_driver(user_name, 0)

                    elif point == 4 :
                        ######## back   ##########
                        return

        point = point % 5
        clock.tick(FPS)
        pygame.display.update()