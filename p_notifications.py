import pygame

import db_manager
from p_global import *
from colors import *

def notifications_driver(user_name) :

    result = db_manager.get_notifications(connection, user_name)

    tuples = result[0]
    hasPending = result[1]

    if tuples == [] and hasPending == 0 :
        return

    print_notifications(user_name, tuples, hasPending)
    db_manager.remove_notification(connection, user_name)


def print_notifications(user_name, tuples, hasPending) :

    global_message = headfont.render('NOTIFICATIONS', True, red)
    exit_message = mediumfont.render('press esc to exit', True, red)
    pending_message = mediumfont.render("you have pending friend requests", True, green)

    y_mult = 5
    x_offset = 30

    hasPrinted = False

    DISPLAY.blit(background_image, [0, 0])
    DISPLAY.blit(global_message, (450, 100))
    DISPLAY.blit(exit_message, (7.5 * WINDOWWIDTH / 10, 9 * WINDOWHEIGHT / 10))

    x = 0
    y = 0
    h = WINDOWHEIGHT
    x1 = 0
    y1 = -h

    while 1:

        for event in pygame.event.get():
            # quit
            if event.type == pygame.QUIT:
                db_manager.delete_from_online(connection, user_name)
                pygame.quit()
                sys.exit()

            # exit
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return

            if not hasPrinted :
                for next_row in tuples:
                    name = next_row[1]

                    message = name + " has accepted your friend request"

                    message = mediumfont.render(message, True, green)

                    DISPLAY.blit(message, (x_offset + 275, y_mult * 60))

                    y_mult += 1
                    pygame.display.flip()
                    pygame.event.pump()


            if hasPending == 1  and not hasPrinted:
                DISPLAY.blit(pending_message, (x_offset + 175 , y_mult * 60))

            hasPrinted = True

        clock.tick(FPS)
        pygame.display.update()