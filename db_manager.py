import mysql.connector
from mysql.connector import Error

#   CREATE SERVER CONNECTION    ########################################################################################
def create_server_connection(host_name, user_name, user_password) :

    #closing any existing connections
    connection = None

    #trying to connect to mysql database with given credentials
    try :
        connection = mysql.connector.connect(
            host = host_name,
            user = user_name,
            passwd = user_password
        )
        print("MySQL Database connection successful")

    # cannot connect
    except Error as err :
        print(f"Error : '{err}'")

    #returning a connection object
    return connection

########################################################################################################################
#####   CHECK TUPLE USER   #############################################################################################

def check_tuple_user(connection, user_name_a, user_name_b):

        # check if a, b exists
        query = "SELECT * FROM friend WHERE user_name_a = '" + user_name_a + "' and user_name_b = '" + user_name_b + "'"

        result = read_query(connection, query)

        if not result == None:
            if len(result) >= 1:
                return True
        else:
            return False

#   INSERT INTO USER   #################################################################################################

def insert_into_user(connection, user_name, password) :

    string1 = "INSERT INTO user VALUES('"
    string2 = "', '"
    string3 = "')"
    query = string1 + user_name + string2 + password + string3

    execute_query(connection, query)

    insert_into_friend(connection, user_name, user_name)

#   CHECK IF TUPLE EXISTS IN GAME_DATA_CAR    ##########################################################################

def check_tuple_game_data(connection, user_name_a, score, game) :

    #check if a, b exists
    query = "SELECT * FROM game_data_" + game + " WHERE user_name = '" + user_name_a + "' and score = '" + str(score) + "'"

    result = read_query(connection, query)

    if not result == None:
        if len(result) >= 1:
            return True
    else:
        return False


#   INSERT INTO GAME_DATA   ############################################################################################

def insert_into_game_data(connection, user_name, score, game) :
    
    flag = check_tuple_game_data(connection, user_name, score, game)

    if flag == True:
        return

    string1 = "INSERT INTO game_data_" + game + " VALUES('"
    string2 = "', '"
    string3 = "')"
    query = string1 + user_name + string2 + str(score) + string3

    execute_query(connection, query)
#   CHECK IF TUPLE EXISTS IN FRIEND     ################################################################################

def check_tuple_friend(connection, user_name_a, user_name_b) :

    #check if a, b exists
    query = "SELECT * FROM friend WHERE user_name_a = '" + user_name_a + "' and user_name_b = '" + user_name_b + "'"

    result = read_query(connection, query)

    if not result == None:
        if len(result) >= 1:
            return True
    else:
        return False

#   INSERT INTO FRIEND ACCEPTED   ###############################################################################################

def insert_into_friend_accepted(connection, user_name_a, user_name_b) :

    string1 = "INSERT IGNORE INTO friend_accepted VALUES('"
    string2 = "', '"
    string3 = "')"

    query1 = string1 + user_name_a + string2 + user_name_b + string3

    execute_query(connection, query1)

#   INSERT INTO FRIEND   ###############################################################################################

def insert_into_friend(connection, user_name_a, user_name_b) :

    string1 = "INSERT IGNORE INTO friend VALUES('"
    string2 = "', '"
    string3 = "')"

    query1 = string1 + user_name_a + string2 + user_name_b + string3
    query2 = string1 + user_name_b + string2 + user_name_a + string3

    execute_query(connection, query1)

    if not user_name_a == user_name_b :
        execute_query(connection, query2)


#   CHECK IF TUPLE EXISTS IN PENDING     ###############################################################################

def check_tuple_pending(connection, user_name_a, user_name_b):
    # check if a, b exists
    query = "SELECT * FROM friend_pending WHERE user_from = '" + user_name_a + "' and user_to = '" + user_name_b + "'"

    result = read_query(connection, query)

    if not result == None :
        if len(result) >= 1:
            return True
    else:
        return False


#   INSERT INTO PENDING   ##############################################################################################

def insert_into_pending(connection, user_name_a, user_name_b) :
    # same name
    if user_name_a == user_name_b:
        return -3

    flag = check_tuple_friend(connection, user_name_a, user_name_b)

    # friend already added
    if flag:
        return -1

    # alerady requested
    flag = check_tuple_pending(connection, user_name_a, user_name_b)
    flag2 = check_tuple_pending(connection, user_name_b, user_name_a)

    if flag2:
        return -6

    if flag:
        return -2

    string1 = "INSERT IGNORE INTO friend_pending VALUES('"
    string2 = "', '"
    string3 = "')"

    query1 = string1 + user_name_a + string2 + user_name_b + string3

    execute_query(connection, query1)

    return 1

#   CREATE DATABASE     ################################################################################################

def create_database(connection, query) :
    cursor = connection.cursor(buffered = True)

    try :
        cursor.execute(query)
        print("Database created successfully")
    except Error as err :
        print(f"Error : '{err}'")

#   EXECUTE QUERIES   ##################################################################################################

def execute_query(connection, query) :
    cursor = connection.cursor()

    try :
        cursor.execute(query)
        connection.commit()
        #print("Query executed successfully")
    except Error as err :
        print(f"Error : '{err}'")

#   READ QUERY   #######################################################################################################

def read_query(connection, query) :
    cursor = connection.cursor()
    result = None

    insert_into_online(connection, "dummy42069")

    try :
        cursor.execute(query)
        result = cursor.fetchall()
        return result
    except Error as err :
        print(f"Error : '{err}'")

#   VALIDATE PASSWORD   ################################################################################################

def validate_password(connection, username, password) :
    # return 0 on match
    # return -1 on wrong password
    # return 1 on usernmae not found

    query1 = "SELECT * FROM user WHERE user_name = '" + username + "'"
    result = read_query(connection, query1)

    if not len(result) == 1 :
        return 1

    query2 = "SELECT * FROM user WHERE user_name = '" + username + "' AND password = '" + password + "'"
    result = read_query(connection, query2)

    if not len(result) == 1 :
        return -1
    
    return 0

#   GET NOTIFS  ###################################################################################################################

def get_notifications(connection, user_name) :

    query = "SELECT * FROM friend_accepted WHERE user_name_a = '" + user_name + "';"
    result = read_query(connection, query)

    print(result)

    #check for any pending requests
    pending = get_pending_requests(connection, user_name)

    if pending == [] or pending is None :
        return [result, 0]
    else :
        return [result, 1]

#  REMOVE NOTIFICATIONS  ###################################################################################################################

def remove_notification(connection, user_name) :

    query = "DELETE FROM friend_accepted WHERE user_name_a = '" + user_name + "';"
    execute_query(connection, query)

#   VALIDATE FRIEND   ##################################################################################################

def validate_friend(connection, username):
    # return 0 on match
    # return -1 on friend not found

    query1 = "SELECT * FROM user WHERE user_name = '" + username + "'"
    result = read_query(connection, query1)

    if len(result) == 1:
        return 0

    else :
        return -1

########################################################################################################################
#   GET FRIENDS LEADERBOARD #############################################################################################

def get_leaderboard_friends(connection, user_name, game) :

    query = """SELECT DISTINCT user_name, MAX(score) as score FROM game_data_""" + game +  """ g 
               INNER JOIN friend f ON g.user_name = f.user_name_b and f.user_name_a = '"""
    query += user_name + "' GROUP BY user_name ORDER BY score DESC"

    result = read_query(connection, query)

    return result

########################################################################################################################
#   GET GLOBAL LEADERBOARD  ############################################################################################

def get_leaderboard_global(connection, game) :

    query = """SELECT DISTINCT user_name, MAX(score) as score FROM game_data_""" + game + """ 
            GROUP BY user_name ORDER BY score DESC"""
    result = read_query(connection, query)

    return result

########################################################################################################################
#   GET FRIENDS LIST    ################################################################################################

def get_friends_list(connection, username, start):

    #gets 5 friends from start(offset) in ascending order of names

    query = "SELECT user_name_b FROM friend WHERE user_name_a = '" + username
    query += "' and user_name_b != '" + username
    query += "' ORDER BY user_name_b ASC LIMIT 5 OFFSET " + str(start)

    result = read_query(connection, query)

    return result

########################################################################################################################
#   DELETE FROM FRIENDS    #############################################################################################

def delete_from_friends(connection, user_name_a, user_name_b) :

    query = "DELETE FROM friend WHERE user_name_a = '" + user_name_a + "' and user_name_b = '" + user_name_b + "'"
    execute_query(connection, query)

########################################################################################################################
#   GET PENDING REQUESTS    ############################################################################################

def get_pending_requests(connection, username):

    query = "SELECT user_from FROM friend_pending WHERE user_to = '" + username + "'"

    result = read_query(connection, query)

    return result

########################################################################################################################
#   REMOVE FROM PENDING    #############################################################################################

def remove_from_pending(connection, user_from, user_to):
    query = "DELETE FROM friend_pending WHERE user_from = '" + user_from + "' and user_to = '" + user_to + "'"

    execute_query(connection, query)

########################################################################################################################
#   INSERT INTO ONLINE   ###############################################################################################

def insert_into_online(connection, user_name) :
    string1 = "INSERT IGNORE INTO online VALUES('"
    string2 = "')"

    query = string1 + user_name + string2
    execute_query(connection, query)

########################################################################################################################
#   DELETE FROM ONLINE    ##############################################################################################

def delete_from_online(connection, user_name) :
    query = "DELETE FROM online WHERE user_name = '" + user_name + "'"

    execute_query(connection, query)

    print(user_name, " signing out")

########################################################################################################################
#   CHECK IF ONLINE    #################################################################################################

def check_if_online(connection, user_name) :

    query = "SELECT * FROM `online` WHERE user_name = '" + user_name + "'"

    result = read_query(connection, query)

    if result == [] or result == None :
        return False

    return True

#   CALL PROCEDURE  #####################################################################################################

def call_procedure(connection, procedure, args) :
    cursor = connection.cursor()
    cursor.callproc(procedure, args)

    result = []

    for row in cursor.stored_results():
        result.append(row.fetchall())

    return result

########################################################################################################################
#############################################     MAIN METHOD     ######################################################



