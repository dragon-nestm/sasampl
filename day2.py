import os
import time
from math import radians
import pygame

SCREEN_SIZE = (800, 600)
SCREEN_TITLE = "Kolobok Adventures"

FOX_STEP_TIME = 0.3
KOLO_STEP_TIME = 0.3
KOLO_FLY_TIME = 0.2

level = 0

frame = 0

karta = [
    "##########",
    "#   >    #",
    "#  ###   #",
    "#      o #",
    "##########"
]

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

def my_path():
    return os.path.abspath(os.path.dirname(__file__))

def path_to_file(filename):
    return os.path.join(my_path(), filename)

def load_resources():
    res["wall"] = pygame.image.load(path_to_file("1345.png"))
    res["wall"].convert()

def load_map(filename):
    global karta
    global SCREEN_SIZE

    with open(path_to_file(filename), "r") as f:
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
    pygame.draw.circle(screen, (255, 255, 150), (x+16, y+20), 12)
    pygame.draw.circle(screen, (0, 0, 0), (x+12, y+16), 2, 1)
    pygame.draw.circle(screen, (0, 0, 0), (x+20, y+16), 2, 1)
    pygame.draw.arc(screen, (0, 0, 0), (x+10, y+16, 12, 9), radians(-135), radians(-30), 1)

def draw_kolobok_jump(screen, x, y):
    pygame.draw.ellipse(screen, (255, 255, 150), (x+4, y+0, 24, 32))
    pygame.draw.circle(screen, (0, 0, 0), (x+12, y+10), 2, 1)
    pygame.draw.circle(screen, (0, 0, 0), (x+20, y+10), 2, 1)
    pygame.draw.ellipse(screen, (0, 0, 0), (x+10, y+16, 12, 9), 1)

def draw_kolobok_land(screen, x, y):
    pygame.draw.ellipse(screen, (255, 255, 150), (x+0, y+12, 32, 20))
    pygame.draw.circle(screen, (0, 0, 0), (x+8, y+18), 2, 1)
    pygame.draw.circle(screen, (0, 0, 0), (x+24, y+18), 2, 1)
    pygame.draw.ellipse(screen, (0, 0, 0), (x+10, y+20, 12, 9), 1)

def draw_fox_right_v(screen, x, y):
    pygame.draw.polygon(screen, (255, 69, 0), [(x, y+2), (x+31, y+16), (x, y+26)])
    pygame.draw.lines(screen, (0, 0, 0), False, [(x+4, y+22), (x, y+31), (x+4, y+31)], 2)
    pygame.draw.lines(screen, (0, 0, 0), False, [(x+4, y+22), (x+8, y+31), (x+12, y+31)], 2)

def draw_fox_right_l(screen, x, y):
    pygame.draw.polygon(screen, (255, 69, 0), [(x, y), (x+31, y+14), (x, y+24)])
    pygame.draw.lines(screen, (0, 0, 0), False, [(x+4, y+22), (x+4, y+31), (x+8, y+31)], 2)

def draw_fox_left_v(screen, x, y):
    pygame.draw.polygon(screen, (255, 69, 0), [(x+31, y+2), (x, y+16), (x+31, y+26)])
    pygame.draw.lines(screen, (0, 0, 0), False, [(x+27, y+22), (x+31, y+31), (x+27, y+31)], 2)
    pygame.draw.lines(screen, (0, 0, 0), False, [(x+27, y+22), (x+23, y+31), (x+18, y+31)], 2)

def draw_fox_left_l(screen, x, y):
    pygame.draw.polygon(screen, (255, 69, 0), [(x+31, y), (x, y+14), (x+31, y+24)])
    pygame.draw.lines(screen, (0, 0, 0), False, [(x+27, y+22), (x+27, y+31), (x+23, y+31)], 2)

def draw_wall(screen, x, y):
    screen.blit(res["wall"], (x, y))

def draw_map(screen):
    for i in range(len(karta)):
        for j in range(len(karta[i])):
            if karta[i][j] == "#":
                draw_wall(screen, j*32, i*32)
            # if karta[i][j] == "o":
            #     draw_kolobok_normal(screen, j*32, i*32)
            # if karta[i][j] == "<":
            #     draw_fox_left_v(screen, j*32, i*32)
            # if karta[i][j] == ">":
            #     draw_fox_right_v(screen, j*32, i*32)

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

def move_kolo_left():
    t = time.time()
    if t-kolo["x_update"] >= KOLO_STEP_TIME:
        x = kolo["x"] // 32
        y = kolo["y"] // 32

        if karta[y][x-1] != "#":
            kolo["x"] = kolo["x"] - 32

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

    load_map("map2.txt")
    setup_chars()

    screen = pygame.display.set_mode(SCREEN_SIZE)

    pygame.display.set_caption(SCREEN_TITLE)

    #img = pygame.image.load(path_to_file("wall.jpg"))
    #img.convert()

    load_resources()

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
            if (fox["x"] == kolo["x"]) and (fox["y"] == kolo["y"]):
                level = 1

        screen.fill((135, 206, 235))

        # draw_frame(screen)
        # screen.blit(img, (0, 96))
        # screen.blit(img, (32, 96))
        # screen.blit(img, (64, 96))
        draw_frame(screen)

        if level == 1:
            pygame.draw.line(screen, (255, 0, 0), (0, 0), SCREEN_SIZE, 10)
            pygame.draw.line(screen, (255, 0, 0), (SCREEN_SIZE[0], 0), (0, SCREEN_SIZE[1]), 10)

        pygame.display.flip()

    pygame.quit()

game()
