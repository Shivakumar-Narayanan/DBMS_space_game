import sys, pygame , random, time
import db_manager
from pygame import mixer

########################################################################################################################
#   GLOBAL VARIABLES    ################################################################################################

pw = "MbfO3jp7EYtzo4lmtcPb"
uname = "ug7ry83gvomeakvh"
connection = db_manager.create_server_connection("bjmfhj5srdttznativgd-mysql.services.clever-cloud.com", uname, pw)

use_db_query = "USE bjmfhj5srdttznativgd"
db_manager.execute_query(connection, use_db_query)

pygame.init()
WINDOWWIDTH = 1550
WINDOWHEIGHT = 810

FPS = 50

user_id = 0
user_name = None

"""CARWIDTH = WINDOWWIDTH / 9
CARHEIGHT = WINDOWHEIGHT / 4
RECTWIDTH = WINDOWWIDTH / 32
RECTHEIGHT = WINDOWHEIGHT / 16
COINSIZE = WINDOWWIDTH / 24
YDIFF = WINDOWHEIGHT / 8"""

STEP = 5

white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)
lime = (180,255,100)
cyan = (0, 255, 255, 255)
dark_blue = (72, 61, 139, 255)
pink = (255, 192, 203, 255)
light_red = (230,103,113)

clock = pygame.time.Clock()
DISPLAY = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))

background_image = pygame.image.load('Assets/spaacebg.jpg').convert()
background_image_2 = pygame.image.load('Assets/space_background_2.PNG').convert()
background_image_3 = pygame.image.load('Assets/space_background_3.PNG').convert()

point_sound = pygame.mixer.Sound('Assets/eat.ogg')

smallfont = pygame.font.Font("Assets/font.ttf", 18)
menufont = pygame.font.Font("Assets/font.ttf", 28)
mediumfont = pygame.font.Font("Assets/font.ttf", 36)
headingfont = pygame.font.Font("Assets/font.ttf", 42)
titlefont = pygame.font.Font("Assets/font.ttf", 130)
italicfont = pygame.font.Font("Assets/space_font.otf", 40)
headfont = pygame.font.Font("Assets/font.ttf", 70)
headfont2 = pygame.font.Font("Assets/font.ttf", 55)
scorefont = pygame.font.Font("Assets/scorefont.ttf", 38)
#overfont = pygame.font.Font(None, 40)

pygame.display.set_caption("ALTERNITY")



mixer.music.load('Assets/bg_music_2.mp3')
mixer.music.set_volume(0.1)
#mixer.music.play(-1)

