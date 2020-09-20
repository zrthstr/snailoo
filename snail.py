#!/usr/bin/env  python3

import sys
import pygame
import random
from pygame.locals import *
import time

GRID_SLEN = 30
GRAY =   (159,182,205) ## blude gray ??
RED = (255,  0,  0)
FPS = 3

UP = (1,0)
DOWN = (-1,0)
RIGHT = (0,1)
LEFT = (0,-1)

#GRID_WIDTH = 140
#GRID_HEIGHT = 100
#SCREEN_WIDTH = GRID_WIDTH * GRID_SLEN
#SCREEN_HEIGHT = GRID_HEIGHT * GRID_SLEN


class Snail:
    screen = 0

    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y

    def draw(self):
        snake_size = 10
        not_full = 0
        pygame.draw.circle(game.screen, RED, (self.x * GRID_SLEN, self.y * GRID_SLEN), snake_size, not_full)

    def go(self, direction):
        new_x = self.x
        new_y = self.y
        bnew_x = self.x
        bnew_y = self.y

        if direction == K_UP:
            new_y -= 1
            bnew_y -= 2
        elif direction == K_DOWN:
            new_y += 1
            bnew_y += 2
        elif direction == K_LEFT:
            new_x -= 1
            bnew_x -= 2
        elif direction == K_RIGHT:
            new_x += 1
            bnew_x += 2
        else:
            print(f"error, snake got bad movement instruction: {direction}")
            sys.exit()

        if game.snakes.is_snake(new_x, new_y):
            self.x = new_x
            self.y = new_y
            game.over()

        elif game.bricks.is_solid(new_x, new_y):
            #bell()
            return

        elif game.bricks.is_mobile(new_x, new_y):
            ## is_any is broken, why is this working? ## TODO
            if game.bricks.is_any(bnew_x, bnew_y) and not self.is_outside(bnew_x, bnew_y):
                game.bricks.rm(new_x, new_y)
                game.bricks.blist.append(Brick(bnew_x, bnew_y, True))

                if game.snakes.is_snake(bnew_x, bnew_y):
                    game.snakes.kill_or_cut(bnew_x, bnew_y)
                pass
            else:
                # bell()
                return

        elif self.is_outside(new_x, new_y):
            return

        self.x = new_x
        self.y = new_y


    def is_outside(self ,new_x, new_y):
        if new_x < 0 or new_y < 0 or new_x > game.max_x or new_y > game.max_y:
            return True
        return False



class Snake():
    def __init__(self,x,y):
        self.body = [(x,y)]
        self.directions = [UP, DOWN, RIGHT, LEFT]
        random.shuffle(self.directions)
        MIN_SNAKE_LEN = 2
        MAX_SNAKE_LEN = 8
        self.len = random.randint(MIN_SNAKE_LEN, MAX_SNAKE_LEN+1)

    def is_on(self, x, y):
        count = 0
        for part in self.body:
            count +=1
            if part == (x,y):
                return True, count
        return False, 0


    def do_move(self):
        direction = self.directions[0]
        new_head = (self.body[0][0] + direction[0], self.body[0][1] + direction[1])
        if len(self.body) > self.len:
            self.body.pop()
        self.body.insert(0,new_head)

    def can_do_any(self):
        for i in range(4):
            a = self.directions.pop(0)
            self.directions.insert(4,a)
            if self.can_continue():
                return True
        return False

    def can_continue(self):
        direction = self.directions[0]
        new_head = (self.body[0][0] + direction[0], self.body[0][1] + direction[1])

        if self.is_outside(* new_head):
            return False
        elif game.bricks.is_brickk(* new_head):
            return False
        elif game.snakes.is_snake(* new_head):
            return False
        return True

    def reverse_snake(self):
        self.body = self.body[::-1]

    def maybe_turn(self):
        if not random.randint(0,4):
            random.shuffle(self.directions)

    def check_if_has_eaten_snail(self):
        if self.body[0][0] == game.snail.x and self.body[0][1] == game.snail.y:
            game.over()

    def move(self):
        if self.can_continue():
            print("can_cont")
            self.do_move()
        elif self.can_do_any():
            print("can_do_any")
            self.do_move()
        else:
            print("reverse snake")
            self.reverse_snake()

        self.maybe_turn()
        self.check_if_has_eaten_snail()


    def is_outside(self, x, y):
        return x < 0 or y < 0 or x > game.max_x or y > game.max_y

    def is_snail(self,x ,y):
        return game.snail.x == x and game.snail.y == y


    def draw(self):
        snake_size = 15
        not_full = 0
        color = (10,200,20)
        for i, _ in enumerate(self.body):
            pygame.draw.circle(game.screen, color , (self.body[i][0] * GRID_SLEN, self.body[i][1] * GRID_SLEN), snake_size, not_full)
            color = (40,230,50)


class Snakes:
    screen = 0
    def __init__(self):
        self.slist = []

    def draw(self):
        for snake in self.slist:
            snake.draw()

    def is_snake(self, x, y):
        for snake in self.slist:
            if snake.is_on(x,y)[0]:
                return True
        return False

    def kill_or_cut(self,x ,y):
        for i, snake in enumerate(self.slist):
            _, count = snake.is_on(x,y)
            if count == 1:
                self.slist.pop(i)
                if len(self.slist) == 0:
                    game.win()
            else:
                snake.len = count
                snake.body = snake.body[0:count-1]


    def move(self):
        for snake in self.slist:
            snake.move()


class Brick:
    def __init__(self,x,y,movable):
        self.x = x
        self.y = y
        self.movable = movable
        self.color = [(0, 0,255), (0, 0,105)]


    def draw(self):
        snake_size = 10
        not_full = 0
        pygame.draw.circle(game.screen, self.color[self.movable] , (self.x * GRID_SLEN, self.y * GRID_SLEN), snake_size, not_full)


class Bricks:
    def __init__(self):
        self.blist = []

    def debug(self):
        for i, brick in enumerate(self.blist):
            print(i, brick.x, brick.y, brick.movable)

    def rm(self, x, y):
        for i, brick in enumerate(self.blist):
            if brick.x == x and brick.y == y:
                self.blist.pop(i)

    def draw(self):
        for b in self.blist:
            b.draw()

    def is_mobile(self, x, y):
        for brick in self.blist:
            if brick.x == x and brick.y == y and brick.movable == True:
                return True
        return False

    def is_solid(self, x, y):
        for brick in self.blist:
            if brick.x == x and brick.y == y and brick.movable == False:
                return True
        return False

    # TODO
    # only one of these should be needed...
    # yet this funtion seems broken
    def is_any(self, x, y):
        return not (self.is_mobile(x,y) or self.is_solid(x,y))
        #return not ((self.is_mobile(x,y) or self.is_solid(x,y)))

    def is_brickk(self, x, y):
        #print(f"testing if {x,y} is part of bricks")
        if self.is_mobile(x,y):
            #print("YES is m brick")
            return True
        elif self.is_solid(x,y):
            #print("YES is s brick")
            return True
        else:
            #print("no brick")
            return False



class Game:
    def __init__(self, level_file, BG_COLOR=GRAY):
        global bricks
        self.BG_COLOR = BG_COLOR
        pygame.init()
        #pygame.display.set_caption("dddddd")
        font = pygame.font.Font(None, 10)
        self.level_file = level_file
        self.bricks = Bricks()
        self.snakes = Snakes()
        self.max_x, self.max_y, self.snail = self.read_level_file(self.level_file)
        self.screen = pygame.display.set_mode( (GRID_SLEN * self.max_x, GRID_SLEN * self.max_y) )
        #self.snail.screen = self.screen
        #self.bricks.screen = self.screen


    def over(self):
        print("You lose .. :( ")
        game.draw()
        time.sleep(20)
        sys.exit()

    def win(self):
        print("You win!")
        time.sleep(3)
        sys.exit()

    def draw(self):
        not_full = 0
        snake_size = GRID_SLEN - 2
        self.bricks.draw()
        self.snakes.draw()
        self.snail.draw()
        pygame.display.update()

    def play(self):
        while True:
            self.handle_input()
            self.screen.fill(self.BG_COLOR)
            #self.screen.blit('222', textRect)
            game.snakes.move()
            self.draw()
            time.sleep(1/FPS)


    def handle_input(self):
            key_press = pygame.event.get(KEYDOWN)
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


    def read_level_file(self, level_file):
        with open(level_file, 'r') as f:
            lines = f.read().splitlines()
            max_len = max([len(i) for i in lines])
            len_x = max_len
            len_y = len(lines)

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
    global game

    if len(sys.argv) == 1:
        level='level1.lvl'
    else:
        level = sys.argv[1]

    game = Game(level)
    game.play()


if __name__ == "__main__":
    main()
