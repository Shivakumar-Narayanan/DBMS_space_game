from p_global import *
from colors import *
import db_manager
from p_post_game_screens import *

########################################################################################################################
#   POST GAME PROCESSING    ############################################################################################

def post_game_processing(user_name, points, game) :

    result = get_highscore(connection, game)

    #if there are no entries in game_data yet
    if not result == [] :
        hs_name = result[0][0]
        hs_score = int(result[0][1])
    else :
        hs_name = "yourself"
        hs_score = -1

    # addding cur game's data to database
    db_manager.insert_into_game_data(connection, user_name, points, game)

    #calling appropriate screen
    if points >= hs_score :
        return post_game_screen(user_name, points, hs_score, hs_name, 1, game)

    else :
        return post_game_screen(user_name, points, hs_score, hs_name, 0, game)

########################################################################################################################
#   GET HIGHSCORE DETAILS   ############################################################################################

def get_highscore(connection, game) :
    # calling procedure get_highscore
    args = []
    args.append(game)
    result = db_manager.call_procedure(connection, 'get_highscore', args)

    if result == [] :
        return []

    return result[0]
