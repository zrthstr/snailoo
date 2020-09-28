#!/usr/bin/env python3
#
# level tools can:
#
# generate random maps
# mirror maps, to the right, then downward
# (the snail, & is ignore)
#
# so this:
#
# -------
# | MM  |
# |    B|
# |  S  |
# | &   |
# -------
#
# becomes:
#
# ------------
# | MM    MM |
# |    BB    |
# |  S    S  |
# | &        |
# |          |
# |  S    S  |
# |    BB    |
# | MM    MM |
# ------------
#


import sys
import random

default = {
        "x":70,            ## x len
        "y":50,             ## y len
        "snakes": 10,       ## number of snakes
        "brick_movable_ratio":0.5, ## probbability of a space becoming a brick
        "walls": 23, ## probbability of a space becming a movable brick
        "wall_len": 3,
        }


def usage():
    print("usage:")
    print(f"{sys.argv[0]} mirror [mapfile]")
    print(f"{sys.argv[0]} random[_mirror]")
    print(f"{sys.argv[0]} random[_mirror] [x] [y] [snakes] [brick_movable_ratio] [wall_len] [walls]")
    print(f"where: x, y, snakes, walls, wall_len   --> positive int ")
    print(f"       brick_movable_ratio             --> 1 > float > 0 eg: 0.03")
    print("")
    print(f"       x            | x len of level")
    print(f"       y            | y len of level")
    print(f"       snake        | number of snakes")
    print(f"       wall len   | max wall len")

    sys.exit()


def random_map(args):
    global default
    global level

    # parse the optional args
    # unsure how to do this nicer with a normal dict
    if len(args) > 0:
        x = args.pop(0)
        default["x"] = int(x)
    if len(args) > 0:
        y = args.pop(0)
        default["y"] = int(y)
    if len(args) > 0:
        snakes = args.pop(0)
        default["snakes"] = int(snakes)
    if len(args) > 0:
        brick_movable_ratio = args.pop(0)
        default["brick_movable_ratio"] = float(brick_movable_ratio)
    if len(args) > 0:
        wall_len = args.pop(0)
        default["wall_len"] = int(wall_len)
    if len(args) > 0:
        wall_len = args.pop(0)
        default["walls"] = int(walls)


    x = default["x"]
    y = default["y"]
    snakes = default["snakes"]
    brick_movable_ratio = default["brick_movable_ratio"]
    wall_len = default["wall_len"]
    walls = default["walls"]

    print(f"Generating random map with:",
        "x -> {x}\n",
        "y -> {y}\n",
        "snakes -> {snakes}\n",
        "brick_movable_ratio -> {brick_movable_ratio}\n",
        "wall_len -> {wall_len}\n",
        "walls -> {walls}\n",  file=sys.stderr)


    level = [[" "] * x for l in  range(y)]
    #print_level(level)


    place_snakes(snakes,x,y)
    #print_level(level)
    place_walls(walls, wall_len, brick_movable_ratio, x, y)
    place_snail(x,y)


    #print_level(level)
    write_level(level)


def write_level(level):
    for line in level:
        print("".join(line))

def choose_brick(brick_movable_ratio):
    if random.random() > brick_movable_ratio:
        return "M"
    else:
        return "B"

def place_walls(walls, wall_len, brick_movable_ratio, x, y):
    global level
    for _ in range(0,walls):
        start = [random.randint(0,y-1), random.randint(0,x-1)]
        #print("SSS", start)
        #print_level(level)
        level[start[0]][start[1]] = choose_brick(brick_movable_ratio)
        direction = random.choice([[1,0],[0,1],[-1,0],[0,-1]])
        for _ in range(wall_len):
            next_y = start[0] + direction[0]
            next_x = start[1] + direction[1]
            if 0 < next_x < x and 0 < next_y < y: ## should this be x -1 and y -1 ?
                level[next_y][next_x] = choose_brick(brick_movable_ratio)
            start = [next_y,next_x]
            if random.randint(0,wall_len):
                break


def place_snakes(snakes,x,y):
    global level
    for _ in range(0,snakes):
        xx = random.randint(0,x-1)
        yy = random.randint(0,y-1)
        #print(f"{x} {y} {xx} {yy}")
        #level[random.randint(0,x)][random.randint(0,y)]="S"
        level[yy][xx]="S"
        

def place_snail(x,y):
    global level
    ## maybe check if can move??
    level[random.randint(0,y-1)][random.randint(0,x-1)]="&"

def mirror_map(filename):
    global level
    pass

def random_mirror():
    pass

def print_level(level):
    for line in level:
        print(line)


def main():
    if len(sys.argv) == 1:
        usage()
    if sys.argv[1] == "random":
        random_map(sys.argv[2:])
    elif sys.argv[1] == "mirror":
        if not len(sys.argv) == 3:
            usage()
        mirror_map(filename)
    elif sys.argv[1] == "random_mirror":
        random_mirror(sys.argv[2:])

if __name__ == "__main__":
    main()
