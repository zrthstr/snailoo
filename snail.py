#!/usr/bin/env  python3

import sys
import pygame
from pygame.locals import *

GRID_SLEN = 30
GRAY =   (159,182,205) ## blude gray ??
RED = (255,  0,  0)
#GRID_WIDTH = 140
#GRID_HEIGHT = 100
#SCREEN_WIDTH = GRID_WIDTH * GRID_SLEN
#SCREEN_HEIGHT = GRID_HEIGHT * GRID_SLEN


class Snail:
    def __init__(self, x=0, y=0):
        self.x = x * GRID_SLEN
        self.y = y * GRID_SLEN

    def go(self, direction):
        if direction == K_UP:
            #if self.y > 0:
            self.y -= 1 * GRID_SLEN

        elif direction == K_DOWN:
            #if self.y < min_y:
            self.y += 1 * GRID_SLEN

        elif direction == K_LEFT:
            #if self.x > 0:
            self.x -= 1 * GRID_SLEN

        elif direction == K_RIGHT:
            #if self.x < min_x:
            self.x += 1 * GRID_SLEN
        else:
            print(f"error, snake got bad moevemtn: {direction}")
            sys.exit()


class Snake():
    def __init__(self,x,y):
        self.head = (x,y)
        self.tail = []

class Snakes:
    def __init__(self):
        self.slist = []

class Brick:
    def __init__(self,x,y,movable):
        self.x = x
        self.y = y
        self.movable = movable

class Bricks:
    def __init__(self):
        self.blist = []

#class Grid:
#    def __init__(self, max_x, max_y):
#        self.max_x = max_x
#        self.max_y = max_y


class Game:
    def __init__(self, level_file="level1.lvl", BG_COLOR=GRAY):
        self.BG_COLOR = BG_COLOR
        pygame.init()
        pygame.display.set_caption("dddddd")
        font = pygame.font.Font(None, 10)

        self.level_file = level_file
        self.bricks = Bricks()
        #self.snail = Snail()
        self.snakes = Snakes()
        self.max_x, self.max_y, self.snail = self.read_level_file(self.level_file)
        self.screen = pygame.display.set_mode( (GRID_SLEN * self.max_x, GRID_SLEN * self.max_y) )

        #self.grid = Grid(x,y)

    def draw(self):
        not_full = 0
        snake_size = GRID_SLEN - 2

        pygame.draw.circle(self.screen, RED, (self.snail.x, self.snail.y), snake_size, not_full)

    def play(self):
        while True:
            #frame += 1
            #time.sleep(1 / FPS)
            #move_player(handle_input())
            #move_snake()
            #display(frame)
            self.handle_input()

            self.screen.fill(self.BG_COLOR)
            #self.screen.blit('222', textRect)
            self.draw()
            pygame.display.update()
            #pygame.event.clear()
        
    def handle_input(self):
            key_press = pygame.event.get(KEYDOWN)
            ##print(key_press)
            if len(key_press) != 0:
                #sys.exit()
                #if K_ESCAPE in key_press.key:
                #    print("escape key pressed, exiting")
                #    sys.exit()
                if key_press[0].key in [K_UP, K_DOWN, K_RIGHT, K_LEFT]:
                    self.snail.go(key_press.pop(0).key)
                else:
                    print("unknown key")
                    print(key_press[0].key)
            #pygame.event.clear()

    def read_level_file(self, level_file):
        with open(level_file, 'r') as f:
            #lines = f.readlines()
            lines = f.read().splitlines()
            max_len = max([len(i) for i in lines])

            len_x = max_len
            len_y = len(lines)
            print(f"len_x {len_x}  len_y {len_y}")

            #grid = [['V' ] * len_x] * len_y
            #print(grid)

            self.snakes = Snakes()
            for y, line in enumerate(lines):
                for x, o in enumerate(line):
                    if o == '&':
                        snail = Snail(x,y)
                    elif o == 'S':
                        self.snakes.slist.append(Snake(x,y))
                    elif o == 'B':
                        self.bricks.blist.append(Brick(x,y,False))
                    elif o == 'M':
                        self.bricks.blist.append(Brick(x,y,True))
                    elif o == ' ':
                        pass
                    else:
                        print(f"bad char: o")
                        sys.exit()
            return len_x, len_y, snail



def main():
    game = Game()
    #game.setup()
    game.play()


if __name__ == "__main__":
    main()
