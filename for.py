import os
import math
import pygame
import time 

MAX_LEVELS = 3

SCREEN_SIZE = (800,600)
FOX_STEP_TIME = 0.2
IMG3_STEP_TIME = 0.15
IMG3_FLY_TIME = 0.15


BLACK = (0, 0, 0)           # ������
SIRENEVYI = (198, 112, 156) # SIRENEVYI
WHITE = (255, 255, 255)     # �����
RED = (255, 0, 0)           # �������
GREEN = (0, 255, 0)         # �������
BLUE = (0, 0, 255)          # �����
CYAN = (0, 255, 255)        # ������� �����
MAGENTA = (255, 0, 255)     # ���������
YELLOW = (255, 255, 0)      # ������

karta = [
    "#########################",
    "#>                      #",
    "###<               ### ##",
    "#####      ##           #",
    "#      o        #       #",
    "#########################"
]

level = 0

res = {}

bonuses = []
total_bonuses = 0

img5 = {
    "x": 0,
    "y": 0,
    "dir": "."
}
img3 = {
    "x": 0,
    "y": 0,
    "dir": ".",
    "x_update": time.time(),
    "y_update": time.time(),
    "jumping": 0,
    "can_jump": False
}

def my_path():
    return os.path.abspath(os.path.dirname(__file__))

def path_to_file(filename):
    return os.path.join(my_path(), filename) 

def load_resourses():
    res["fon"] = pygame.image.load(path_to_file("ht.jpg"))
    res["fon"].convert()
    res["img1"] = pygame.image.load(path_to_file("wall.jpg"))
    res["img1"].convert()
    res["img2"] = pygame.image.load(path_to_file("PALTFORMA.jpg"))
    res["img2"].convert()
    res["img3"] = pygame.image.load(path_to_file("тiкай_на_скейте.png"))
    res["img3"].convert()
    res["img4"] = pygame.image.load(path_to_file("петрик.png"))
    res["img4"].convert()
    res["img5"] = pygame.image.load(path_to_file("fon.png"))
    res["img5"].convert()
    res["ht"] = pygame.image.load(path_to_file("ht.jpg"))
    res["ht"].convert()
    #pygame.mixer.music.load("music.mp3")
    #pygame.mixer.music.load("lvlpassed.mp3")
    #res["lvlpassed"] = pygame.mixer.Sound(path_to_file("lvlpassed.wav"))


def load_map(filename):
    global karta
    global SCREEN_SIZE

    with open(path_to_file(filename), "r") as f:
            s = f.read()
    karta = s.split("\n")

    SCREEN_SIZE = (len(karta[0])*32, len(karta)*32)

def setup_chars():
    global total_bonuses
    for i in range(len(karta)):
        for j in range(len(karta[i])):
            ch = karta[i][j]
            if ch == "%":
                img5["x"] = j*32
                img5["y"] = i*32    
            if ch == "$":
                img3["x"] = j*32
                img3["y"] = i*32
                img3["x_update"] = time.time()
            if ch == "*":
                bonuses.append({
                    "x": j*32,
                    "y": i*32
                })
                total_bonuses = total_bonuses + 1

def draw_img1(screen, x, y):
    screen.blit(res["img1"], (x,y))

def draw_img2(screen, x, y):
    screen.blit(res["img2"], (x,y))

def draw_img3(screen):
    screen.blit(res["img3"], (img3["x"],img3["y"]))

def draw_img4(screen,x,y):
    screen.blit(res["img4"], (x,y))

def draw_img5(screen):
    screen.blit(res["img5"], (img5["x"],img5["y"]))

def draw_map(screen):
    for i in range(len(karta)):
        for j in range(len(karta[i])):
            if karta[i][j] == "#":
                draw_img1(screen,j*32, i*32)
            if karta[i][j] == "@":
                draw_img2(screen,j*32, i*32)
            #if karta[i][j] == "*":
            #    draw_img4(screen,j*32, i*32)
            #if karta[i][j] == "%":
            #    draw_img5(screen,j*32, i*32)
            # if karta[i][j] == "$":z
            #     draw_img3(screen,j*32, i*32)

def move_img3_right():
    t = time.time()
    if t-img3["x_update"] >= IMG3_STEP_TIME:
        x = img3["x"] // 32
        y = img3["y"] // 32

        if karta[y][x+1] != "#":
            img3["x"] = img3["x"] + 32

        img3["x_update"] = t

def move_img3_left():
    t = time.time()
    if t-img3["x_update"] >= IMG3_STEP_TIME:
        x = img3["x"] // 32
        y = img3["y"] // 32

        if karta[y][x-1] != "#":
            img3["x"] = img3["x"] - 32

        img3["x_update"] = t
        
def move_img3_down():
    t = time.time()
    if t-img3["y_update"] >= IMG3_FLY_TIME:
        x = img3["x"] // 32
        y = img3["y"] // 32

        if (karta[y+1][x] != "#") and (karta[y+1][x] != "@"):
            img3["y"] = img3["y"] + 32
            img3["can_jump"] = False
        else:
            img3["can_jump"] = True

        img3["y_update"] = t

def move_img3_up():
    t = time.time()
    if t-img3["y_update"] >= IMG3_FLY_TIME:
        x = img3["x"] // 32
        y = img3["y"] // 32

        img3["y"] = img3["y"] - 32
        img3["jumping"] = img3["jumping"] - 1
        img3["y_update"] = t

def animate_img3():
    if img3["dir"] == ">":
       move_img3_right()
    if img3["dir"] == "<":
        move_img3_left()
    if img3["jumping"] > 0:
        move_img3_up()
    else:
        move_img3_down()   

def animate_frame():
    animate_img3()
    #pygame.mixer.music.play("music.mp3")

def draw_bonuses(screen):
    for bonus in bonuses:
        draw_img4(screen, bonus["x"], bonus["y"])
    

def draw_frame(screen):
    #screen.blit
    draw_img5(screen)
    draw_map(screen)
    draw_bonuses(screen)
    draw_img3(screen)

def control_img3(event):
    if event.type  == pygame.KEYDOWN:
        if event.key == pygame.K_d:
            img3["dir"] = ">"
        if event.key == pygame.K_a:
            img3["dir"] = "<"
        if event.key == pygame.K_SPACE:
            if img3["can_jump"]:
                img3["jumping"] = 2
    if event.type == pygame.KEYUP:
        if (event.key == pygame.K_d) or (event.key == pygame.K_a):
            img3["dir"] = "."

def game():
    global frame
    global total_bonuses
    global level
    pygame.mixer.pre_init(44100, 16, 2, 4096)
    pygame.init()

    load_map("map{}.txt".format(level+1))
    setup_chars()

    screen = pygame.display.set_mode(SCREEN_SIZE)

    pygame.display.set_caption("pygame")

    #img1 = pygame.image.load(path_to_file("KIRPICH.JPG"))
    #img2 = pygame.image.load(path_to_file("TRAVA.JPG"))
    #img1.convert()
    #img2.convert()

    load_resourses()

    #pygame.mixer.music.load(path_to_file("music.mp3"))
    #pygame.mixer.music.play()
       
    done = False

    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            if level >= 0 and level < MAX_LEVELS:
                control_img3(event)
            if level == MAX_LEVELS or level == MAX_LEVELS+1:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        level = 0
                        loag_map("map{}.txt".format(level+1))
                        setup_chars()

        if level >= 0 and level < MAX_LEVELS:
            animate_frame()

        animate_frame()

        for i, img5 in enumerate(bonuses):
            if (img3["x"] == img5["x"]) and (img3["y"] == img5["y"]):
                del bonuses[i]

        if len(bonuses) == 0:
                level = level + 1
                if level < MAX_LEVELS:
                    load_map("map{}.txt".format(level+1))
                    setup_chars()
        
        # if total_bonuses == 0:
        #     res["lvlpassed"].play()
        #     level == level + 1
        #     load_map("map2.txt")
        #     setup_chars()
        #     if total_bonuses == 0:
        #         res["lvlpassed"].play()
        #         level == level + 1
        #         load_map("map2.txt")
        #         setup_chars()

        # if (level == level + 1) and (total_bonuses == 0):
        #     res["lvlpassed"].play()
        #     level == level + 1
        #     load_map("map2.txt")
        #     setup_chars()
            #pygame.mixer.music.play("lvlpassed.mp3")


        #if level == 0:
        #    for total_bonuses in 
            
        screen.fill(WHITE)

        if level == MAX_LEVELS:
            screen.blit(res["ht"], (0,0))
        
        screen.blit(res["fon"], (0,0))
        if level >= 0 and level < MAX_LEVELS:
            draw_frame(screen)

        if level == MAX_LEVELS:
            screen.blit(res["ht"], (0,0))

        pygame.display.flip()

    pygame.quit()

game()