# 通过手动玩游戏生成操作数据并保存,用于模型的训练
import pygame
from pygame.locals import *
import math
from game_logic import my_item
import numpy as np

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

WALL_COLOR = (75, 60, 40)
WALL_WIDE = 12
lines = []
data = []
res = []

long_press = {'up': False, 'down': False, 'left': False, 'right': False}


def car_update(car):
    speed = 0
    direction = 0
    if long_press["up"]:
        speed = 1
        car.speed_up()
    if long_press["down"]:
        speed = -1
        car.speed_down()
    if long_press["left"]:
        direction = 0
        car.left_move()
    if long_press["right"]:
        direction = 1
        car.right_move()

    if long_press["up"] or long_press["down"] or long_press["left"] or long_press["right"]:
        data.append(
            [car.dis_wall, car.ldis_wall, car.lldis_wall, car.rdis_wall, car.rrdis_wall, car.v, car.r])
        res.append([speed, direction])
    return car


def rot_center(image, angle, topleft):
    """rotate an image while keeping its center and size"""
    rotated_image = pygame.transform.rotate(image, angle)
    rotated_rect = rotated_image.get_rect(center=image.get_rect(topleft=topleft).center)
    return rotated_image, rotated_rect


def carPaint(pygame, screen, car, image_car):
    rotated_image, rotated_rect = rot_center(image_car, 360 * (-1 * car.r) / (2 * math.pi), (car.x, car.y))
    screen.blit(rotated_image, rotated_rect.topleft)

    # 画车中心
    pygame.draw.circle(screen, YELLOW, car.get_center(), 4)

    # 画线
    pygame.draw.line(screen, YELLOW, car.get_center(), (car.dis_pos[0], car.dis_pos[1]))

    pygame.draw.line(screen, YELLOW, car.get_center(), (car.ldis_pos[0], car.ldis_pos[1]))
    pygame.draw.line(screen, YELLOW, car.get_center(), (car.lldis_pos[0], car.lldis_pos[1]))
    pygame.draw.line(screen, YELLOW, car.get_center(), (car.rdis_pos[0], car.rdis_pos[1]))
    pygame.draw.line(screen, YELLOW, car.get_center(), (car.rrdis_pos[0], car.rrdis_pos[1]))


class Line:
    def __init__(self, i, x1, y1, x2, y2):
        self.index = i
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2
        self.a = (y2 - y1) / (x2 - x1 + 1)
        self.b = y1 - self.a * x1
        self.minx = min(x1, x2)
        self.miny = min(y1, y2)
        self.maxx = max(x1, x2)
        self.maxy = max(y1, y2)


def initMap():
    from game_logic.map_data import map_lines
    line_num = 26
    for i in range(line_num):
        lines.append(Line(i + 1, map_lines[i][0][0], map_lines[i][0][1], map_lines[i][1][0], map_lines[i][1][1]))


# 绘制地图
def mapPaint(pygame, screen, bg):
    screen.blit(bg, Rect((0, 0), (0, 0)))


def gameStart():
    pygame.init()
    screen = pygame.display.set_mode((800, 600), 0, 32)

    initMap()

    bg = pygame.transform.scale(pygame.image.load("../image/bg.png"), (800, 600))

    car = my_item.Car(50, 220)
    image_car = pygame.transform.scale(pygame.image.load("../image/car_r.png"), car.size)

    clock = pygame.time.Clock()

    running = True

    while running:
        clock.tick(40)
        if car.alive:
            car.postion_move(0.01)
            car.computer_and_update(lines)
            car.is_live(lines)
            car = car_update(car)
        for even in pygame.event.get():
            if even.type == QUIT:
                # pygame.image.save(screen, "bg.png")
                running = False
            elif even.type == KEYDOWN:
                pressed_keys = pygame.key.get_pressed()
                if pressed_keys[K_ESCAPE]:
                    print("esc")
                    running = False
                else:
                    if even.key == pygame.K_UP:
                        long_press['up'] = True
                    if even.key == pygame.K_DOWN:
                        long_press['down'] = True
                    if even.key == pygame.K_LEFT:
                        long_press['left'] = True
                    if even.key == pygame.K_RIGHT:
                        long_press['right'] = True
            elif even.type == KEYUP:
                if even.key == pygame.K_UP:
                    long_press['up'] = False
                if even.key == pygame.K_DOWN:
                    long_press['down'] = False
                if even.key == pygame.K_LEFT:
                    long_press['left'] = False
                if even.key == pygame.K_RIGHT:
                    long_press['right'] = False

        mapPaint(pygame, screen, bg)
        carPaint(pygame, screen, car, image_car)
        pygame.display.flip()


if __name__ == "__main__":
    gameStart()
    np.savetxt('../ai_logic_自己实现神经网络/data/data3.txt', data, fmt='%.5f')
    np.savetxt('../ai_logic_自己实现神经网络/data/res3.txt', res, fmt='%.5f')
