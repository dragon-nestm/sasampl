import os
import time
import math
import pygame

SCREEN_SIZE = (800, 600)
SCREEN_TITLE = "Kolobok Advenchers"

FOX_STEP_TIME = 0.3
KOLO_STEP_TIME = 0.3
KOLO_FLY_TIME = 0.2

karta = []

level = 0

res = {}
foxes = []
kolo = {
    "x": 0,
    "y": 0,
    "dir": ".",
    "x_update": time.time(),
    "y_update": time.time(),
    "jumping": 0,
    "can_jump": False
}

BLACK = (0, 0, 0)           # черный
WHITE = (255, 255, 255)     # белый
RED = (255, 0, 0)           # красный
GREEN = (0, 255, 0)         # зеленый
BLUE = (0, 0, 255)          # синий
CYAN = (0, 255, 255)        # морской волны
MAGENTA = (255, 0, 255)     # пурпурный
YELLOW = (255, 255, 0)      # желтый
NOS = (224, 49, 49)         #нос


def my_path():
    return os.path.abspath(os.path.dirname(__file__))

def path_to_file(filername):
    return os.path.join(my_path(), filername)

def load_resoursces():
    res["wall"] = pygame.image.load(path_to_file("1345.png"))
    res["wall"].convert()

def loag_map(filername):
    global karta
    global SCREEN_SIZE

    with open(path_to_file(filername), "r") as f:
        s = f.read()
    karta = s.split("\n")

    SCREEN_SIZE = (len(karta[0])*32, len(karta)*32)

def setup_chars():
    for i in range(len(karta)):
        for j in range(len(karta[i])):
            ch = karta[i][j]
            if ch == ">":
                foxes.append({
                    "dir": ">",
                    "legs": "v",
                    "x": j*32,
                    "y": i*32,
                    "x_update": time.time()
                })
            if ch == "<":
                foxes.append({
                    "dir": "<",
                    "legs": "v",
                    "x": j*32,
                    "y": i*32,
                    "x_update": time.time()
                })
            if ch == "o":
                kolo["x"] = j*32
                kolo["y"] = i*32
                kolo["x_update"] = time.time()




def draw_kolobok_normal(screen, x, y):
    pygame.draw.circle(screen, YELLOW, (x+16, y+18), 14, 0)
    pygame.draw.circle(screen, NOS, (x+10, y+16), 2, 0)
    pygame.draw.circle(screen, NOS, (x+22, y+16), 2, 0)
    pygame.draw.arc(screen, RED, (x+7, y+9, 20, 20), math.radians(225), math.radians(-45), 2)

def draw_kolobok_jump(screen, x, y):
    pygame.draw.ellipse(screen, YELLOW, (x+34, y+1, 25, 31), 0)
    pygame.draw.circle(screen, NOS, (x+41, y+9), 2, 0)
    pygame.draw.circle(screen, NOS, (x+50, y+9), 2, 0)
    pygame.draw.ellipse(screen, RED, (x+39, y+15, 17, 14), 2)

def draw_kolobok_land(screen, x, y):
    pygame.draw.ellipse(screen, YELLOW, (x+65, y+12, 31, 20), 0)
    pygame.draw.circle(screen, NOS, (x+73, y+19), 2, 0)
    pygame.draw.circle(screen, NOS, (x+88, y+19), 2, 0)
    pygame.draw.ellipse(screen, RED, (x+74, y+21, 15, 10), 2)

def draw_fox_right_v(screen, x, y):
    pygame.draw.polygon(screen, RED, [(x, y+2), (x+31, y+16), (x, y+26)], 0)
    pygame.draw.lines(screen, BLACK, False, [(x+4, y+22), (x, y+31), (x+4, y+31)], 2)
    pygame.draw.lines(screen, BLACK, False, [(x+4, y+22), (x+8, y+31), (x+12, y+31)], 2)

def draw_fox_right_l(screen, x, y):
    pygame.draw.polygon(screen, RED, [(x, y), (x+31, y+14), (x, y+24)], 0)
    pygame.draw.lines(screen, BLACK, False, [(x+4, y+22), (x+4, y+31), (x+8, y+31)], 2)

def draw_fox_left_v(screen, x, y):
    pygame.draw.polygon(screen, RED, [(x+31, y+2), (x, y+16), (x+31, y+26)], 0)
    pygame.draw.lines(screen, BLACK, False, [(x+27, y+22), (x+31, y+31), (x+27, y+31)], 2)
    pygame.draw.lines(screen, BLACK, False, [(x+27, y+22), (x+23, y+31), (x+18, y+31)], 2)

def draw_fox_left_l(screen, x, y):
    pygame.draw.polygon(screen, RED, [(x+31, y), (x, y+14), (x+31, y+24)], 0)
    pygame.draw.lines(screen, BLACK, False, [(x+27, y+22), (x+27, y+31), (x+23, y+31)], 2)
    
def draw_wall(screen, x, y):
    screen.blit(res["wall"], (x, y))

def draw_map(screen):
    for i in range(len(karta)):
        for j in range(len(karta[i])):
            if karta[i][j] == "#":
                draw_wall(screen, j*32, i*32)
            #if karta[i][j] == "o":
                #draw_kolobok_normal(screen, j*32, i*32)
            #if karta[i][j] == "<":
            #    draw_fox_left_v(screen, j*32, i*32)
            #if karta[i][j] == ">":
            #    draw_fox_right_v(screen, j*32, i*32)

def draw_kolobok(screen):
    draw_kolobok_normal(screen, kolo["x"], kolo["y"])

def draw_fox(screen, fox):
    if fox["dir"] == ">":
        if fox["legs"] == "v":
            draw_fox_right_v(screen, fox["x"], fox["y"])
        if fox["legs"] == "l":
            draw_fox_right_l(screen, fox["x"], fox["y"])
    if fox["dir"] == "<":
        if fox["legs"] == "v":
            draw_fox_left_v(screen, fox["x"], fox["y"])
        if fox["legs"] == "l":
            draw_fox_left_l(screen, fox["x"], fox["y"])


def draw_foxes(screen):
    for fox in foxes:
        draw_fox(screen, fox)

def change_fox_legs(fox):
    if fox["legs"] == "v":
        fox["legs"] = "l"
    else:
        fox["legs"] = "v"

def move_fox_right(fox):
    t = time.time()
    if t-fox["x_update"] >= FOX_STEP_TIME:
        x = fox["x"] // 32
        y = fox["y"] // 32
        if (karta[y][x+1] != "#") and (karta[y+1][x+1] == "#"):
            fox["x"] = fox["x"] + 32
        else:
            fox["dir"] = "<"
        change_fox_legs(fox)
        fox["x_update"] = t
    

def move_fox_left(fox):
    t = time.time()
    if t-fox["x_update"] >= FOX_STEP_TIME:
        x = fox["x"] // 32
        y = fox["y"] // 32
        if (karta[y][x-1] != "#") and (karta[y+1][x-1] == "#"):
            fox["x"] = fox["x"] - 32
        else:
            fox["dir"] = ">"
        change_fox_legs(fox)
        fox["x_update"] = t

def move_kolo_right():
    t = time.time()
    if t-kolo["x_update"] >= KOLO_STEP_TIME:
        x = kolo["x"] // 32
        y = kolo["y"] // 32

        if karta[y][x+1] != "#":
            kolo["x"] = kolo["x"] + 32

        kolo["x_update"] = t

def move_kolo_down():
    t = time.time()
    if t-kolo["y_update"] >= KOLO_FLY_TIME:
        x = kolo["x"] // 32
        y = kolo["y"] // 32

        if karta[y+1][x] != "#":
            kolo["y"] = kolo["y"] + 32
            kolo["can_jump"] = False
        else:
            kolo["can_jump"] = True

        kolo["y_update"] = t

def move_kolo_up():
    t = time.time()
    if t-kolo["y_update"] >= KOLO_FLY_TIME:
        x = kolo["x"] // 32
        y = kolo["y"] // 32

        kolo["y"] = kolo["y"] - 32
        kolo["jumping"] = kolo["jumping"] - 1
        kolo["y_update"] = t

def move_kolo_left():
    t = time.time()
    if t-kolo["x_update"] >= KOLO_STEP_TIME:
        x = kolo["x"] // 32
        y = kolo["y"] // 32

        if karta[y][x-1] != "#":
            kolo["x"] = kolo["x"] - 32

        kolo["x_update"] = t

def animate_kolobok():
    if kolo["dir"] == ">":
        move_kolo_right()
    if kolo["dir"] == "<":
        move_kolo_left()
    if kolo["jumping"] > 0:
        move_kolo_up()
    else:
        move_kolo_down()

def move_foxes():
    for fox in foxes:
        if fox["dir"] == ">":
            move_fox_right(fox)
        if fox["dir"] == "<":
            move_fox_left(fox)

def animate_frame():
    move_foxes()
    animate_kolobok()

def draw_frame(screen):
    draw_map(screen)
    draw_foxes(screen)
    draw_kolobok(screen)

def control_kolobok(event):
    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_d:
            kolo["dir"] = ">"
        if event.key == pygame.K_a:
            kolo["dir"] = "<"
        if event.key == pygame.K_SPACE:
            if kolo["can_jump"]:
                kolo["jumping"] = 2
    if event.type == pygame.KEYUP:
        if (event.key == pygame.K_d) or (event.key == pygame.K_a):
            kolo["dir"] = "."

def game():
    global level
    pygame.init()

    loag_map("map2.txt")
    setup_chars()

    screen = pygame.display.set_mode(SCREEN_SIZE)

    pygame.display.set_caption("змейка")

    img = pygame.image.load(path_to_file("1345.png"))
    img.convert()

    load_resoursces()

    done = False

    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            if level == 0:
                control_kolobok(event)

        if level == 0:
            animate_frame()


        for fox in foxes:
            if(kolo["x"] == fox["x"]) and (fox["y"] == kolo["y"]):
                level = 1

        # заполнить экран черным цветом
        screen.fill(WHITE)
        

        #
        # код рисования пишется здесь
        #
        for i in range(0, 800, 32):
            pygame.draw.line(screen, (128, 128, 128), (i, 0), (i, 600), 1)
        for j in range(0, 600, 32):
            pygame.draw.line(screen, (128, 128, 128), (0, j), (800, j), 1)#-это всё сетка(разметка)
        
        # draw_kolobok_normal(screen, 0, 0)
        # draw_fox_right_l(screen, 500, 500)
        # draw_fox_left_v(screen, 400, 400)
        # draw_fox_left_l(screen, 300, 300)
        # screen.blit(img, (96, 96))
        # screen.blit(img, (128, 96))
        # draw_kolobok_jump(screen, 32, 0)
        # draw_kolobok_land(screen, 32, 0)
        # draw_fox_right_v(screen, 96, 0)
        # screen.blit(img, (160, 96))
        # screen.blit(img, (192, 96))


        # вывести все нарисованное на экран
        draw_frame(screen)
    
        pygame.display.flip()

    pygame.quit()

game()

