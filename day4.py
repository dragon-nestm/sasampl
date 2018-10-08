import os
import time
from math import radians
import pygame

SCREEN_SIZE = (800, 600)
SCREEN_TITLE = "Kolobok Adventures"

FOX_STEP_TIME = 0.3
KOLOBOK_STEP_TIME = 0.3
KOLOBOK_FLY_TIME = 0.2

TILE_SIZE = 32

res = {}
field = []

done = False

foxes = []
stars = []
kolo = {
    "skin": "o",
    "x_dir": ".", # ".", ">" or "<"
    "can_jump": True,
    "jumping": 0,
    "x": 0,
    "y": 0,
    "last_x_update": time.time(),
    "last_y_update": time.time(),
    "last_jump_update": time.time()
}

total_stars = 0

def my_path():
    return os.path.abspath(os.path.dirname(__file__))

def path_to_file(filename):
    return os.path.join(my_path(), filename)

def load_resources():
    res["wall"] = pygame.image.load(path_to_file("wall.jpg"))
    res["wall"].convert()
    res["star"] = pygame.image.load(path_to_file("star.png"))
    res["star"].convert()
    res["font"] = pygame.font.Font("Kinda 3D.ttf", 24)
    res["score"] = res["font"].render("Score: 0", True, (0, 255, 0))

def load_map(filename):
    global field
    global SCREEN_SIZE

    with open(path_to_file(filename), "r") as f:
        s = f.read()
    field = s.split('\n')

    SCREEN_SIZE = (len(field[0]) * 32, len(field) * 32)

def setup_characters():
    global kolo
    global total_stars

    t = time.time()

    for i, row in enumerate(field):
        for j, ch in enumerate(row):
            if ch == '>':
                foxes.append({
                    "skin": ">",
                    "legs": "v",
                    "x": j*TILE_SIZE,
                    "y": i*TILE_SIZE,
                    "last_x_update": t,
                    "last_legs_update": t
                })
            elif ch == '<':
                foxes.append({
                    "skin": "<",
                    "legs": "v",
                    "x": j*TILE_SIZE,
                    "y": i*TILE_SIZE,
                    "last_x_update": t,
                    "last_legs_update": t
                })
            elif ch == 'o':
                kolo = {
                    "skin": "o",
                    "x_dir": ".",
                    "can_jump": True,
                    "jumping": 0,
                    "x": j*TILE_SIZE,
                    "y": i*TILE_SIZE,
                    "last_x_update": t,
                    "last_y_update": t,
                    "last_jump_update": t
                }
            elif ch == "*":
                stars.append({
                    "x": j*TILE_SIZE,
                    "y": i*TILE_SIZE
                })

    total_stars = len(stars)

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

def draw_brick(screen, x, y):
    screen.blit(res["wall"], (x, y))

def draw_star(screen, x, y):
    screen.blit(res["star"], (x, y))

def draw_score(screen, x, y):
    screen.blit(res["score"], (x, y))

def draw_stars(screen):
    for star in stars:
        draw_star(screen, star["x"], star["y"])

def draw_foxes(screen):
    for fox in foxes:
        if fox["skin"] == '>':
            if fox["legs"] == 'v':
                draw_fox_right_v(screen, int(fox["x"]), int(fox["y"]))
            elif fox["legs"] == 'l':
                draw_fox_right_l(screen, int(fox["x"]), int(fox["y"]))
        elif fox["skin"] == '<':
            if fox["legs"] == 'v':
                draw_fox_left_v(screen, int(fox["x"]), int(fox["y"]))
            elif fox["legs"] == 'l':
                draw_fox_left_l(screen, int(fox["x"]), int(fox["y"]))

def draw_kolobok(screen):
    if kolo["skin"] == 'o':
        draw_kolobok_normal(screen, int(kolo["x"]), int(kolo["y"]))
    elif kolo["skin"] == '0':
        draw_kolobok_jump(screen, int(kolo["x"]), int(kolo["y"]))
    elif kolo["skin"] == '@':
        draw_kolobok_land(screen, int(kolo["x"]), int(kolo["y"]))

def draw_map(screen):
    for i, row in enumerate(field):
        for j, ch in enumerate(row):
            if ch == "#":
                draw_brick(screen, j*32, i*32)

def smooth_offset(required_time, current_time, required_offset):
    val = (required_offset / required_time) * current_time
    max_val = TILE_SIZE - 2
    return max_val if val > max_val else val

def next_fox_animation(fox):
    if fox["legs"] == "v":
        return "l"
    return "v"

def approximately(val1, val2):
    if abs(val1 - val2) < 1:
        return True

def fox_matrix_x(fox):
    x = fox["x"] // TILE_SIZE
    if not approximately(fox["x"], x*TILE_SIZE):
        return int(x), False
    return int(x), True

def fox_matrix_y(fox):
    y = fox["y"] // TILE_SIZE
    if not approximately(fox["y"], y*TILE_SIZE):
        return int(y), False
    return int(y), True

def move_fox_right(fox_num):
    t = time.time()

    fox = foxes[fox_num]

    x, complete_x = fox_matrix_x(fox)
    y, _ = fox_matrix_y(fox)

    if complete_x:
        if ((fox["x"]+TILE_SIZE) >= SCREEN_SIZE[0]) or (field[y+1][x+1] != "#") or (field[y][x+1] == "#"):
            fox["skin"] = "<"
        else:
            fox["x"] = fox["x"] + smooth_offset(FOX_STEP_TIME, t-fox["last_x_update"], TILE_SIZE)
    else:
        fox["x"] = fox["x"] + smooth_offset(FOX_STEP_TIME, t-fox["last_x_update"], TILE_SIZE)

    fox["last_x_update"] = t

    if t-fox["last_legs_update"] >= FOX_STEP_TIME:
        fox["legs"] = next_fox_animation(fox)
        fox["last_legs_update"] = t

def move_fox_left(fox_num):
    t = time.time()

    fox = foxes[fox_num]

    x, complete_x = fox_matrix_x(fox)
    y, _ = fox_matrix_y(fox)

    if complete_x:
        if ((fox["x"]-TILE_SIZE) < 0) or (field[y+1][x-1] != "#") or (field[y][x-1] == "#"):
            fox["skin"] = ">"
        else:
            fox["x"] = fox["x"] - smooth_offset(FOX_STEP_TIME, t-fox["last_x_update"], TILE_SIZE)
    else:
        fox["x"] = fox["x"] - smooth_offset(FOX_STEP_TIME, t-fox["last_x_update"], TILE_SIZE)

    fox["last_x_update"] = t

    if t-fox["last_legs_update"] >= FOX_STEP_TIME:
        fox["legs"] = next_fox_animation(fox)
        fox["last_legs_update"] = t

def animate_foxes():
    for i, fox in enumerate(foxes):
        if fox["skin"] == ">":
            move_fox_right(i)
        elif fox["skin"] == "<":
            move_fox_left(i)

def kolo_matrix_x():
    x = kolo["x"] // TILE_SIZE
    if not approximately(kolo["x"], x*TILE_SIZE):
        return int(x), False
    return int(x), True

def kolo_matrix_y():
    y = kolo["y"] // TILE_SIZE
    if not approximately(kolo["y"], y*TILE_SIZE):
        return int(y), False
    return int(y), True

def move_kolo_right():
    t = time.time()

    x, complete_x = kolo_matrix_x()
    y, _ = kolo_matrix_y()

    if complete_x:
        if ((kolo["x"]+TILE_SIZE) < SCREEN_SIZE[0]) and (field[y][x+1] != "#"):
            kolo["x"] = kolo["x"] + smooth_offset(KOLOBOK_STEP_TIME, t-kolo["last_x_update"], TILE_SIZE)
    else:
        kolo["x"] = kolo["x"] + smooth_offset(KOLOBOK_STEP_TIME, t-kolo["last_x_update"], TILE_SIZE)

    kolo["last_x_update"] = t

def move_kolo_left():
    t = time.time()

    x, complete_x = kolo_matrix_x()
    y, _ = kolo_matrix_y()

    if complete_x:
        if ((kolo["x"]-TILE_SIZE) >= 0) and (field[y][x-1] != "#"):
            kolo["x"] = kolo["x"] - smooth_offset(KOLOBOK_STEP_TIME, t-kolo["last_x_update"], TILE_SIZE)
    else:
        kolo["x"] = kolo["x"] - smooth_offset(KOLOBOK_STEP_TIME, t-kolo["last_x_update"], TILE_SIZE)

    kolo["last_x_update"] = t

def move_kolo_up():
    t = time.time()

    x, _ = kolo_matrix_x()
    y, complete_y = kolo_matrix_y()

    if complete_y:
        if kolo["jumping"] == 0:
            kolo["skin"] = "@"
        else:
            kolo["skin"] = "0"
            kolo["y"] = kolo["y"] - smooth_offset(KOLOBOK_FLY_TIME, t-kolo["last_y_update"], TILE_SIZE)
        if t-kolo["last_jump_update"] > KOLOBOK_FLY_TIME / 2:
            kolo["jumping"] = kolo["jumping"] - 1
            kolo["last_jump_update"] = t
    else:
        kolo["y"] = kolo["y"] - smooth_offset(KOLOBOK_FLY_TIME, t-kolo["last_y_update"], TILE_SIZE)

    kolo["last_y_update"] = t

def move_kolo_down():
    t = time.time()

    x, _ = kolo_matrix_x()
    y, complete_y = kolo_matrix_y()

    if complete_y:
        if ((kolo["y"]+TILE_SIZE) < SCREEN_SIZE[1]) and (field[y+1][x] != "#"):
            kolo["skin"] = "@"
            kolo["y"] = kolo["y"] + smooth_offset(KOLOBOK_FLY_TIME, t-kolo["last_y_update"], TILE_SIZE)
    else:
        kolo["y"] = kolo["y"] + smooth_offset(KOLOBOK_FLY_TIME, t-kolo["last_y_update"], TILE_SIZE)

    kolo["last_y_update"] = t

def animate_kolobok():
    if kolo["jumping"] > 0:
        move_kolo_up()
    else:
        x, _ = kolo_matrix_x()
        y, complete_y = kolo_matrix_y()

        if complete_y and field[y+1][x] == "#":
            kolo["can_jump"] = True
            kolo["skin"] = "o"
            kolo["last_y_update"] = time.time()
        else:
            kolo["can_jump"] = False
            move_kolo_down()

    if kolo["x_dir"] == ">":
        move_kolo_right()
    elif kolo["x_dir"] == "<":
        move_kolo_left()
    elif kolo["x_dir"] == ".":
        kolo["last_x_update"] = time.time()

def check_stars():
    global done
    global stars

    stars_left = []
    for star in stars:
        if (star["x"] // TILE_SIZE != kolo["x"] // TILE_SIZE) or (star["y"] // TILE_SIZE != kolo["y"] // TILE_SIZE):
            stars_left.append(star)

    stars = stars_left

    res["score"] = res["font"].render("Score: " + str(total_stars - len(stars)), True, (0, 255, 0))

    if len(stars) == 0:
        print("You won!")
        done = True

def animate_frame():
    animate_foxes()
    animate_kolobok()

def draw_frame(screen):
    draw_map(screen)
    draw_stars(screen)

    draw_foxes(screen)
    draw_kolobok(screen)

    draw_score(screen, 0, 0)

def check_lose():
    global done

    for fox in foxes:
        if (fox["x"] // TILE_SIZE == kolo["x"] // TILE_SIZE) and (fox["y"] // TILE_SIZE == kolo["y"] // TILE_SIZE):
            print("Game over!")
            done = True

def control_kolobok(event):
    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_d:
            kolo["x_dir"] = ">"
        elif event.key == pygame.K_a:
            kolo["x_dir"] = "<"
        elif event.key == pygame.K_SPACE:
            if kolo["can_jump"] and kolo["y"] > TILE_SIZE:
                kolo["jumping"] = 3
                kolo["can_jump"] = False
    elif event.type == pygame.KEYUP:
        if (event.key == pygame.K_d) or (event.key == pygame.K_a):
            kolo["x_dir"] = "."

def game():
    global done

    pygame.init()

    load_map("map1.txt")
    setup_characters()

    screen = pygame.display.set_mode(SCREEN_SIZE)

    load_resources()

    pygame.display.set_caption(SCREEN_TITLE)

    done = False

    # fix foxes and kolobok at startup
    t = time.time()
    for fox in foxes:
        fox["last_x_update"] = t
    kolo["last_y_update"] = t

    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            else:
                control_kolobok(event)

        animate_frame()
        check_lose()
        check_stars()

        screen.fill((135, 206, 235))
        draw_frame(screen)
        pygame.display.flip()

    pygame.quit()

game()
